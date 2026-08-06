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

    def get_window_index(self, hwnd) -> int:
        for i in range(len(self.windows)):
            window = self.windows[i]

            if window.hwnd != hwnd:
                continue

            return i

        return -1

    def get_window(self, hwnd) -> WindowInfo | None:
        window_index = self.get_window_index(hwnd)
        if window_index == -1:
            return None

        window = self.windows[window_index]

        return window

    def remove_window(self, hwnd) -> WindowInfo | None:
        window_index = self.get_window_index(hwnd)

        if window_index == -1:
            return None
        
        window = self.windows.pop(window_index)

        return window
