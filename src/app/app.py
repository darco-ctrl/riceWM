import os
import sys

from pympler import asizeof
from PySide6.QtWidgets import QApplication

import src.app.paths as rice_paths
from src.app.bootstrap import BootStrap
from src.config.app_config import AppConfig
from src.core.data_manager import DataManager
from src.core.events.event_bus import eventBus
from src.core.hotkey.hotkey_mananger import HotKeyManager
from src.services.window.listner import WindowListener
from src.services.window.scanner import WindowScanner
from src.ui.tray.tray import Tray
from src.ui.ui_manager import UIManager
from src.wm.manager import WindowManager


class App:
    def __init__(self):
        self.bootstrap = self.create_bootstrap()
        self.application = self.create_application()
        self.window_listner = self.create_window_listner()
        self.window_scanner = self.create_window_scanner()
        self.app_config = self.create_app_config()
        self.data_manager = self.create_data_manager()
        self.hotkey_manager = self.create_hotkey_manager()
        self.window_manager = self.create_window_manager()
        self.ui_manager = self.create_ui_manager()
        self.tray = self.create_tray()

        self.connect_events()
        self.print_theme_size()

    def connect_events(self):
        eventBus.requestRestartApplication.connect(self.restart_application)

    def run(self):
        self.hotkey_manager.start()
        self.ui_manager.load()

        sys.exit(self.application.exec())

    def create_window_listner(self) -> WindowListener:
        listner = WindowListener()
        return listner

    def create_window_scanner(self) -> WindowScanner:
        return WindowScanner()

    def create_window_manager(self) -> WindowManager:
        window_manager = WindowManager(self.window_scanner)

        return window_manager

    def create_application(self) -> QApplication:
        application = QApplication(sys.argv)
        application.setQuitOnLastWindowClosed(False)

        return application

    def create_bootstrap(self) -> BootStrap:
        bootstrap: BootStrap = BootStrap()
        bootstrap.ensure_config()

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
            theme=self.data_manager.active_theme,
            window_scanner=self.window_scanner
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

    def print_theme_size(self):
        print(f"Theme uses {asizeof.asizeof(
            self.data_manager.active_theme
        ) / 1024:.2f} KB")

    def restart_application(self):
        print("restarting application")
        os.execv(sys.executable, [sys.executable] + sys.argv)
