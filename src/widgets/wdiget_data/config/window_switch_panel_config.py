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

        self.apply()

    def apply(self):
        pass
