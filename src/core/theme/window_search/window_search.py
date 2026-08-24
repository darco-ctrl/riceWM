from dataclasses import dataclass

from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.window_search.styles.search_box import SearchBoxStyle
from src.core.theme.window_search.styles.window_item import WindowItemStyle


@dataclass
class WindowSearchStyle:
    color_style: ColorStyle
    search_box: SearchBoxStyle
    window_item: WindowItemStyle
