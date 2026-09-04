
from dataclasses import dataclass

from src.core.theme.components.frame_style import FrameStyle


@dataclass
class VirtualDesktopNotifierFrameStyle(FrameStyle):
    margin: list
