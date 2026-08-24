
from dataclasses import dataclass

from src.core.theme.components.label_style import LabelStyle
from src.core.theme.primitives.color_style import ColorStyle


@dataclass
class TitleLabelStyle(LabelStyle):
    margin: int
    selection_color: ColorStyle
