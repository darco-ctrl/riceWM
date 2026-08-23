from dataclasses import dataclass

from src.core.theme.primitives.border_style import BorderStyle
from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.primitives.dimension import Dimension


@dataclass
class FrameStyle:
    color_style: ColorStyle 
    border_style: BorderStyle
