from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QSize, Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QVBoxLayout, QWidget
from pyvda.pyvda import VirtualDesktop

from src.core.config.config import Config
from src.core.config.models import Animation, AnimationConfig, VirtualDesktopNotifierConfig
from src.core.events.event_bus import eventBus
from src.core.theme.theme import Theme
from src.ui.virtual_desktop_notifier.constructor import NotiferConstructor
from src.ui.virtual_desktop_notifier.model import VirtualDesktopNotiferUI
from src.wm import desktop


class VirtualDesktopNotifier(QWidget):
    def __init__(self, theme: Theme, config: Config):
        super().__init__()

        self.ui: VirtualDesktopNotiferUI
        self.theme: Theme = theme
        self.config: Config = config

        self.timer: QTimer = self.get_timer()

        self.fade_out_animation: QPropertyAnimation = (
            self.get_fade_out_animation()
        )
        self.fade_in_animation: QPropertyAnimation = (
            self.get_fade_in_animation()
        )
        
        self.constructor: NotiferConstructor = NotiferConstructor(
            theme=self.theme
        )

        self.connect_events()
        self.load()

    def connect_events(self):
        eventBus.vDesktopNotiferShow.connect(self.show_notifier)

    def load(self):
        layout = self.load_window()

        self.ui = self.constructor.get_ui()
        layout.addWidget(self.ui.label)
        
        # self.show()

    def get_timer(self) -> QTimer:
        timer: QTimer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(self.hide_window)

        return timer

    def get_fade_out_animation(self) -> QPropertyAnimation:
        config: Animation = self.config.virtual_destkop_notifer.animation.fade_out
        
        animation: QPropertyAnimation = QPropertyAnimation(
            self, b"windowOpacity"
        )
        animation.setDuration(config.duration)
        animation.setLoopCount(1)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        animation.finished.connect(self.finished_fade_out)
        return animation

    def get_fade_in_animation(self) -> QPropertyAnimation:
        config: Animation = self.config.virtual_destkop_notifer.animation.fade_in
        
        animation: QPropertyAnimation = QPropertyAnimation(
            self, b"windowOpacity"
        )
        animation.setDuration(config.duration)
        animation.setLoopCount(1)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        animation.finished.connect(self.finished_fade_in)
        
        return animation

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
        style: VirtualDesktopNotifierConfig = self.config.virtual_destkop_notifer

        print("Timer Started")
        self.timer.start(style.auto_hide_time)

    def finished_fade_out(self):
        self.fade_out_animation.stop()
        self.hide()

    def finished_fade_in(self):
        self.fade_in_animation.stop()

    def hide_window(self):
        print("Hiding window")
        self.timer.stop()
        self.fade_out_animation.start()

    def show_window(self):
        self.show()
        self.fade_in_animation.start()

    def show_notifier(self, desktop: VirtualDesktop):
        style: VirtualDesktopNotifierConfig = (
            self.config.virtual_destkop_notifer
        )

        desktop_name: str = desktop.name
        display_name: str
        if not desktop_name or desktop_name.isspace():
            display_name = f"Desktop {desktop.number}"
        else:
            display_name = desktop_name
        
        self.ui.label.setText(
            f"{
                style.desktop_name.prefix
            }{display_name}{
                style.desktop_name.suffix
            }"
        )
        self.ui.label.repaint()
        self.start_timer()
        self.show_window()
