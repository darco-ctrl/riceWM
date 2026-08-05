import sys

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

import src.app.paths as rice_paths
from src.app.bootstrap import BootStrap
from src.config.app_config import AppConfig
from src.core.hotkey.hotkey_mananger import HotKeyManager
from src.data.data_manager import DataManager
from src.widgets.widget_manager import WidgetManager


def main():

    bootstrap: BootStrap = BootStrap()

    application = QApplication(sys.argv)
    application.setQuitOnLastWindowClosed(False)

    def quit_application():
        bootstrap.delete_cache()
        application.quit()

    bootstrap.ensure_config()

    # Create AppConfig after config is ensured
    app_config = AppConfig(rice_paths.app_config_path)

    # Create ThemeManager with AppConfig and apply theme
    data_manager = DataManager(
        app_config=app_config,
        config_dir=rice_paths.config_dir,
        themes_dir=rice_paths.themes_dir,
        keybinds_file=rice_paths.key_map_file,
    )

    hotkey_manager = HotKeyManager(data_manager.key_map)
    hotkey_manager.start()

    # Create WidgetManager with theme and show widgets
    widget_manager = WidgetManager(
        config=data_manager.active_config, theme=data_manager.active_theme
    )
    widget_manager.show_widgets()

    # Create system tray icon
    if not QSystemTrayIcon.isSystemTrayAvailable():
        sys.exit(1)

    tray_icon = QSystemTrayIcon(QIcon("assets/rice.png"))
    tray_icon.setToolTip("Rice")

    menu = QMenu()

    open_settings_action = QAction("Settings")
    quit_action = QAction("Quit")

    menu.addAction(open_settings_action)
    menu.addAction(quit_action)

    quit_action.triggered.connect(quit_application)

    tray_icon.setContextMenu(menu)

    tray_icon.show()

    sys.exit(application.exec())


def open_settings():
    pass


if __name__ == "__main__":
    main()
