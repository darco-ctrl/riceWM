import os
import sys

from PySide6.QtWidgets import QApplication

import src.app.paths as rice_paths
from app.event_logger import EventLogger, LogEventType
from src.app.bootstrap import BootStrap
from src.config.app_config import AppConfig
from src.core.data_manager import DataManager
from src.core.events.event_bus import eventBus
from src.core.hotkey.hotkey_mananger import HotKeyManager
from src.services.commands.command_service import CommandService
from src.services.window.scanner import WindowScanner
from src.ui.tray.tray import Tray
from src.ui.ui_manager import UIManager
from src.wm.manager import WindowManager


class App:
    def __init__(self):
        self._bootstrap = self._create_bootstrap()
        self._logger = self._create_event_logger()
        self._application = self._create_application()
        self._window_scanner = self._create_window_scanner()
        self._app_config = self._create_app_config()
        self._data_manager = self._create_data_manager()
        self._commands_service = self._create_commands_service()
        self._hotkey_manager = self._create_hotkey_manager()
        self._window_manager = self._create_window_manager()
        self._ui_manager = self._create_ui_manager()
        self._tray = self._create_tray()

        self._connect_events()


    def _connect_events(self):
        eventBus.requestRestartApplication.connect(self.restart_application)
        eventBus.requestQuitApplication.connect(
            self.quit_application
        )

    def _create_bootstrap(self) -> BootStrap:
        bootstrap: BootStrap = BootStrap()
        bootstrap.ensure_config()

        return bootstrap


    def _create_event_logger(self) -> EventLogger:
        return EventLogger()


    def _create_application(self) -> QApplication:
        application = QApplication(sys.argv)
        application.setQuitOnLastWindowClosed(False)

        return application


    def _create_window_scanner(self) -> WindowScanner:
        return WindowScanner()


    def _create_app_config(self) -> AppConfig:
        app_config = AppConfig(rice_paths.app_config_path)
        return app_config

    
    def _create_data_manager(self) -> DataManager:
        data_manager = DataManager(
            logger=self._logger,
            app_config=self._app_config,
            config_dir=rice_paths.config_dir,
            themes_dir=rice_paths.themes_dir,
            keymap_file=rice_paths.key_map_file,
        )

        return data_manager
        

    def _create_commands_service(self) -> CommandService:
        return CommandService(
            logger=self._logger,
            data_manager=self._data_manager
        )

    def _create_hotkey_manager(self) -> HotKeyManager:
        hotkey_manager = HotKeyManager(self._logger, self._data_manager.key_map)

        return hotkey_manager


    def _create_window_manager(self) -> WindowManager:
        window_manager = WindowManager(
            logger=self._logger,
            window_scanner=self._window_scanner,
            config=self._data_manager.active_config
        )

        return window_manager
        

    def _create_ui_manager(self) -> UIManager:
        ui_manager = UIManager(
            config=self._data_manager.active_config,
            theme=self._data_manager.active_theme,
            window_scanner=self._window_scanner,
            command_service=self._commands_service
        )

        return ui_manager


    def _create_tray(self) -> Tray:
        tray = Tray(command_service=self._commands_service)
        tray.load()

        return tray

    
    def run(self):
        self._logger.log(
            log_type=LogEventType.APPLICATION_START,
            message="Started RiceWM"
        )
        
        self._hotkey_manager.start()
        self._ui_manager.load()

        sys.exit(self._application.exec())
        

    def quit_application(self):
        self._logger.log(
            log_type=LogEventType.APPLICATION_QUIT,
            message="Quiting RiceWM.."
        )
        
        self._bootstrap.delete_cache()
        self._application.quit()


    def restart_application(self):
        self._logger.log(
            log_type=LogEventType.APPLICATION_RESTART,
            message="Restarting RiceWM.."
        )
            
        os.execv(sys.executable, [sys.executable] + sys.argv)
