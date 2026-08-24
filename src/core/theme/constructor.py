
from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.components.label_style import LabelStyle
from src.core.theme.components.line_edit_style import LineEditStyle
from src.core.theme.json_parser import JsonParser
from src.core.theme.primitives.border_style import BorderStyle
from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.primitives.dimension import Dimension
from src.core.theme.primitives.font_style import FontStyle
from src.core.theme.window_search.styles.icon_container import IconContainerStyle
from src.core.theme.window_search.styles.item_frame import ItemFrameStyle
from src.core.theme.window_search.styles.keybind_label import KeybindLabelStyle
from src.core.theme.window_search.styles.search_box import SearchBoxStyle
from src.core.theme.window_search.styles.search_box_line_edit import (
    SearchBoxLineEditStyle,
)
from src.core.theme.window_search.styles.selection_indicator import (
    SelectionIndicatorStyle,
)
from src.core.theme.window_search.styles.title_label import TitleLabelStyle
from src.core.theme.window_search.styles.window_item import WindowItemStyle
from src.core.theme.window_search.window_search import WindowSearchStyle


class ThemeConstructor:
    def __init__(self):
        self.json_parser: JsonParser = JsonParser()

    # ----- GENERAL PURPOSE COMPONENTS ----- #
    def get_line_edit_style(self, style: dict) -> LineEditStyle:
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

    def get_label_style(self, style: dict) -> LabelStyle:
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
        
    def get_frame_style(self, style: dict) -> FrameStyle:
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
    def get_search_box_line_edit_style(
        self, style: dict
    ) -> SearchBoxLineEditStyle:

        font_style: FontStyle = self.json_parser.get_font_style(
            style=style["font_style"]
        )
        border_style: BorderStyle = self.json_parser.get_border_style(
            style=style["border_style"]
        )
        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )

        margin: list = style["margin"]
        text_margin: list = style["text_margin"]

        return SearchBoxLineEditStyle(
            border_style=border_style,
            color_style=color_style,
            font_style=font_style,
            margin=margin,
            text_margin=text_margin
        )
    
    def get_search_box_style(self, style) -> SearchBoxStyle:
        dict_line_edit: dict = style["line_edit"]
        
        line_edit: SearchBoxLineEditStyle = self.get_search_box_line_edit_style(
            style=dict_line_edit
        )

        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )

        height: int = style["height"]

        return SearchBoxStyle(
            color_style=color_style,
            height=height,
            line_edit=line_edit
        )

    def get_item_frame_style(self, style: dict) -> ItemFrameStyle:

        # color style
        # border style

        # selection color
        # contents margin
        # height

        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )
        border_style: BorderStyle = self.json_parser.get_border_style(
            style=style["border_style"]
        )
        selection_color: ColorStyle = self.json_parser.get_color_style(
            style=style["selection_color_style"]
        )
        contents_margin: list = style["contents_margin"]
        height: int = style["height"]

        return ItemFrameStyle(
            border_style=border_style,
            color_style=color_style,
            contents_margin=contents_margin,
            height=height,
            selection_color=selection_color
        )
        

    def get_selection_indicator_style(
        self, style: dict
    ) -> SelectionIndicatorStyle:

        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )
        border_style: BorderStyle = self.json_parser.get_border_style(
            style=style["border_style"]
        )
        dimension: Dimension = self.json_parser.get_dimension(
            style=style["dimension"]
        )

        return SelectionIndicatorStyle(
            border_style=border_style,
            color_style=color_style,
            dimension=dimension
        )

    def get_icon_container_style(
        self, style: dict
    ) -> IconContainerStyle:

        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )

        border_style: BorderStyle = self.json_parser.get_border_style(
            style=style["border_style"]
        )
        
        dimension: Dimension = self.json_parser.get_dimension(
            style=style["dimension"]   
        )
        margin: list = style["margin"]

        selection_color = self.json_parser.get_color_style(
            style=style["selection_color_style"]
        )

        return IconContainerStyle(
            border_style=border_style,
            color_style=color_style,
            dimension=dimension,
            margin=margin,
            selection_color=selection_color
        )

    def get_title_label_style(self, style: dict) -> TitleLabelStyle:

        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )
        border_style: BorderStyle = self.json_parser.get_border_style(
            style=style["border_style"]
        )
        font_style: FontStyle = self.json_parser.get_font_style(
            style=style["font_style"]
        )
        margin = style["margin"]
        selection_color: ColorStyle = self.json_parser.get_color_style(
            style=style["selection_color_style"]
        )

        return TitleLabelStyle(
            border_style=border_style,
            color_style=color_style,
            font_style=font_style,
            margin=margin,
            selection_color=selection_color
        )
        
    def get_keybind_label_style(self, style) -> KeybindLabelStyle:
        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )
        border_style: BorderStyle = self.json_parser.get_border_style(
            style=style["border_style"]
        )
        font_style: FontStyle = self.json_parser.get_font_style(
            style=style["font_style"]
        )
        margin: int = style["margin"]
        selection_color: ColorStyle = self.json_parser.get_color_style(
            style=style["selection_color_style"]
        )
        dimension: Dimension = self.json_parser.get_dimension(
            style=style["dimension"]   
        )

        return KeybindLabelStyle(
            border_style=border_style,
            color_style=color_style,
            dimension=dimension,
            font_style=font_style,
            margin=margin,
            selection_color=selection_color
        )
    
    def create_window_item(self, style) -> WindowItemStyle:
        frame: dict = style["frame"]
        components: dict = frame["components"]

        color_style: ColorStyle = self.json_parser.get_color_style(
            style=style["color_style"]
        )
        
        frame_style: ItemFrameStyle = self.get_item_frame_style(
            style=frame
        )
        
        selection_indicator: SelectionIndicatorStyle = self.get_selection_indicator_style(
            style=components["selection_indicator"]
        )
        
        icon_container: IconContainerStyle = self.get_icon_container_style(
            style=components["icon_container"]
        )
        
        title_label: TitleLabelStyle = self.get_title_label_style(
            style=components["title_label"]
        )
        
        keybind_label: KeybindLabelStyle = self.get_keybind_label_style(
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
        
        search_box: SearchBoxStyle = self.get_search_box_style(
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
