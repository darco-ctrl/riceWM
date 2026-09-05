

from copy import copy

from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.window_search.styles.icon_container import IconContainerStyle
from src.core.theme.window_search.styles.keybind_label import KeybindLabelStyle
from src.core.theme.window_search.styles.title_label import TitleLabelStyle
from src.core.theme.window_search.styles.window_item import WindowItemStyle
from src.models.window import WindowInfo
from src.ui.window_search.window_item.models import ColorDefinition, WindowItemColor
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

    def get_window_item_color_def(self, style: WindowItemStyle):
        frame_style: FrameStyle = style.frame_style
        icon_container_style: IconContainerStyle = style.icon_container
        title_label_style: TitleLabelStyle = style.title_label
        keybind_label_style: KeybindLabelStyle = style.keybind_label
        
        frame: ColorDefinition = ColorDefinition(
            normal=frame_style.color_style,
            selection=frame_style.selection_color
        )
        icon_container: ColorDefinition = ColorDefinition(
            normal=icon_container_style.color_style,
            selection=icon_container_style.selection_color
        )
        title_label: ColorDefinition = ColorDefinition(
            normal=title_label_style.color_style,
            selection=title_label_style.selection_color
        )
        keybind_label: ColorDefinition = ColorDefinition(
            normal=keybind_label_style.color_style,
            selection=keybind_label_style.selection_color
        )

        return WindowItemColor(
            frame=frame,
            icon_container=icon_container,
            keybind_label=keybind_label,
            title_label=title_label
        )
