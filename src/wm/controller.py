import pygetwindow as gw
from pygetwindow import Win32Window

from src.core.events.event_bus import eventBus
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
        _ = eventBus.restoreWindow.connect(self.restore_window)
        _ = eventBus.maximizeWindow.connect(self.maximize_window)
        _ = eventBus.minimizeWindow.connect(self.minimize_window)

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

    def restore_window(self):
        hwnd = self.get_focused_window()

        if not hwnd:
            return

        window: Win32Window = Win32Window(hwnd)
        window.restore()

    def get_focused_window(self) -> int:
        window: Win32Window | None = gw.getActiveWindow()
        if not window:
            return

        if self.window_scanner.is_regular_window(window._hWnd):
            return window._hWnd

        print("returning becuase not regular window")
        return 0

    def focus_window(self, hwnd: int):
        window: Win32Window = Win32Window(hwnd)
        window.activate()
        window.maximize()

    def close(self, hwnd: int):
        window: Win32Window = Win32Window(hwnd)
        window.close()

    def minimize(self, hwnd: int):
        window: Win32Window = Win32Window(hwnd)
        window.minimize()

    def restore(self, hwnd: int):
        window: Win32Window = Win32Window(hwnd)
        window.restore()

    def maximize(self, hwnd: int):
        window = Win32Window(hwnd)
        window.maximize()
