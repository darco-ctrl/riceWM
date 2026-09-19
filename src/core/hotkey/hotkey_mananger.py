import keyboard

from src.core.events.event_bus import eventBus
from src.core.key_map.key_map import KeyMap
from src.core.key_map.models import ApplicationKM, WindowManagerKM, WindowSearchKM


class HotKeyManager:
    def __init__(self, key_map: KeyMap) -> None:
        self.key_map = key_map
        self._global_handles = []

        self.set_global_listner()

    def connect_events(self):
        eventBus.enablePanelKeys.connect(self.enable_panelkeys)
        eventBus.disablePanelKeys.connect(self.disable_panelkeys)

    def start(self):
        pass

    def set_global_listner(self):
        data_manager: ApplicationKM = self.key_map.application
        window_manager: WindowManagerKM = self.key_map.window_manager
        window_search: WindowSearchKM = self.key_map.window_search
        vdesktop = window_manager.virtual_desktop
        window_controls = window_manager.window_controls

        mapping = {
            data_manager.restart_application: self.on_data_reload,
            vdesktop.create_new: self.on_vdesktop_new,
            vdesktop.delete_current: self.on_vdesktop_delete,
            vdesktop.go_left: self.on_vdesktop_left,
            vdesktop.go_right: self.on_vdesktop_right,
            window_controls.close: self.close_window,
            window_controls.restore: self.restore_window,
            window_controls.maximize: self.maximize_window,
            window_controls.minimize: self.minimize_window,
            window_search.toggle: self.on_wsp_toggle,
            window_search.close_window: self.on_wsp_close,
            window_search.select_down: self.on_wsp_select_down,
            window_search.select_up: self.on_wsp_select_up,
        }

        for combo, handler in mapping.items():
            handle = keyboard.add_hotkey(
                combo, handler, suppress=True, trigger_on_release=False
            )
            self._global_handles.append(handle)

    def stop_globalkeys(self):
        for handle in self._global_handles:
            keyboard.remove_hotkey(handle)

    def disable_panelkeys(self):
        self.panel_listner.stop()

    def enable_panelkeys(self):
        self.panel_listner.start()

    def close_window(self):
        eventBus.closeWindow.emit()

    def minimize_window(self):
        eventBus.minimizeWindow.emit()

    def maximize_window(self):
        eventBus.maximizeWindow.emit()

    def restore_window(self):
        eventBus.restoreWindow.emit()

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

    def on_vdesktop_new(self):
        eventBus.createNewVDesktop.emit()

    def on_vdesktop_delete(self):
        eventBus.deleteCurrentVDesktop.emit()

    def on_vdesktop_left(self):
        eventBus.vDesktopGoLeft.emit()

    def on_vdesktop_right(self):
        eventBus.vDesktopGoRight.emit()
