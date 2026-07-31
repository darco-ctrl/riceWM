from pynput import keyboard

from core.hotkey.event_bus import events
from data.key_map.data_class import DataManager, WindowSwitchPanel
from data.key_map.key_map import KeyMap


class HotKeyManager:
    def __init__(self, key_map: KeyMap) -> None:
        self.key_map = key_map
        self.listner: keyboard.GlobalHotKeys

        self.set_listner()

    def set_listner(self):
        wsp_key_map: WindowSwitchPanel = self.key_map.window_switch_panel
        data_manager: DataManager = self.key_map.data_manager

        self.listner = keyboard.GlobalHotKeys(
            {
                wsp_key_map.toggle: self.on_wsp_toggle,
                data_manager.reload_data: self.on_data_reload,
            }
        )

    def start(self):
        self.listner.start()

    def on_data_reload(self):
        events.dataReloadRequested.emit()

    def on_wsp_toggle(self):
        events.wspToggleRequested.emit()
