import sys

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon


class Tray:
    def __init__(self) -> None:
        self.tray_icon: QSystemTrayIcon
        self.menu: QMenu

        self.quit_action: QAction

    def load(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            sys.exit(1)

        self.tray_icon = QSystemTrayIcon(QIcon("assets/rice.png"))
        self.tray_icon.setToolTip("Rice")

        self.menu = QMenu()

        self.quit_action = QAction("Quit")

        self.menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()
