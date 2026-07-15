from dataclasses import dataclass

@dataclass
class Behavior:
    max_results_shown: int = 0
    set_height_auto: bool = True

@dataclass
class WindowPanel:
    width: int = 0

@dataclass
class SearchBox:
    height: int = 0

class WindowSwitchPanelConfig:
    def __init__(self, data: dict):
        self.data = data

        print(data)

        self.behavior: Behavior = self.create_behavior(data)
        self.window_panel: WindowPanel = self.create_window_panel(data)
        self.search_box: SearchBox = self.create_search_box(data)

    def create_behavior(self, data: dict) -> Behavior:
        behavior_dict = data["behavior"]
        behavior = Behavior(
            max_results_shown=behavior_dict["max_results_shown"],
            set_height_auto=behavior_dict["set_height_auto"]
        )

        return behavior

    def create_window_panel(self, data: dict) -> WindowPanel:
        window_panel_dict = data["window_panel"]

        window_panel = WindowPanel(
            width=window_panel_dict["window_width"]
        )

        return window_panel

    def create_search_box(self, data: dict) -> SearchBox:

        search_box_dict = data["search_box"]

        search_box = SearchBox(
            height=search_box_dict["search_box_height"]
        )

        return search_box
