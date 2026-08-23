

from dataclasses import dataclass

from src.core.theme.components.label_style import LabelStyle
from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.primitives.dimension import Dimension


@dataclass
class KeybindLabelStyle(LabelStyle):
    dimension: Dimension
    margine: int
    selection_color: ColorStyle
