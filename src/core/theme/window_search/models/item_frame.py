
from dataclasses import dataclass

from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.primitives.color_style import ColorStyle


@dataclass
class ItemFrame(FrameStyle):
    height: int
    contents_margin: list
    selection_color: ColorStyle
