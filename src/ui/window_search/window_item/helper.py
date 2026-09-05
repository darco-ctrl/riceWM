
from src.models.window import WindowInfo
from src.ui.window_search.window_item.window_item import WindowItem


class WindowItemHelper:
    def get_info_index(self, info: WindowInfo, list: list[WindowInfo]) -> int:
        for i in range(0, len(list)):
            if list[i].hwnd == info.hwnd:
                return i

        return -1

    def get_window_item_index(
        self, 
        info: WindowInfo, 
        list: list[WindowItem]
    ) -> int:
        for i in range(0, len(list)):
            if list[i].info.hwnd == info.hwnd:
                return i

        return -1
