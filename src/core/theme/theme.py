import json
from dataclasses import dataclass

from src.core.hotkey.event_bus import events
from src.core.theme.data_class import (
    BorderStyle,
    FontStyle,
    IconContainer,
    ItemFrame,
    KeyBindLabel,
    LineEdit,
    SearchBox,
    SelectionIndicator,
    T_WindowSwitchPanel,
    TitleLabel,
    WindowItemsContainer,
)


class Theme:
    def __init__(self, theme_path: str):
        self.theme_file_path = theme_path
        self.name: str = ""
        self.window_switch_panel: T_WindowSwitchPanel

        self.load()

    def reload(self):
        print("reloading themes")
        self.load()
        events.reloadWSPThemeRequested.emit()
        print(f"applying new theme: {self.name}")

    def load(self):
        with open(self.theme_file_path, "r") as file:
            # text = file.read()
            # print(f"\n\n {text} \n\n")
            print(f"Loading Theme: {self.theme_file_path}.")

            file.seek(0)
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
        window_item_container = window_switch_panel_dict["window_item_container"]
        frame_dict = window_item_container["frame"]
        frame_border_dict = frame_dict["border"]
        selection_indicator_dict = frame_dict["selection_indicator"]
        icon_conatiner_dict = frame_dict["icon_container"]
        icon_container_border_dict = icon_conatiner_dict["border"]
        title_label_dict = frame_dict["title_label"]
        tl_font_dict = title_label_dict["font"]
        tl_border_dict = title_label_dict["border"]
        key_bind_label_dict = frame_dict["key_bind_label"]
        kbl_font_dict = key_bind_label_dict["font"]
        kbl_border_dict = key_bind_label_dict["border"]

        font_style: FontStyle = FontStyle(style=font_style_dict)
        ln_border_style: BorderStyle = BorderStyle(style=border_style_dict)

        line_edit_style: LineEdit = LineEdit(
            style=line_edit_dict, border=ln_border_style, font=font_style
        )
        search_box_style: SearchBox = SearchBox(
            style=search_box_dict,
            line_edit=line_edit_style,
        )

        kbl_font_style = FontStyle(kbl_font_dict)
        kbl_border_style = BorderStyle(kbl_border_dict)

        key_bind_label: KeyBindLabel = KeyBindLabel(
            style=key_bind_label_dict,
            border_style=kbl_border_style,
            font_style=kbl_font_style,
        )

        tl_font_style = FontStyle(tl_font_dict)
        tl_border_style = BorderStyle(tl_border_dict)
        title_label: TitleLabel = TitleLabel(
            style=title_label_dict,
            border_style=tl_border_style,
            font_style=tl_font_style,
        )

        i_container_border: BorderStyle = BorderStyle(style=icon_container_border_dict)
        i_container: IconContainer = IconContainer(
            style=icon_conatiner_dict, border_style=i_container_border
        )

        selection_indicator: SelectionIndicator = SelectionIndicator(
            style=selection_indicator_dict
        )

        cn_border_style: BorderStyle = BorderStyle(style=frame_border_dict)

        item_frame = ItemFrame(
            style=frame_dict,
            border_Style=cn_border_style,
            key_bind_label=key_bind_label,
            icon_container=i_container,
            selection_indicator=selection_indicator,
            title_label=title_label,
        )

        window_items_container: WindowItemsContainer = WindowItemsContainer(
            style=window_item_container, item_frame=item_frame
        )

        # Window Switch Panel
        self.window_switch_panel = T_WindowSwitchPanel(
            style=window_switch_panel_dict,
            search_box=search_box_style,
            window_item_container=window_items_container,
        )
