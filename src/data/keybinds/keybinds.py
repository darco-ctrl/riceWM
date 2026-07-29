import json

from src.data.keybinds.data_class import WindowSwitchPanel


class KeyBinds:
    def __init__(self, json_path: str) -> None:
        self.path = json_path

        self.window_switch_panel: WindowSwitchPanel

    def load(self):
        with open(self.path, "r") as file:
            print(f" Loading keybinds: {self.path}")

            data = json.load(file)
            self.create_data_classes(data)

            del data

    def create_data_classes(self, data: dict):
        self.create_wsp_keybinds(data)

    def create_wsp_keybinds(self, data: dict):
        dict = data["window_switch_panel"]

        self.window_switch_panel = WindowSwitchPanel(toggle=dict["toggle"])
