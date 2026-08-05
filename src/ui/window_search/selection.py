from src.ui.window_search.item import WindowItem
from src.ui.window_search.window_search import WindowSearch


class WindowStateController:
    def __init__(self, window: WindowSearch):
        self.window = window
        self.focus_window: WindowItem | None = None

    def set_focus_window(self, window_item: WindowItem):
        if self.focus_window:
            self.focus_window.set_focused(False)

        window_item.set_focused(True)
