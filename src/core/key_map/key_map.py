import json

from src.core.key_map.models import (
    DataManagerKB,
    VirtualDesktopKB,
    WindowControlsKB,
    WindowManagerKB,
    WindowSwitchPanelKB,
)


class KeyMap:
    def __init__(self, json_path: str) -> None:
        self.path = json_path

        self.data_manager: DataManagerKB
        self.window_switch_panel: WindowSwitchPanelKB
        self.window_manager: WindowManagerKB
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
        self.create_wm_keybind(data)

    def create_data_manager_keybinds(self, data: dict):
        dict = data["data_manager"]

        self.data_manager = DataManagerKB(reload_data=dict["reload_data"])

    def create_wsp_keybinds(self, data: dict):
        dict = data["window_search"]

        self.window_switch_panel = WindowSwitchPanelKB(
            toggle=dict["toggle"],
            select_up=dict["select_up"],
            select_down=dict["select_down"],
        )

    def create_wm_keybind(self, data: dict):
        dict = data["window_manager"]

        v_desktop_dict = dict["virtual_desktop"]
        virtual_desktop = VirtualDesktopKB(
            create_new=v_desktop_dict["create_new"],
            delete_current=v_desktop_dict["delete_current"],
            go_left=v_desktop_dict["go_left"],
            go_right=v_desktop_dict["go_right"],
        )

        win_controls_dict = dict["window_controls"]
        window_controls = WindowControlsKB(
            go_left=win_controls_dict["go_left"], go_right=win_controls_dict["go_right"]
        )

        self.window_manager = WindowManagerKB(
            virtual_desktop=virtual_desktop, window_controls=window_controls
        )
