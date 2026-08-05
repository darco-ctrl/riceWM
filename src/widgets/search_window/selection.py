from widgets.search_window.item import WindowItem
from widgets.search_window.search_window import SearchWindow


class WindowStateController:
    def __init__(self, window: SearchWindow):
        self.window = window
        self.focus_window: WindowItem | None = None

    def set_focus_window(self, window_item: WindowItem):
        if self.focus_window:
            self.focus_window.set_focused(False)

        window_item.set_focused(True)
