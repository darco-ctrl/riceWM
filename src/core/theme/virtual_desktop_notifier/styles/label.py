

from dataclasses import dataclass

from src.core.theme.components.label_style import LabelStyle


@dataclass
class VirtualDesktopNotifierLabelStyle(LabelStyle):
    prefix: str
    suffix: str
    text_margin: list
