import sys

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

import app.bootstrap as bootstrap
import app.paths as rice_paths
from config.app_config import AppConfig
from data.data_manager import DataManager
from widgets.widget_manager import WidgetManager


def ensure_config():
    bootstrap.ensure_config()


def on_exit():
    bootstrap.delete_cache()


def main():

    application = QApplication(sys.argv)
    # application.setQuitOnLastWindowClosed(False)

    def quit_application():
        on_exit()
        application.quit()

    ensure_config()

    # Create AppConfig after config is ensured
    app_config = AppConfig(rice_paths.app_config_path)

    # Create ThemeManager with AppConfig and apply theme
    data_manager = DataManager(
        app_config=app_config,
        config_dir=rice_paths.config_dir,
        themes_dir=rice_paths.themes_dir,
    )

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
