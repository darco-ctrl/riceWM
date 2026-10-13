import keyboard
import pynput.keyboard as pkbaord

from app.event_logger import EventLogger, LogEventType
from src.core.events.event_bus import eventBus
from src.core.key_map.key_map import KeyMap
from src.core.key_map.models import ApplicationKM, WindowManagerKM, WindowSearchKM


class HotKeyManager:
    def __init__(self, logger: EventLogger, key_map: KeyMap) -> None:
        self.logger = logger

        self.key_map = key_map
        self._global_handles = []
        self.panel_listner: pkbaord.GlobalHotKeys

        self.set_panel_listner()
        self.set_global_listner()

    def connect_events(self):
        eventBus.enablePanelKeys.connect(self.enable_panelkeys)
        eventBus.disablePanelKeys.connect(self.disable_panelkeys)

    def start(self):
        
        self.panel_listner.start()
        self.logger.log(
            log_type=LogEventType.INFO,
            message="Hotkey Manager has started"
        )

    def set_panel_listner(self):
        wsp_key_map: WindowSearchKM = self.key_map.window_search

        self.panel_listner = pkbaord.GlobalHotKeys(
            {
                wsp_key_map.toggle: self.on_wsp_toggle,
                wsp_key_map.close_window: self.on_wsp_close,
                wsp_key_map.select_up: self.on_wsp_select_up,
                wsp_key_map.select_down: self.on_wsp_select_down,
            }
        )

    def set_global_listner(self):
        data_manager: ApplicationKM = self.key_map.application
        window_manager: WindowManagerKM = self.key_map.window_manager
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
        }

        for combo, handler in mapping.items():
            hotkey_str = combo.replace("<", "").replace(">", "")
            handle = keyboard.add_hotkey(
                hotkey_str, handler, suppress=True, trigger_on_release=False
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
        self._log("CLOSE_WINDOW")
        
        eventBus.closeWindow.emit()

    def minimize_window(self):
        self._log("MINIMIZE_WINDOW")
        
        eventBus.minimizeWindow.emit()

    def maximize_window(self):
        self._log("MAXIMIZE_WINDOW")
        
        eventBus.maximizeWindow.emit()

    def restore_window(self):
        self._log("RESTORE_WINDOW")
        
        eventBus.restoreWindow.emit()

    def on_wsp_select_up(self):
        eventBus.itemSelectUp.emit()

    def on_wsp_select_down(self):
        eventBus.itemSelectDown.emit()

    def on_data_reload(self):
        self._log("RESTART_APPLICATION")
        
        eventBus.requestRestartApplication.emit()

    def on_wsp_toggle(self):
        self._log("WINDOW_SEARCH_PANEL_TOGGLE")
        
        eventBus.wspToggleRequested.emit()

    def on_wsp_close(self):
        self._log("WINDOW_SEARCH_PANEL_CLOSE")
        
        eventBus.wspCloseRequested.emit()

    def on_vdesktop_new(self):
        self._log("VIRTUAL_DESKTOP_NEW")
        
        eventBus.createNewVDesktop.emit()

    def on_vdesktop_delete(self):
        self._log("VIRTUAL_DESKTOP_DELETE")
        
        eventBus.deleteCurrentVDesktop.emit()

    def on_vdesktop_left(self):
        self._log("VIRTUAL_DESKTOP_GO_LEFT")
        
        eventBus.vDesktopGoLeft.emit()

    def on_vdesktop_right(self):
        self._log("VIRTUAL_DESKTOP_GO_RIGHT")
        
        eventBus.vDesktopGoRight.emit()

    def _log(self, message: str):
        self.logger.log(
            log_type=LogEventType.KEY_PRESSED,
            message=message
        )
