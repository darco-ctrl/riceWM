
from dataclasses import dataclass
from turtle import position

from src.core.theme.primitives.dimension import Dimension
from src.core.theme.virtual_desktop_notifier.styles.label import (
    VirtualDesktopNotifierLabelStyle,
)


@dataclass
class VirtualDesktopNotiferStyle:
    size: Dimension
    position: Dimension
    label: VirtualDesktopNotifierLabelStyle
