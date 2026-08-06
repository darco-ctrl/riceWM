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

    

    def window_created(self, hwnd: int):

        window: WindowInfo | None = self.window_scanner.window_by_hwnd(hwnd)
        

        if not window:
            return
        print(f"creating window: {window.title}")
        
        self.set_focused_window(window)

    def window_deystroyed(self, hwnd: int):
        window = self.registry.virtual_desktop.remove_window(hwnd)

        if not window: return
        if window != self.registry.focused_window: return
        
        self.registry.focused_window = None
        window.set_focused(False)

    def window_maximized(self, hwnd: int):
        window = self.registry.virtual_desktop.get_window(hwnd)

        if not window: return
        self.set_focused_window(window)

    def window_minimized(self, hwnd: int):
        window = self.registry.virtual_desktop.get_window(hwnd)
        f_window = self.registry.focused_window
    
        if not window or not f_window:
            return
    
        if window.hwnd != f_window.hwnd:
            return
    
        self.clear_focused_window()

    def window_fullscreen(self, hwnd: int):
        window = self.registry.virtual_desktop.get_window(hwnd)
    
        if not window:
            return
    
        self.set_focused_window(window)

    def window_focused(self, hwnd: int):
        window = self.registry.virtual_desktop.get_window(hwnd)
    
        if not window:
            return
    
        self.set_focused_window(window)

    def minimize(self, hwnd: int):
        print("Focused:", self.registry.focused_window.title if self.registry.focused_window else None)
        print("Minimized event:", hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def maximize(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def fullscreen(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SHOW_FULLSCREEN)

    def set_focus(self, hwnd: int):
        if not win32gui.IsWindow(hwnd):
            return
    
        if win32gui.GetForegroundWindow() == hwnd:
            return
    
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
        f_window = self.registry.focused_window
    
        if f_window and f_window.hwnd == window.hwnd:
            window.set_focused(True)
    
            if win32gui.IsIconic(window.hwnd):
                self.maximize(window.hwnd)
    
            self.set_focus(window.hwnd)
            return
    
        if f_window:
            f_window.set_focused(False)
            self.minimize(f_window.hwnd)
    
        self.registry.focused_window = window
        window.set_focused(True)
    
        self.maximize(window.hwnd)
        self.set_focus(window.hwnd)
