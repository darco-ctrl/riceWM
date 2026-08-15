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
        eventBus.windowCreated.connect(self.window_created)
        eventBus.windowDeystroyed.connect(self.window_deystroyed)
        eventBus.windowMaximized.connect(self.window_maximized)
        eventBus.windowMinimized.connect(self.window_minimized)
        eventBus.windowFullscreen.connect(self.window_fullscreen)
        eventBus.windowFocused.connect(self.window_focused)
        eventBus.windowShow.connect(self.window_show)

        eventBus.windowGoLeft.connect(self.window_go_left)
        eventBus.windowGoRight.connect(self.window_go_right)

    def window_go_left(self):
        # This is for future
        pass

    def window_go_right(self):
        # This is for future
        pass

    def window_created(self, hwnd: int):
        pass
    
    def window_show(self, hwnd: int):

        create_new: bool = False
        window: WindowInfo | None = None
        window = self.registry.get_window(hwnd)

        if not window:
            create_new = True
            window = self.window_scanner.get_window_info(hwnd)

        if not window:
            return

        if create_new:
            self.registry.add_window(window)
        
        # print("window shwn")
        
        self.set_focused_window(window)
        
    def window_deystroyed(self, hwnd: int):
        self.registry.remove_window(hwnd)

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

    def clear_focused_window(self): 
        f_window: WindowInfo | None = self.registry.focused_window
        if not f_window:
            return

        f_window.set_focused(False)
        self.minimize(f_window.hwnd)
        self.registry.focused_window = None

    def set_focused_window(self, window: WindowInfo):
        # print(f"TItle of window: {window.title}")
        f_window = self.registry.focused_window
    
        if f_window and f_window.hwnd == window.hwnd:
            window.set_focused(True)
    
            if win32gui.IsIconic(window.hwnd):
                self.maximize(window.hwnd)
    
            self.set_focus(window.hwnd)
            return
    
        if f_window:
            f_window.set_focused(False)
    
        self.registry.focused_window = window
        window.set_focused(True)
    
        self.maximize(window.hwnd)
        self.set_focus(window.hwnd)
