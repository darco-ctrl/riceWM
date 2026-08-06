from uuid import UUID

from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner


class RVirtualDesktop:
    def __init__(
        self, 
        window_scanner: WindowScanner,
        name: str,
        id: UUID
    ):
        self.window_scanner: WindowScanner = window_scanner
        self.name: str = name
        self.windows: list[WindowInfo] = self.load_windows()

    def load_windows(self) -> list[WindowInfo]:
        windows = self.window_scanner.get_windows_info()
        return windows

    def get_window_info(self, hwnd) -> WindowInfo | None:
        for window in self.windows:
            if hwnd != window.hwnd:
                continue

            return window

        return None
