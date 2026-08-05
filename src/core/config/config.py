import json
from dataclasses import dataclass

from src.core.config.data_class import Behavior, C_WindowSwitchPanel


class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path

        self.name: str
        self.window_switch_panel: C_WindowSwitchPanel
        self.load()

    def reload(self):
        self.load()

    def load(self):
        with open(self.config_path, "r") as file:
            print(f"Loading config: {self.config_path}.")

            data = json.load(file)
            print(data)
            self.create_data_classes(data)
            del data

    def create_data_classes(self, data: dict):
        self.name = data["name"]

        wsp_dict = data["window_switch_panel"]
        behavior_dict = wsp_dict["behavior"]
        # Behavior
        behavior: Behavior = Behavior(
            auto_adjust_height=behavior_dict["auto_adjust_height"],
            max_results_shown=behavior_dict["max_results_shown"],
        )

        # Window Switch Panel
        self.window_switch_panel = C_WindowSwitchPanel(
            behavior=behavior, window_width=wsp_dict["window_width"]
        )
