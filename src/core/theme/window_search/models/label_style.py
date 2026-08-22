from dataclasses import dataclass

from src.core.theme.components.label_style import LabelStyle
from src.core.theme.primitives.color_style import ColorStyle


@dataclass
class SelectableLabelStyle:
    label_style: LabelStyle
    selection_color: ColorStyle
