

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QWidget

from src.ui.virtual_desktop_notifier.model import VirtualDesktopNotiferUI


class VirtualDesktopNotifier(QWidget):
    def __init__(self):
        super().__init__()

        self.ui: VirtualDesktopNotiferUI

    def load(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )

    def reload(self):
        pass
