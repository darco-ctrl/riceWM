import sys

from PySide6.QtWidgets import QApplication

import src.app.paths as rice_paths
from src.app.bootstrap import BootStrap
from src.config.app_config import AppConfig
from src.core.data_manager import DataManager
from src.core.hotkey.hotkey_mananger import HotKeyManager
from src.ui.manager import UIManager
from src.ui.tray.tray import Tray


class App:
    def __init__(self):
        self.application = self.create_application()
        self.bootstrap = self.create_bootstrap()
        self.app_config = self.create_app_config()
        self.data_manager = self.create_data_manager()
        self.hotkey_manager = self.create_hotkey_manager()
        self.ui_manager = self.create_ui_manager()
        self.tray = self.create_tray()

    def run(self):
        self.bootstrap.ensure_config()
        self.hotkey_manager.start()
        self.ui_manager.load()

        sys.exit(self.application.exec())

    def create_application(self) -> QApplication:
        application = QApplication(sys.argv)
        application.setQuitOnLastWindowClosed(False)

        return application

    def create_bootstrap(self) -> BootStrap:
        bootstrap: BootStrap = BootStrap()

        return bootstrap

    def create_app_config(self) -> AppConfig:
        app_config = AppConfig(rice_paths.app_config_path)
        return app_config

    def create_data_manager(self) -> DataManager:
        data_manager = DataManager(
            app_config=self.app_config,
            config_dir=rice_paths.config_dir,
            themes_dir=rice_paths.themes_dir,
            keybinds_file=rice_paths.key_map_file,
        )

        return data_manager

    def create_hotkey_manager(self) -> HotKeyManager:
        hotkey_manager = HotKeyManager(self.data_manager.key_map)

        return hotkey_manager

    def create_ui_manager(self) -> UIManager:
        ui_manager = UIManager(
            config=self.data_manager.active_config,
            theme=self.data_manager.active_theme
        )

        return ui_manager

    def create_tray(self) -> Tray:
        tray = Tray()
        tray.load()
        tray.quit_action.triggered.connect(self.quit_application)

        return tray

    def quit_application(self):
        self.bootstrap.delete_cache()
        self.application.quit()
