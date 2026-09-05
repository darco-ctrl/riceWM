

from dataclasses import dataclass

from src.core.theme.primitives.color_style import ColorStyle


@dataclass 
class ColorDefinition:
    normal: ColorStyle
    selection: ColorStyle

@dataclass
class WindowItemColor:
    frame: ColorDefinition
    icon_container: ColorDefinition
    title_label: ColorDefinition
    keybind_label: ColorDefinition
