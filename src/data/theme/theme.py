import json
from dataclasses import dataclass

from data.theme.data_class import (
    Border,
    FontStyle,
    LineEdit,
    SearchBox,
    T_WindowSwitchPanel,
)


class Theme:
    def __init__(self, theme_path: str):
        self.theme_file_path = theme_path

        self.load()

        self.name: str
        self.window_switch_panel: T_WindowSwitchPanel

    def reload(self):
        self.load()

    def load(self):
        with open(self.theme_file_path, "r") as file:
            print(f"Loading Theme: {self.theme_file_path}.")

            data = json.load(file)
            self.create_data_classes(data)

            del data

    def create_data_classes(self, data: dict):
        self.name = data["name"]

        window_switch_panel_dict = data["window_switch_panel"]
        search_box_dict = window_switch_panel_dict["search_box"]
        line_edit_dict = search_box_dict["line_edit"]
        border_style_dict = line_edit_dict["border"]
        font_style_dict = line_edit_dict["font"]
        # FontSyle

        font_style: FontStyle = FontStyle(
            family=font_style_dict["family"],
            is_bold=font_style_dict["is_bold"],
            is_italic=font_style_dict["is_italic"],
            is_strike_out=font_style_dict["is_strike_out"],
            is_underline=font_style_dict["is_underline"],
            letter_spacing=font_style_dict["letter_spacing"],
            pixel_size=font_style_dict["size"],
            weight=font_style_dict["weight"],
        )

        # Border Style
        border_style: Border = Border(
            color=border_style_dict["color"],
            radius=border_style_dict["radius"],
            style=border_style_dict["style"],
            width=border_style_dict["width"],
        )

        # Line Edit
        line_edit_style: LineEdit = LineEdit(
            background_color=line_edit_dict["background_color"],
            color=line_edit_dict["color"],
            border=border_style,
            font=font_style,
            margin=line_edit_dict["margin"],
            text_margin=line_edit_dict["text_margin"],
        )

        # SearchBox
        search_box_style: SearchBox = SearchBox(
            background_color=search_box_dict["background_color"],
            height=search_box_dict["height"],
            line_edit=line_edit_style,
        )

        # Window Switch Panel
        self.window_switch_panel = T_WindowSwitchPanel(
            background_color=window_switch_panel_dict["background_color"],
            search_box=search_box_style,
            window_width=window_switch_panel_dict["window_width"],
        )
