import json

from src.core.key_map.models import (
    DataManagerKM,
    VirtualDesktopKB,
    WindowControlsKB,
    WindowManagerKM,
    WindowSearchKM,
)


class KeyMap:
    def __init__(self, json_path: str) -> None:
        self.path = json_path

        self.data_manager: DataManagerKM
        self.window_search: WindowSearchKM
        self.window_manager: WindowManagerKM
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

        self.data_manager = DataManagerKM(reload_data=dict["reload_data"])

    def create_wsp_keybinds(self, data: dict):
        dict = data["window_search"]

        self.window_search = WindowSearchKM(
            close_window=dict["close_window"],
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
            close=win_controls_dict["close"],
            restore=win_controls_dict["restore"],
            maximize=win_controls_dict["maximize"],
            minimize=win_controls_dict["minimize"]
        )

        self.window_manager = WindowManagerKM(
            virtual_desktop=virtual_desktop, window_controls=window_controls
        )
