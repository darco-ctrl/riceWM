
from typing import Any

from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.primitives.border_style import BorderStyle
from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.primitives.dimension import Dimension
from src.core.theme.primitives.font_style import FontStyle


class JsonParser:

    # ------ GENERAL PURPOSE COMPONENTS ------ #
    def get_color_style(self, style: dict) -> ColorStyle: 
        return ColorStyle(
            background_color=style["background_color"],
            color=style["color"]
        )

    def get_border_style(self, style: dict) -> BorderStyle:
        return BorderStyle(
            color=style["color"],
            radius=style["radius"],
            style=style["style"],
            width=style["width"]
        )

    def get_font_style(self, style: dict) -> FontStyle:
        
        return FontStyle(
            family=style["family"],
            is_bold=style["is_bold"],
            is_italic=style["is_italic"],
            is_strike_out=style["is_strike_out"],
            is_underline=style["is_underline"],
            letter_spacing=style["letter_spacing"],
            pixel_size=style["pixel_size"],
            weight=style["weight"]
        )

    def get_dimension(self, style) -> Dimension:

        return Dimension(
            x=style["x"],
            y=style["y"]
        )
