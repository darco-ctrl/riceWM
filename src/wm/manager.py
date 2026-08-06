from src.models.window import WindowInfo
from src.services.window_scanner import WindowScanner
from src.wm.controller import WindowController


class WindowManager:
    def __init__(self) -> None:
        self.controller = WindowController()
        self.window_scanner = WindowScanner()

        self.focused_window: WindowInfo | None = None

    def initalize_wm(self):
        windows = self.window_scanner.get_windows_info()

        self.initiate(windows)

    def initiate(self, windows: list[WindowInfo]):

        for window in windows:
            self.set_foreground_window(window)

    def set_foreground_window(self, window: WindowInfo):
        hwnd = window.hwnd

        if not window.is_focused:
            self.controller.minimize(hwnd)
            return

        if self.focused_window:
            self.focused_window.set_focused(False)
            self.controller.minimize(self.focused_window.hwnd)

        self.focused_window = window
        self.controller.maximize(hwnd)
