import json

from app.event_logger import EventLogger, LogEventType
from src.core.key_map.models import (
    ApplicationKM,
    VirtualDesktopKB,
    WindowControlsKB,
    WindowManagerKM,
    WindowSearchKM,
)


class KeyMap:
    """Manages keymap configuration and key bindings."""
    
    def __init__(self, logger: EventLogger, json_path: str) -> None:
        self._path = json_path
        self._logger = logger
        
        self.application: ApplicationKM
        self.window_search: WindowSearchKM
        self.window_manager: WindowManagerKM
        
        self.load()


    def _create_data_classes(self, data: dict):
        self._create_wsp_keybinds(data)
        self._create_data_manager_keybinds(data)
        self._create_wm_keybind(data)


    def _create_data_manager_keybinds(self, data: dict):
        dict = data["application"]

        self.application = ApplicationKM(restart_application=dict["restart_application"])


    def _create_wsp_keybinds(self, data: dict):
        dict = data["window_search"]

        self.window_search = WindowSearchKM(
            close_window=dict["close_window"],
            toggle=dict["toggle"],
            select_up=dict["select_up"],
            select_down=dict["select_down"],
        )


    def _create_wm_keybind(self, data: dict):
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

        
    def load(self):
        with open(self._path, "r") as file:
            self._logger.log(
                log_type=LogEventType.LOAD_DATA,
                message=f"Loading keybinds: {self._path}"
            )

            data = json.load(file)
            self._create_data_classes(data)

            del data
