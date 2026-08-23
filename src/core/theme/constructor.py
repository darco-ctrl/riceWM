from turtle import st

from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.components.label_style import LabelStyle
from src.core.theme.components.line_edit_style import LineEditStyle
from src.core.theme.json_parser import JsonParser
from src.core.theme.primitives.border_style import BorderStyle
from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.primitives.font_style import FontStyle
from src.core.theme.window_search.models.frame_style import SelectableFrameStyle
from src.core.theme.window_search.models.label_style import SelectableLabelStyle
from src.core.theme.window_search.models.search_box import SearchBoxStyle
from src.core.theme.window_search.models.window_item import WindowItemStyle
from src.core.theme.window_search.window_search import WindowSearchStyle


class ThemeConstructor:
    def __init__(self):
        self.json_parser: JsonParser = JsonParser()

    # ----- GENERAL PURPOSE COMPONENTS ----- #
    def create_line_edit_style(self, style: dict) -> LineEditStyle:
        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )

        border_style: BorderStyle = self.json_parser.get_border_style(
            style=style["border_style"]
        )

        font_style: FontStyle = self.json_parser.get_font_style(
            style=style["font_style"]
        )

        return LineEditStyle(
            color_style=color_style,
            border_style=border_style,
            font_style=font_style
        )

    def create_label_style(self, style: dict) -> LabelStyle:
        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )

        border_style: BorderStyle = self.json_parser.get_border_style(
            style=style["border_style"]
        )

        font_style: FontStyle = self.json_parser.get_font_style(
            style=style["font_style"]
        )

        return LabelStyle(
            color_style=color_style,
            border_style=border_style,
            font_style=font_style
        )
        
    def create_frame_style(self, style: dict) -> FrameStyle:
        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )

        border_style: BorderStyle = self.json_parser.get_border_style(
            style=style["border_style"]
        )

        return FrameStyle(
            color_style=color_style,
            border_style=border_style
        )

    # ----- WINDOW SEARCH ----- #

    
    def create_window_item(self, style) -> WindowItemStyle:
        frame: dict = style["frame"]
        components: dict = frame["components"]

        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )
        
        frame_style: SelectableFrameStyle = self.create_selectable_frame(
            style=frame
        )
        
        selection_indicator: FrameStyle = self.create_frame_style(
            style=components["selection_indicator"]
        )
        
        icon_container: SelectableFrameStyle = self.create_selectable_frame(
            style=components["icon_container"]
        )
        
        title_label: SelectableLabelStyle = self.create_selectable_label_style(
            style=components["title_label"]
        )
        
        keybind_label: SelectableLabelStyle = self.create_selectable_label_style(
            style=components["keybind_label"]
        )

        return WindowItemStyle(
            color_style=color_style,
            frame_style=frame_style,
            icon_container=icon_container,
            keybind_label=keybind_label,
            selection_indicator=selection_indicator,
            title_label=title_label
        )
    
    def create_window_search(self, style: dict) -> WindowSearchStyle:
        dict_color_style: dict = style["color_style"]
        color_style: ColorStyle = self.json_parser.get_color_style(
            style=dict_color_style
        )
        
        search_box: SearchBoxStyle = self.create_search_box(
            style=style["search_box"]
        )
        window_item: WindowItemStyle = self.create_window_item(
            style=style["window_item"]
        )

        return WindowSearchStyle(
            color_style=color_style,
            search_box=search_box,
            window_item=window_item
        )
