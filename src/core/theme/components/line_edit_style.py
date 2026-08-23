from dataclasses import dataclass

from src.core.theme.primitives.border_style import BorderStyle
from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.primitives.dimension import Dimension
from src.core.theme.primitives.font_style import FontStyle


@dataclass
class LineEditStyle:
    color_style: ColorStyle
    border_style: BorderStyle
    font_style: FontStyle
