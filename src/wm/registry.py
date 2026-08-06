from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner
from src.wm.virtual_desktop import RVirtualDesktop


class WindowRegistry:
    def __init__(self, window_scanner: WindowScanner):
        self.focused_window: WindowInfo | None = None

        self.virtual_desktop = RVirtualDesktop(
            name="first desktop",
            id=1,
            window_scanner=window_scanner
        )
