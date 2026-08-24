from dataclasses import dataclass

from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.window_search.styles.search_box_line_edit import (
    SearchBoxLineEditStyle,
)


@dataclass
class SearchBoxStyle:
    height: int
    color_style: ColorStyle
    line_edit: SearchBoxLineEditStyle
