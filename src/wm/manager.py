from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner
from src.wm.controller import WindowController
from src.wm.registry import WindowRegistry


class WindowManager:
    def __init__(self, window_scanner: WindowScanner) -> None:
        self.registry = WindowRegistry(
            window_scanner=window_scanner
        )
        self.controller = WindowController(
            self.registry, window_scanner
        )
        self.window_scanner = window_scanner

    def initalize_wm(self):
        windows = self.window_scanner.get_windows_info()

        self.initiate(windows)

    def initiate(self, windows: list[WindowInfo]):

        for window in windows:
            self.set_foreground_window(window)

    def set_foreground_window(self, window: WindowInfo):
        hwnd = window.hwnd

        if not window.is_focused:
            # self.controller.minimize(hwnd)
            return

        if self.registry.focused_window:
            self.registry.focused_window.set_focused(False)

        self.registry.focused_window = window
        self.controller.maximize(hwnd)
