from dataclasses import dataclass, field
from turtle import back

@dataclass
class Panel:
    background_color: str = ""

@dataclass
class SearchBox:
    padding: list = field(default_factory=lambda: [0, 0, 0, 0])
    background_color: str = ""

@dataclass
class LineEdit:
    corner_radius: int = 3
    border_width: int = 2
    padding: list = field(default_factory=lambda: [0, 0, 0, 0]) # [top, right, bottom, left]
    background_color: str = "#1e1e2e"
    border_color: str = "#bac2de"

class WindowSwitchPanelTheme:
    def __init__(self, data: dict):
        self.data = data

        self.main_panel: Panel = self.create_panel(data)
        self.search_box: SearchBox = self.create_search_box(data)
        self.line_edit: LineEdit = self.create_line_edit(data)

    def create_panel(self, data) -> Panel:

        panel: Panel = Panel(
            background_color=data["background_color"]
        )
        return panel

    def create_search_box(self, data) -> SearchBox:
        search_box_dict = data["search_box"]

        search_box = SearchBox(
            padding=search_box_dict["padding"],
            background_color=search_box_dict["background_color"]
        )
        return search_box

    def create_line_edit(self, data) -> LineEdit:
        line_edit_dict = data["line_edit"]

        line_edit = LineEdit(
            corner_radius=line_edit_dict["corner_radius"],
            border_width=line_edit_dict["border_width"],
            border_color=line_edit_dict["border_color"],
            padding=line_edit_dict["padding"],
            background_color=line_edit_dict["background_color"]
        )

        return line_edit
