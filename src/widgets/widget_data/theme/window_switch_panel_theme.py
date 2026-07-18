from dataclasses import dataclass, field
from operator import is_, truediv
from turtle import back, window_width

from PySide6.QtGui import QFont

FONT_CLASS = {
    "Thin": QFont.Weight.Thin,
    "Light": QFont.Weight.Light,
    "Normal": QFont.Weight.Normal,
    "Medium": QFont.Weight.Medium,
    "Bold": QFont.Weight.Bold,
    "Black": QFont.Weight.Black
}

@dataclass(frozen=True)
class Panel:
    background_color: str
    window_width: int

@dataclass(frozen=True)
class SearchBox:
    height: int
    background_color: str

@dataclass(frozen=True)
class FontStyle:

    family: str
    weight: str
    color: str
    letter_spacing: float
    pixel_size: int
    is_bold: bool
    is_italic: bool
    is_underline: bool
    is_strike_out: bool = True

@dataclass(frozen=True)
class LineEdit:
    border_style: str
    border_radius: int
    border_width: list
    margin: list
    text_margin: list
    background_color: str
    border_color: str

class WindowSwitchPanelTheme:
    def __init__(self, data: dict):
        self.data = data

        self.main_panel: Panel = self.create_panel(data)
        self.search_box: SearchBox = self.create_search_box(data)
        self.line_edit: LineEdit = self.create_line_edit(data)
        self.font_style: FontStyle = self.create_font_style(data)

    def create_panel(self, data) -> Panel:

        window_panel_dict = data["window_panel"]

        panel: Panel = Panel(
            window_width=window_panel_dict["window_width"],
            background_color=window_panel_dict["background_color"]
        )
        return panel

    def create_search_box(self, data) -> SearchBox:
        search_box_dict = data["search_box"]

        search_box = SearchBox(
            height=search_box_dict["height"],
            background_color=search_box_dict["background_color"]
        )
        return search_box

    def create_line_edit(self, data) -> LineEdit:
        line_edit_dict = data["search_box"]["line_edit"]

        line_edit = LineEdit(
            border_style=line_edit_dict["border_style"],
            border_radius=line_edit_dict["border_radius"],
            border_width=line_edit_dict["border_width"],
            border_color=line_edit_dict["border_color"],
            margin=line_edit_dict["margin"],
            text_margin=line_edit_dict["text_margin"],
            background_color=line_edit_dict["background_color"]
        )

        return line_edit

    def create_font_style(self, data) -> FontStyle:
        font_style_dict = data["search_box"]["line_edit"]["font_style"]

        font_style = FontStyle(
            family=font_style_dict["family"],
            weight=font_style_dict["weight"],
            color=font_style_dict["color"],
            pixel_size=font_style_dict["size"],
            letter_spacing=font_style_dict["letter_spacing"],
            is_bold=font_style_dict["is_bold"],
            is_italic=font_style_dict["is_italic"],
            is_underline=font_style_dict["is_underline"],
            is_strike_out=font_style_dict["is_strike_out"]
        )

        return font_style
