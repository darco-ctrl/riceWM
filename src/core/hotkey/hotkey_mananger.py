from pynput import keyboard

from core.hotkey.event_bus import events
from data.key_map.data_class import WindowSwitchPanel
from data.key_map.key_map import KeyMap


class HotKeyManager:
    def __init__(self, key_map: KeyMap) -> None:
        self.key_map = key_map
        self.listner: keyboard.GlobalHotKeys

        self.set_listner()

    def set_listner(self):
        wsp_key_map: WindowSwitchPanel = self.key_map.window_switch_panel

        self.listner = keyboard.GlobalHotKeys({wsp_key_map.toggle: self.on_hotkey})

    def start(self):
        self.listner.start()

    def on_hotkey(self):
        print("Hot key pressed")
        events.windowSwitchPanelRequested.emit()
