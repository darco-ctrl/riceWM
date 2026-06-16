import ctypes
from ctypes import wintypes

import psutil
import win32con
import win32gui
import win32process
from pyvda import AppView, VirtualDesktop

user32 = ctypes.windll.user32

WINEVENT_OUTOFCONTEXT = 0x0000
EVENT_OBJECT_CREATE = 0x8000
EVENT_OBJECT_DESTROY = 0x8001
EVENT_SYSTEM_FOREGROUND = 0x0003
EVENT_OBJECT_NAMECHANGE = 0x800C
OBJID_WINDOW = 0


WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.HWND,
    wintypes.LONG,
    wintypes.LONG,
    wintypes.DWORD,
    wintypes.DWORD,
)


def is_pwa_process(pid):
    try:
        proc = psutil.Process(pid)
        cmdline = proc.cmdline()

        for arg in cmdline:
            if arg.startswith("--app-id=") or arg.startswith("--app="):
                return True, arg
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    return False, None


def is_window_on_current_desktop(hwnd: int) -> bool:

    try:
        app_view = AppView(hwnd)

        current_desktop = VirtualDesktop.current()

        return app_view.desktop.number == current_desktop.number

    except Exception:
        return False


def can_show_on_taskbar(hwnd: int) -> bool:
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

    if not is_window_on_current_desktop(hwnd):
        return False

    return True


def get_open_windows() -> dict[int, dict]:
    open_windows = dict[int, dict]()

    def callback(hwnd: int, _extra) -> bool:
        if not can_show_on_taskbar(hwnd):
            return True

        title = win32gui.GetWindowText(hwnd).strip()

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        is_pwa, pwa_arg = is_pwa_process(pid)

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


def callback(
    hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime
):
    if idObject != OBJID_WINDOW:
        return

    if event == EVENT_OBJECT_CREATE:
        # on_window_open(hwnd)
        pass

    elif event == EVENT_OBJECT_DESTROY:
        pass
        # dock_core.on_window_close(hwnd)
        # on_window_close(hwnd)

    elif event == EVENT_SYSTEM_FOREGROUND:
        pass
        # on_window_focus_change(hwnd)

    elif event == EVENT_OBJECT_NAMECHANGE:
        # on_window_title_change(hwnd)
        pass

    # print("window event:", event, hwnd)
    # QTimer.singleShot(150, sync_windows)


callback_ref = WinEventProcType(callback)

hook = user32.SetWinEventHook(
    EVENT_OBJECT_CREATE,
    EVENT_OBJECT_NAMECHANGE,
    0,
    callback_ref,
    0,
    0,
    WINEVENT_OUTOFCONTEXT,
)
