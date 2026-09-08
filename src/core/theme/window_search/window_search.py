from dataclasses import dataclass

from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.window_search.styles.search_box import SearchBoxStyle
from src.core.theme.window_search.styles.window_item import WindowItemStyle


@dataclass
class WindowSearchStyle(FrameStyle):
    search_box: SearchBoxStyle
    window_item: WindowItemStyle
