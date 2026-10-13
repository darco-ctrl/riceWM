import keyboard
import pynput.keyboard as pkbaord

from app.event_logger import EventLogger, LogEventType
from src.core.events.event_bus import eventBus
from src.core.key_map.key_map import KeyMap
from src.core.key_map.models import ApplicationKM, WindowManagerKM, WindowSearchKM


class HotKeyManager:
    """Manages hotkeys, keymaps, and key press events."""
    
    def __init__(self, logger: EventLogger, key_map: KeyMap) -> None:
        self._logger = logger

        self._key_map = key_map
        self._global_handles = []
        self._panel_listener: pkbaord.GlobalHotKeys

        self._set_panel_listener()
        self._set_global_listener()
        self._connect_events()

    def _connect_events(self):
        eventBus.enablePanelKeys.connect(self._enable_panel_keys)
        eventBus.disablePanelKeys.connect(self._disable_panel_keys)

        
    def _set_panel_listener(self) -> None:
        wsp_key_map: WindowSearchKM = self._key_map.window_search
    
        self._panel_listener = pkbaord.GlobalHotKeys(
            {
                wsp_key_map.close_window: self._on_wsp_close,
                wsp_key_map.select_up: self._on_wsp_select_up,
                wsp_key_map.select_down: self._on_wsp_select_down,
            }
        )
    
    
    def _disable_panel_keys(self) -> None:
        if self._panel_listener.is_alive():
            self._panel_listener.stop()
    
    
    def _enable_panel_keys(self) -> None:
        if not self._panel_listener.is_alive():
            self._set_panel_listener()
            self._panel_listener.start()


    def _set_global_listener(self):
        wsp_key_map: WindowSearchKM = self._key_map.window_search
        data_manager: ApplicationKM = self._key_map.application
        window_manager: WindowManagerKM = self._key_map.window_manager
        vdesktop = window_manager.virtual_desktop
        window_controls = window_manager.window_controls

        mapping = {
            wsp_key_map.toggle: self._on_wsp_toggle,
            data_manager.restart_application: self._on_data_reload,
            vdesktop.create_new: self._on_vdesktop_new,
            vdesktop.delete_current: self._on_vdesktop_delete,
            vdesktop.go_left: self._on_vdesktop_left,
            vdesktop.go_right: self._on_vdesktop_right,
            window_controls.close: self._close_window,
            window_controls.restore: self._restore_window,
            window_controls.maximize: self._maximize_window,
            window_controls.minimize: self._minimize_window,
        }

        for combo, handler in mapping.items():
            hotkey_str = combo.replace("<", "").replace(">", "")
            handle = keyboard.add_hotkey(
                hotkey_str, handler, suppress=True, trigger_on_release=False
            )
            self._global_handles.append(handle)


    def _stop_globalkeys(self):
        for handle in self._global_handles:
            keyboard.remove_hotkey(handle)


    def _close_window(self):
        self._log("CLOSE_WINDOW")
        
        eventBus.closeWindow.emit()


    def _minimize_window(self):
        self._log("MINIMIZE_WINDOW")
        
        eventBus.minimizeWindow.emit()


    def _maximize_window(self):
        self._log("MAXIMIZE_WINDOW")
        
        eventBus.maximizeWindow.emit()


    def _restore_window(self):
        self._log("RESTORE_WINDOW")
        
        eventBus.restoreWindow.emit()


    def _on_wsp_select_up(self):
        eventBus.itemSelectUp.emit()


    def _on_wsp_select_down(self):
        eventBus.itemSelectDown.emit()


    def _on_data_reload(self):
        self._log("RESTART_APPLICATION")
        
        eventBus.requestRestartApplication.emit()


    def _on_wsp_toggle(self):
        self._log("WINDOW_SEARCH_PANEL_TOGGLE")
        
        eventBus.wspToggleRequested.emit()


    def _on_wsp_close(self):
        self._log("WINDOW_SEARCH_PANEL_CLOSE")
        
        eventBus.wspCloseRequested.emit()


    def _on_vdesktop_new(self):
        self._log("VIRTUAL_DESKTOP_NEW")
        
        eventBus.createNewVDesktop.emit()


    def _on_vdesktop_delete(self):
        self._log("VIRTUAL_DESKTOP_DELETE")
        
        eventBus.deleteCurrentVDesktop.emit()


    def _on_vdesktop_left(self):
        self._log("VIRTUAL_DESKTOP_GO_LEFT")
        
        eventBus.vDesktopGoLeft.emit()


    def _on_vdesktop_right(self):
        self._log("VIRTUAL_DESKTOP_GO_RIGHT")
        
        eventBus.vDesktopGoRight.emit()


    def _log(self, message: str):
        self._logger.log(
            log_type=LogEventType.KEY_PRESSED,
            message=message
        )


    def start(self):
        self._panel_listener.start()
        self._logger.log(
            log_type=LogEventType.INFO,
            message="Hotkey Manager has started"
        )
