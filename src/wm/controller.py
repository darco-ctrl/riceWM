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
        _ = eventBus.windowCreated.connect(self.window_created)
        _ = eventBus.windowDeystroyed.connect(self.window_deystroyed)
        _ = eventBus.windowMaximized.connect(self.window_maximized)
        _ = eventBus.windowMinimized.connect(self.window_minimized)
        _ = eventBus.windowFullscreen.connect(self.window_fullscreen)
        _ = eventBus.windowFocused.connect(self.window_focused)
        _ = eventBus.windowShow.connect(self.window_show)

        _ = eventBus.windowGoLeft.connect(self.window_go_left)
        _ = eventBus.windowGoRight.connect(self.window_go_right)
        _ = eventBus.focusWindow.connect(self.focus_window)

    def focus_window(self, hwnd: int):
        # self.set_focus(hwnd)
        print(f"Open window: {hwnd}")

    def window_go_left(self):
        # This is for future
        pass

    def window_go_right(self):
        # This is for future
        pass

    def window_created(self, hwnd: int):
        pass
    
    def window_show(self, hwnd: int):
        is_valid_window = self.window_scanner.is_regular_window(
            hwnd=hwnd
        )

        if is_valid_window:
            self.maximize(hwnd)
        
    def window_deystroyed(self, hwnd: int):
        pass

    def window_maximized(self, hwnd: int):
        pass

    def window_minimized(self, hwnd: int):
        pass

    def window_fullscreen(self, hwnd: int):
        pass

    def window_focused(self, hwnd: int):
        pass

    def minimize(self, hwnd: int):
        print("minimizing window")
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def maximize(self, hwnd: int):
        self.set_focus(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def fullscreen(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SHOW_FULLSCREEN)

    def set_focus(self, hwnd: int):

        foreground_hwnd = win32gui.GetForegroundWindow()
        
        if not win32gui.IsWindow(hwnd):
            return
    
        if foreground_hwnd == hwnd:
            return

        prt_text_hwnd = "Current Hwnd: -"
        prt_text_title = "Current Title: -"
        if foreground_hwnd != 0:
            prt_text_hwnd += f"{foreground_hwnd}"
            prt_text_title += f"{win32gui.GetWindowText(foreground_hwnd)}"
        # print(prt_text_hwnd)
        # print(prt_text_title)
        # print(f"Target hwnd: {hwnd}")
        # print(f"Target title: {win32gui.GetWindowText(hwnd)}")
    
        try:
            win32gui.SetForegroundWindow(hwnd)
        except pywintypes.error as error:
            print(f"Could not focus hwnd {hwnd}: {error}")
