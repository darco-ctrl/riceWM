import sys

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

import src.app.paths as rice_paths
from services.commands.command_service import CommandService


class Tray:
    def __init__(self, command_service: CommandService) -> None:
        self._command_service = command_service
        self._tray_icon: QSystemTrayIcon
        self._menu: QMenu

        self._quit_action: QAction

    def load(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            sys.exit(1)

        self._tray_icon = QSystemTrayIcon(
            QIcon(str(rice_paths.rice_icon))
        )
        self._tray_icon.setToolTip("Rice")

        self._menu = QMenu()

        self._open_config_folder = QAction ("Open Config Folder")
        self._open_app_config = QAction("Open App Config")
        self._open_theme = QAction("Open Theme")
        self._open_config = QAction("Open Config")
        self._restart = QAction("Restart")
        self._quit_action = QAction("Quit")

        self._menu.addAction(self._open_config_folder)
        self._menu.addAction(self._open_app_config)
        self._menu.addAction(self._open_theme)
        self._menu.addAction(self._open_config)
        self._menu.addSeparator()
        self._menu.addAction(self._restart)
        self._menu.addAction(self._quit_action)

        self._connect_actions()
    
        self._tray_icon.setContextMenu(self._menu)
        self._tray_icon.show()

    def _connect_actions(self):
        self._open_config_folder.triggered.connect(
            lambda: self._command_service.execute(command=":open-config-folder")
        )
        self._open_app_config.triggered.connect(
            lambda: self._command_service.execute(command=":open-app-config")
        )
        self._open_theme.triggered.connect(
            lambda: self._command_service.execute(command=":open-theme")
        )
        self._open_config.triggered.connect(
            lambda: self._command_service.execute(command=":open-config")
        )
        self._restart.triggered.connect(
            lambda: self._command_service.execute(command=":restart")
        )
        self._quit_action.triggered.connect(
            lambda: self._command_service.execute(command=":quit")
        )
