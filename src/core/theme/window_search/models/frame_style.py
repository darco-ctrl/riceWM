from dataclasses import dataclass

from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.primitives.color_style import ColorStyle


@dataclass
class SelectableFrameStyle:
    frame_style: FrameStyle
    selection_color: ColorStyle
