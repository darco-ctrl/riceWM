import json
from dataclasses import dataclass

from core.hotkey.event_bus import events
from data.theme.data_class import (
    Border,
    FontStyle,
    ItemFrame,
    KeyBindLabel,
    LineEdit,
    SearchBox,
    SelectionIndicator,
    T_WindowSwitchPanel,
    TitleLabel,
    WindowIconLabel,
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
            text = file.read()
            print(f"\n\n {text} \n\n")
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
        selection_indicator_dict = frame_dict["selection_indicator"]
        icon_label_dict = frame_dict["icon_label"]
        title_label_dict = frame_dict["title_label"]
        key_bind_label_dict = frame_dict["key_bind_label"]

        font_style: FontStyle = FontStyle(style=font_style_dict)
        border_style: Border = Border(style=border_style_dict)

        line_edit_style: LineEdit = LineEdit(
            style=line_edit_dict, border=border_style, font=font_style
        )
        search_box_style: SearchBox = SearchBox(
            style=search_box_dict,
            line_edit=line_edit_style,
        )

        key_bind_label: KeyBindLabel = KeyBindLabel(key_bind_label_dict)

        title_label: TitleLabel = TitleLabel(title_label_dict)

        icon_label: WindowIconLabel = WindowIconLabel(style=icon_label_dict)

        selection_indicator: SelectionIndicator = SelectionIndicator(
            style=selection_indicator_dict
        )

        item_frame = ItemFrame(
            style=frame_dict,
            key_bind_label=key_bind_label,
            icon_label=icon_label,
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
