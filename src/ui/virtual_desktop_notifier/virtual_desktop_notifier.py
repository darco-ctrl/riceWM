from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QVBoxLayout, QWidget

from src.core.config.config import Config
from src.core.theme.theme import Theme
from src.core.theme.virtual_desktop_notifier.styles.label import VirtualDesktopNotifierLabelStyle
from src.core.theme.virtual_desktop_notifier.virtual_desktop_notifier import VirtualDesktopNotiferStyle
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
        layout.addWidget(self.ui.label)
        
        self.show()

    def load_window(self) -> QVBoxLayout:
        style = self.theme.virtual_desktop_notifer

        layout: QVBoxLayout = QVBoxLayout(self)
        # layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        ) 

        self.resize(
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

    def start_timer(self):
        

    def show_notification(self, desktop_name: str):
        style: VirtualDesktopNotifierLabelStyle = (
            self.theme.virtual_desktop_notifer.label
        ) 

        
        self.ui.label.setText(
            f"{style.prefix}{desktop_name}{style.suffix}"
        )
        self.ui.label.repaint()
        self.show()
