import win32con
import win32gui

from src.core.events.event_bus import eventBus
from src.ui.window_search.item import WindowItem
from src.wm.registry import WindowRegistry


class WindowController:
    def __init__(self, registry):
        self.connect_window_events()

        self.registry: WindowRegistry = registry

    def connect_window_events(self):
        eventBus.windowCreated.connect(self.window_created)
        eventBus.windowDeystroyed.connect(self.window_deystroyed)
        eventBus.windowMaximized.connect(self.window_maximized)
        eventBus.windowMinimized.connect(self.window_minimized)
        eventBus.windowFullscreen.connect(self.window_fullscreen)
        eventBus.windowFocused.connect(self.window_focused)

    def window_created(self, hwnd: int):

        f_window: WindowItem | None = self.registry.focused_window
        if f_window:
            f_window.set_focused(False)
            self.minimize(f_window.hwnd)

        self.maximize(hwnd)
        self.set_focus(hwnd)

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
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def maximize(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def fullscreen(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SHOW_FULLSCREEN)

    def set_focus(self, hwnd: int):
        win32gui.SetForegroundWindow(hwnd)
