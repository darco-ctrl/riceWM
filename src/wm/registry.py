from src.ui.window_search.item import WindowItem


class Registry:
    def __init__(self):
        self.focused_window: WindowItem | None = None
