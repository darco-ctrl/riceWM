from widgets.window_switch_panel.window_item import WindowItem


class TitleSearch:
    def __init__(self, window_items: list[WindowItem]) -> None:

        self.window_items: list[WindowItem] = window_items

    def search(self, text: str) -> list[WindowItem]:
        result: list[WindowItem] = []

        return result
