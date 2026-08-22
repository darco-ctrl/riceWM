from dataclasses import dataclass

from src.core.theme.components.line_edit_style import LineEditStyle
from src.core.theme.primitives.color_style import ColorStyle


@dataclass
class SearchBoxTheme:
    color_style: ColorStyle
    line_edit_style: LineEditStyle
