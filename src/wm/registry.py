from src.services.window.scanner import WindowScanner
from src.ui.window_search.item import WindowItem
from src.wm.virtual_desktop import RVirtualDesktop


class WindowRegistry:
    def __init__(self, window_scanner: WindowScanner):
        self.focused_window: WindowItem | None = None

        self.virtual_desktop = RVirtualDesktop(
            name="first desktop",
            id=1,
            window_scanner=window_scanner
        )
