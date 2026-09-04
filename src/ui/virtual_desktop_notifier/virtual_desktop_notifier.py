from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from src.core.config.config import Config
from src.core.theme.primitives.dimension import Dimension
from src.core.theme.theme import Theme
from src.core.theme.virtual_desktop_notifier.virtual_desktop_notifier import (
    VirtualDesktopNotiferStyle,
)
from src.ui.virtual_desktop_notifier.constructor import NotiferConstructor
from src.ui.virtual_desktop_notifier.model import VirtualDesktopNotiferUI


class VirtualDesktopNotifier(QWidget):
    def __init__(self, theme: Theme, config: Config):
        super().__init__()

        self.ui: VirtualDesktopNotiferUI
        self.theme: Theme = theme

        self.constructor: NotiferConstructor = NotiferConstructor(
            theme=self.theme
        )

        self.load()


    def load(self):
        layout = self.load_window()

        self.ui = self.constructor.get_ui()
        layout.addWidget(self.ui.frame)

        self.show()

    def load_window(self) -> QHBoxLayout:
        style = self.theme.virtual_desktop_notifer

        layout: QHBoxLayout = QHBoxLayout(self)
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )

        self.setFixedSize(
            QSize(style.size.x, style.size.y)
        )

        screen_size: tuple[int, int] = self.get_screen_size()
        print(f"screen_size: x={screen_size[0]}, y={screen_size[1]}.")

        pos_x: int = int(
            ((style.position.x / 100) * screen_size[0]) -
            (style.size.x / 2)
        )
        pos_y: int = int(
            ((style.position.y / 100) * screen_size[1]) -
            (style.size.y / 2)
        )
        
        print(f"pos: x={pos_x}, y={pos_y}.")

        self.move(
            pos_x,
            pos_y
        )

        return layout

    def get_screen_size(self) -> tuple[int, int]:
        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        return size.width(), size.height()

    def reload(self):
        pass
