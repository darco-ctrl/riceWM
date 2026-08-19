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
