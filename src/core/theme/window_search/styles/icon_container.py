

from dataclasses import dataclass

from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.primitives.dimension import Dimension


@dataclass
class IconContainerStyle(FrameStyle):
    dimension: Dimension
    margin: list
    selection_color: ColorStyle
