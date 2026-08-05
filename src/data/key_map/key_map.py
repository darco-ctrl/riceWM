import json

from src.data.key_map.data_class import DataManager, WindowSwitchPanel


class KeyMap:
    def __init__(self, json_path: str) -> None:
        self.path = json_path

        self.data_manager: DataManager
        self.window_switch_panel: WindowSwitchPanel

        self.load()

    def load(self):
        with open(self.path, "r") as file:
            print(f" Loading keybinds: {self.path}")

            data = json.load(file)
            self.create_data_classes(data)

            del data

    def create_data_classes(self, data: dict):
        self.create_wsp_keybinds(data)
        self.create_data_manager_keybinds(data)

    def create_data_manager_keybinds(self, data: dict):
        dict = data["data_manager"]

        self.data_manager = DataManager(reload_data=dict["reload_data"])

    def create_wsp_keybinds(self, data: dict):
        dict = data["window_switch_panel"]

        self.window_switch_panel = WindowSwitchPanel(toggle=dict["toggle"])
