import json
from typing import Any

from src.core.events.event_bus import eventBus
from src.core.theme.models import (
    BorderStyle,
    FontStyle,
    IconContainer,
    ItemFrame,
    KeyBindLabel,
    LineEdit,
    SearchBox,
    SelectionIndicator,
    T_WindowSearch,
    TitleLabel,
    WindowItemsContainer,
)


class Theme:
    def __init__(self, theme_path: str):
        self.theme_file_path = theme_path
        self.name: str = ""
        self.window_search: T_WindowSearch

        self.load()

    def reload(self):
        print("reloading themes")
        self.load()
        eventBus.reloadWSPThemeRequested.emit()
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
        self.window_search = self.get_window_search(data["window_search"])

    def get_font_style(self, style: dict) -> FontStyle:
        return FontStyle(style=style)

    def get_border_style(self, style: dict) -> BorderStyle:
        return BorderStyle(style=style)

    def get_line_edit(self, style: dict) -> LineEdit:

        border_style = self.get_border_style(style["border"])
        font_style = self.get_font_style(style["font"])
        
        line_edit_style: LineEdit = LineEdit(
            style=style, border=border_style, font=font_style
        )

        return line_edit_style

    def get_search_box(self, style) -> SearchBox:

        line_edit = self.get_line_edit(style["line_edit"])
        
        search_box_style: SearchBox = SearchBox(
            style=style,
            line_edit=line_edit,
        )

        return search_box_style

    def get_keybind_label(self, style: dict) -> KeyBindLabel:
        font_style = FontStyle(style["font"])
        border_style = BorderStyle(style["border"])

        key_bind_label: KeyBindLabel = KeyBindLabel(
            style=style,
            border_style=border_style,
            font_style=font_style,
        )

        return key_bind_label

    def get_title_label(self, style) -> TitleLabel:
        font_style = FontStyle(style["font"])
        border_style = BorderStyle(style["border"])
        title_label: TitleLabel = TitleLabel(
            style=style,
            border_style=border_style,
            font_style=font_style,
        )

        return title_label

    def get_icon_container(self, style: dict) -> IconContainer:
        boredr: BorderStyle = BorderStyle(style=style["border"])
        
        container: IconContainer = IconContainer(
            style=style, border_style=boredr
        )

        return container

    def get_selection_indicator(self, style: dict) -> SelectionIndicator:
        selection_indicator = SelectionIndicator(
            style=style
        )

        return selection_indicator

    def get_item_frame(self, style: dict) -> ItemFrame:

        border = self.get_border_style(style["border"])
        keybind_label = self.get_keybind_label(style["keybind_label"])
        icon_container = self.get_icon_container(style["icon_container"])
        selection_indicator = self.get_selection_indicator(style["selection_indicator"])
        title_label = self.get_title_label(style["title_label"])
    
        item_frame = ItemFrame(
            style=style,
            border_Style=border,
            key_bind_label=keybind_label,
            icon_container=icon_container,
            selection_indicator=selection_indicator,
            title_label=title_label,
        )

        return item_frame

    def get_window_item_container(self, style: dict) -> WindowItemsContainer:

        item_frame = self.get_item_frame(style["frame"])
        
        window_items_container: WindowItemsContainer = WindowItemsContainer(
            style=style, item_frame=item_frame
        )
        return window_items_container

    def get_window_search(self, style: dict) -> T_WindowSearch:

        search_box = self.get_search_box(style["search_box"])
        window_item_container = self.get_window_item_container(style["window_item_container"])
        
        window_search = T_WindowSearch(
            style=style,
            search_box=search_box,
            window_item_container=window_item_container,
        )

        return window_search
