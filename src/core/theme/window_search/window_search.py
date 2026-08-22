from dataclasses import dataclass

from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.window_search.models.search_box import SearchBoxTheme
from src.core.theme.window_search.models.window_item import WindowItemTheme


@dataclass
class WindowSearchTheme:
    color_style: ColorStyle
    search_box: SearchBoxTheme
    window_item: WindowItemTheme
