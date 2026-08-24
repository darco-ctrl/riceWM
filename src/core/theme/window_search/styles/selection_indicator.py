from dataclasses import dataclass

from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.primitives.dimension import Dimension


@dataclass
class SelectionIndicatorStyle(FrameStyle):
    dimension: Dimension
