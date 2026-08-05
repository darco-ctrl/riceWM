import ctypes

import psutil
import win32con
import win32gui
import win32process
from pyvda import AppView, VirtualDesktop

from src.services import icon_service
from src.services.window import WindowInfo

user32 = ctypes.windll.user32


class WindowScanner:
    def __init__(self):
        pass

    def is_pwa_process(self, pid):
        try:
            proc = psutil.Process(pid)
            cmdline = proc.cmdline()

            for arg in cmdline:
                if arg.startswith("--app-id=") or arg.startswith("--app="):
                    return True, arg
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        return False, None

    def is_window_on_current_desktop(self, hwnd: int) -> bool:

        try:
            app_view = AppView(hwnd)

            current_desktop = VirtualDesktop.current()

            return app_view.desktop.number == current_desktop.number

        except Exception:
            return False

    def is_regular_window(self, hwnd: int) -> bool:
        if not win32gui.IsWindowVisible(hwnd):
            return False

        title = win32gui.GetWindowText(hwnd).strip()
        if not title:
            return False

        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

        is_tool_window = bool(ex_style & win32con.WS_EX_TOOLWINDOW)
        is_app_window = bool(ex_style & win32con.WS_EX_APPWINDOW)

        if is_tool_window:
            return False

        owner = win32gui.GetWindow(hwnd, win32con.GW_OWNER)

        if owner and not is_app_window:
            return False

        class_name = win32gui.GetClassName(hwnd)

        exclude_classes = {
            "Windows.UI.Core.CoreWindow",  # UWP app containers
            # "ApplicationFrameWindow",  # UWP app frames (parent windows)
            "Progman",  # Desktop
            "WorkerW",  # Desktop worker
            "Shell_TrayWnd",  # Taskbar itself
            "SysListView32",  # Usually part of taskbar
            "NotifyIconOverflowWindow",  # System tray overflow
        }

        if class_name in exclude_classes:
            return False

        if class_name == "ApplicationFrameWindow":
            # Find the actual content window
            def find_content_window(h, _):
                child_class = win32gui.GetClassName(h)
                if child_class == "Windows.UI.Core.CoreWindow":
                    return False  # Stop enumeration
                return True

            win32gui.EnumChildWindows(hwnd, find_content_window, None)
            # If this is just a frame without content, skip it
            #
            return False

        if win32gui.IsIconic(hwnd):  # Minimized windows are fine, they're in taskbar
            pass

        if not self.is_window_on_current_desktop(hwnd):
            return False

        return True

    def get_open_windows(self) -> dict[int, dict]:
        open_windows = dict[int, dict]()

        def callback(hwnd: int, _extra) -> bool:
            if not self.is_regular_window(hwnd):
                return True

            title = win32gui.GetWindowText(hwnd).strip()

            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            is_pwa, pwa_arg = self.is_pwa_process(pid)

            try:
                process = psutil.Process(pid)
                process_name = process.name()

            except psutil.Error:
                return True

            open_windows[hwnd] = {
                "process_name": process_name,
                "title": title,
                "pid": pid,
                "hwnd": hwnd,
                "is_pwa": is_pwa,
                "pwa_arg": pwa_arg,
            }

            return True

        win32gui.EnumWindows(callback, None)
        return open_windows

    def get_windows_info(self) -> list[WindowInfo]:
        windows = []

        windows_dict = self.get_open_windows()

        for info in windows_dict.values():
            windows.append(self.create_window_info(info))

        return windows

    def get_app_name(self, pid) -> str:
        try:
            process = psutil.Process(pid)
            return process.name()
        except psutil.NoSuchProcess:
            return ""

    def create_window_info(self, window_data: dict) -> WindowInfo:
        #                "process_name": process_name,
        # "title": title,
        # "pid": pid,
        # "hwnd": hwnd,
        # "is_pwa": is_pwa,
        # "pwa_arg": pwa_arg,
        #

        hwnd: int = window_data["hwnd"]
        title: str = window_data["title"]
        pid: int = window_data["pid"]
        is_pwa: bool = window_data["is_pwa"]
        pwa_arg: str = window_data["pwa_arg"]
        icon_path: str = icon_service.get_icon_path(hwnd)

        name = ""
        if not is_pwa:
            self.get_app_name(pid=pid)

        window_info = WindowInfo(
            hwnd=hwnd,
            name=name,
            title=title,
            is_pwa=is_pwa,
            pwa_arg=pwa_arg,
            icon_path=icon_path,
        )

        return window_info
