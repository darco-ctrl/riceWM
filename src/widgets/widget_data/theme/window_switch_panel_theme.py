from dataclasses import dataclass, field
from turtle import back, window_width

@dataclass
class Panel:
    background_color: str = ""
    window_width: int = 300

@dataclass
class SearchBox:
    height: int = 30
    background_color: str = ""

@dataclass
class LineEdit:
    border_style: str = "solid"
    border_radius: int = 3
    border_width: list = field(default_factory=lambda: [0, 0, 0, 0]) # [top, right, bottom, left]
    margin: list = field(default_factory=lambda: [0, 0, 0, 0]) # [top, right, bottom, left]
    text_margin: list = field(default_factory=lambda: [0, 0, 0, 0])
    background_color: str = "#1e1e2e"
    border_color: str = "#bac2de"

class WindowSwitchPanelTheme:
    def __init__(self, data: dict):
        self.data = data

        self.main_panel: Panel = self.create_panel(data)
        self.search_box: SearchBox = self.create_search_box(data)
        self.line_edit: LineEdit = self.create_line_edit(data)

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
