from poplib import POP3_SSL_PORT

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
                wsp_key_map.close_window: self.on_wsp_close,
                wsp_key_map.select_up: self.on_wsp_select_up,
                wsp_key_map.select_down: self.on_wsp_select_down,
                wsp_key_map.focus_window: self.on_focus_window,
                data_manager.reload_data: self.on_data_reload,
                vdesktop.create_new: self.on_vdesktop_new,
                vdesktop.delete_current: self.on_vdesktop_delete,
                vdesktop.go_left: self.on_vdesktop_left,
                vdesktop.go_right: self.on_vdesktop_right,
                window_controls.close: self.close_window,
                window_controls.fullscreen: self.fullscreen,
                window_controls.maximize: self.maximize_window,
                window_controls.minimize: self.minimize_window
            }
        )

    def close_window(self):
        eventBus.closeWindow.emit()

    def minimize_window(self):
        eventBus.minimizeWindow.emit()

    def maximize_window(self):
        eventBus.maximizeWindow.emit()

    def fullscreen(self):
        eventBus.fullscreenWindow.emit()

    def start(self):
        self.listner.start()

    def on_wsp_select_up(self):
        eventBus.itemSelectUp.emit()

    def on_wsp_select_down(self):
        eventBus.itemSelectDown.emit()

    def on_data_reload(self):
        eventBus.requestRestartApplication.emit()

    def on_wsp_toggle(self):
        eventBus.wspToggleRequested.emit()

    def on_wsp_close(self):
        eventBus.wspCloseRequested.emit()

    def on_focus_window(self):
        eventBus.wspFocusSelectedWindow.emit()

    def on_vdesktop_new(self):
        eventBus.createNewVDesktop.emit()

    def on_vdesktop_delete(self):
        eventBus.deleteCurrentVDesktop.emit()

    def on_vdesktop_left(self):
        eventBus.vDesktopGoLeft.emit()

    def on_vdesktop_right(self):
        eventBus.vDesktopGoRight.emit()
