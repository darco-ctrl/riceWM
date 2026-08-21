from dataclasses import dataclass
from typing import Any

from PySide6.QtGui import QFont


class FontStyle:
    def __init__(self, style: dict):
        self.family: str
        self.pixel_size: int
        self.letter_spacing: float
        self.is_bold: bool
        self.is_italic: bool
        self.is_underline: bool
        self.is_strike_out: bool
        self.weight: str

        self.load(style)

    def load(self, style: dict):
        self.family = style["family"]
        self.pixel_size = style["size"]
        self.letter_spacing = style["letter_spacing"]
        self.is_bold = style["is_bold"]
        self.is_italic = style["is_italic"]
        self.is_underline = style["is_underline"]
        self.is_strike_out = style["is_strike_out"]
        self.weight = style["weight"]

    def to_qfont(self, qfont: QFont) -> QFont:

        QWEIGHT = {
            "Thin": QFont.Weight.Thin,
            "Light": QFont.Weight.Light,
            "Normal": QFont.Weight.Normal,
            "Medium": QFont.Weight.Medium,
            "Bold": QFont.Weight.Bold,
            "Black": QFont.Weight.Black,
        }

        qfont.setFamily(self.family)
        qfont.setPixelSize(self.pixel_size)
        qfont.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, self.letter_spacing)
        qfont.setBold(self.is_bold)
        qfont.setItalic(self.is_italic)
        qfont.setUnderline(self.is_underline)
        qfont.setStrikeOut(self.is_strike_out)
        qfont.setWeight(QWEIGHT[self.weight])

        return qfont

class BorderStyle:
    def __init__(self, style: dict) -> None:
        self.style: str
        self.radius: int
        self.width: list
        self.color: str

        self.load(style)

    def load(self, style: dict):
        self.style = style["style"]
        self.radius = style["radius"]
        self.width = style["width"]
        self.color = style["color"]


class OnSelected:
    def __init__(self, 
                style: dict):
        self.background_color: str = ""
        self.color: str = ""

        self.load(style)

    def load(self, style: dict):
        self.background_color = style.get("background_color", "")
        self.color = style.get("color", "")

class LineEdit:
    def __init__(self, style: dict, font: FontStyle, border: BorderStyle) -> None:
        self.place_holder_text: str
        self.margin: list
        self.text_margin: list
        self.background_color: str
        self.color: str
        self.border_style: BorderStyle = border
        self.font_style: FontStyle = font

        self.load(style)

    def load(self, style: dict):
        self.place_holder_text = style["place_holder_text"]
        self.margin = style["margin"]
        self.text_margin = style["text_margin"]
        self.background_color = style["background_color"]
        self.color = style["color"]

    def to_style_sheet(self) -> str:
        return f"""
            border-style: {self.border_style.style};
            border-radius: {self.border_style.radius}px;
            border-left-width: {self.border_style.width[0]}px;
            border-top-width: {self.border_style.width[1]}px;
            border-right-width: {self.border_style.width[2]}px;
            border-bottom-width: {self.border_style.width[3]}px;
            background-color: {self.background_color};
            border-color: {self.border_style.color};
            color: {self.color}
        """


@dataclass
class SearchBox:
    def __init__(self, style: dict, line_edit: LineEdit) -> None:
        self.height: int
        self.background_color: str
        self.line_edit: LineEdit = line_edit

        self.load(style)

    def load(self, style: dict):
        self.height = style["height"]
        self.background_color = style["background_color"]


class KeyBindLabel:
    def __init__(
        self, 
        style: dict, 
        font_style: FontStyle, 
        border_style: BorderStyle
    ) -> None:
        self.width: int
        self.height: int
        self.background_color: str
        self.color: str
        self.margin: int
        self.font_style: FontStyle = font_style
        self.border_style: BorderStyle = border_style
        self.on_selected: OnSelected

        self.load(style)

    def load(self, style: dict):
        self.width = style["width"]
        self.height = style["height"]
        self.background_color = style["background_color"]
        self.color = style["color"]
        self.margin = style["margin"]

        self.on_selected = OnSelected(style=style["on_selected"])


class TitleLabel:
    def __init__(
        self, 
        style: dict, 
        font_style: FontStyle, 
        border_style: BorderStyle
    ) -> None:
        self.preload_text: str
        self.background_color: str
        self.color: str
        self.margin: int
        self.font_style: FontStyle = font_style
        self.border_style: BorderStyle = border_style
        self.on_selected: OnSelected 

        self.load(style)

    def load(self, style: dict):
        self.preload_text = style["preload_text"]
        self.background_color = style["background_color"]
        self.color = style["color"]
        self.margin = style["margin"]

        self.on_selected = OnSelected(style=style["on_selected"])


class IconContainer:
    def __init__(
        self, 
        style: dict, 
        border_style: BorderStyle) -> None:
        self.width: int
        self.height: int
        self.container_margin: list
        self.margin: list
        self.background_color: str
        self.border_style: BorderStyle = border_style
        self.on_selected: OnSelected 

        self.load(style)

    def load(self, style):
        self.width = style["width"]
        self.height = style["height"]
        self.container_margin = style["container_margin"]
        self.margin = style["margin"]
        self.background_color = style["background_color"]

        self.on_selected = OnSelected(style=style["on_selected"])


class SelectionIndicator:
    def __init__(self, style: dict) -> None:
        self.width: int
        self.height: int
        self.background_color: str

        self.load(style)

    def load(self, style: dict):
        self.width = style["width"]
        self.height = style["height"]
        self.background_color = style["background_color"]


class ItemFrame:
    def __init__(
        self,
        style: dict,
        border_Style: BorderStyle,
        selection_indicator: SelectionIndicator,
        icon_container: IconContainer,
        title_label: TitleLabel,
        key_bind_label: KeyBindLabel
    ) -> None:
        self.height: int
        self.contents_margin: list
        self.background_color: str
        self.border_style: BorderStyle = border_Style
        self.selection_indicator: SelectionIndicator = selection_indicator
        self.icon_container: IconContainer = icon_container
        self.title_label: TitleLabel = title_label
        self.key_bind_lable: KeyBindLabel = key_bind_label
        self.on_selected: OnSelected 

        self.load(style)

    def load(self, style: dict):
        self.height = style["height"]
        self.contents_margin = style["contents_margin"]
        self.background_color = style["background_color"]

        self.on_selected = OnSelected(style=style["on_selected"])


class WindowItemsContainer:
    def __init__(self, style: dict, item_frame: ItemFrame) -> None:
        self.background_color: str
        self.item_frame: ItemFrame = item_frame

        self.load(style)

    def load(self, style: dict):
        self.background_color = style["background_color"]


class T_WindowSearch:
    def __init__(
        self,
        style: dict,
        search_box: SearchBox,
        window_item_container: WindowItemsContainer,
    ) -> None:
        # window_width: int
        self.background_color: str
        self.search_box: SearchBox = search_box
        self.window_item_container: WindowItemsContainer = window_item_container

        self.load(style)

    def load(self, style: dict):
        self.background_color = style["background_color"]
