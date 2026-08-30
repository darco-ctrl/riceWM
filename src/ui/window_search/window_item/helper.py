

from src.models.window import WindowInfo


class WindowItemHelper:
    def get_info_index(self, info: WindowInfo, list: list[WindowInfo]) -> int:
        for i in range(0, len(list)):
            if list[i].hwnd == info.hwnd:
                return i

        return -1
