from pynput import keyboard

from src.core.events.event_bus import eventBus
from src.core.key_map.key_map import KeyMap
from src.core.key_map.models import DataManagerKB, WindowManagerKB, WindowSwitchPanelKB



class HotKeyManager:
    def __init__(self, key_map: KeyMap) -> None:
        self.key_map = key_map
        self.listner: keyboard.GlobalHotKeys

        self.set_listner()

    def set_listner(self):
        wsp_key_map: WindowSwitchPanelKB = self.key_map.window_switch_panel
        data_manager: DataManagerKB = self.key_map.data_manager

        window_manager: WindowManagerKB = self.key_map.window_manager
        vdesktop = window_manager.virtual_desktop
        window_controls = window_manager.window_controls

        self.listner = keyboard.GlobalHotKeys(
            {
                wsp_key_map.toggle: self.on_wsp_toggle,
                data_manager.reload_data: self.on_data_reload,
                vdesktop.create_new: self.on_vdesktop_new,
                vdesktop.delete_current: self.on_vdesktop_delete,
                vdesktop.go_left: self.on_vdesktop_left,
                vdesktop.go_right: self.on_vdesktop_right,
                window_controls.go_left: self.on_window_left,
                window_controls.go_right: self.on_window_right
            }
        )

    def start(self):
        self.listner.start()

    def on_data_reload(self):
        eventBus.dataReloadRequested.emit()

    def on_wsp_toggle(self):
        eventBus.wspToggleRequested.emit()

    def on_vdesktop_new(self):
        eventBus.createNewVDesktop.emit()

    def on_vdesktop_delete(self):
        print("emit")
        eventBus.deleteCurrentVDesktop.emit()

    def on_vdesktop_left(self):
        eventBus.vDesktopGoLeft.emit()

    def on_vdesktop_right(self):
        eventBus.vDesktopGoRight.emit()

    def on_window_left(self):
        eventBus.windowGoLeft.emit()

    def on_window_right(self):
        eventBus.windowGoRight.emit()
