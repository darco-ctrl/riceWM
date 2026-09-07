from pyvda.pyvda import AppView, VirtualDesktop
import pywintypes
import win32con
import win32gui

from src.core.events.event_bus import eventBus
from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner
from src.wm.registry import WindowRegistry


class WindowController:
    def __init__(self, registry, window_scanner):
        self.connect_window_events()

        self.window_scanner: WindowScanner = window_scanner
        self.registry: WindowRegistry = registry

    def connect_window_events(self):
        _ = eventBus.focusWindow.connect(self.focus_window)
        _ = eventBus.closeWindow.connect(self.close_Window)
        _ = eventBus.maximizeWindow.connect(self.maximize_window)
        _ = eventBus.minimizeWindow.connect(self.minimize_window)
        _ = eventBus.fullscreenWindow.connect(self.fullscreen_window)

    def close_Window(self):
        hwnd = self.get_focused_window()

        if not hwnd:
            return

        self.close(hwnd)

    def minimize_window(self):
        hwnd = self.get_focused_window()

        if not hwnd:
            return

        self.minimize(hwnd)

    def maximize_window(self):
        hwnd = self.get_focused_window()

        if not hwnd:
            return

        self.maximize(hwnd)

    def fullscreen_window(self):
        hwnd = self.get_focused_window()

        if not hwnd:
            return

        self.fullscreen(hwnd)

    def get_focused_window(self) -> int:
        hwnd: int = win32gui.GetForegroundWindow()
        
        if self.window_scanner.is_regular_window(hwnd):
            return hwnd

        print("returning becuase not regular window")
        return 0

    def focus_window(self, hwnd: int):
        try:
            window_view: AppView = AppView(hwnd=hwnd)

            desktop: VirtualDesktop = window_view.desktop
            desktop.go()

            self.set_focus(hwnd)
        except Exception as e:
            print(f"Failed to retrive Virtual Desktop,\n error: {e}")

    def close(self, hwnd: int):
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def minimize(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def maximize(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def fullscreen(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SHOW_FULLSCREEN)

    def set_focus(self, hwnd: int):

        foreground_hwnd = win32gui.GetForegroundWindow()
        
        if not win32gui.IsWindow(hwnd):
            return
    
        if foreground_hwnd == hwnd:
            return

        # print(prt_text_hwnd)
        # print(prt_text_title)
        # print(f"Target hwnd: {hwnd}")
        # print(f"Target title: {win32gui.GetWindowText(hwnd)}")
    
        try:
            win32gui.SetForegroundWindow(hwnd)
        except pywintypes.error as error:
            print(f"Could not focus hwnd {hwnd}: {error}")
