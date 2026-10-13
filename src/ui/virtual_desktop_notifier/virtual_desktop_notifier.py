from PySide6.QtCore import QEasingCurve, QEvent, QPropertyAnimation, QSize, Qt, QTimer
from PySide6.QtGui import QEnterEvent, QGuiApplication
from PySide6.QtWidgets import QVBoxLayout, QWidget
from pyvda.pyvda import VirtualDesktop

from src.core.config.config import Config
from src.core.config.models import (
    Animation,
    VirtualDesktopNotifierConfig,
)
from src.core.events.event_bus import eventBus
from src.core.theme.theme import Theme
from src.ui.virtual_desktop_notifier.constructor import NotiferConstructor
from src.ui.virtual_desktop_notifier.model import VirtualDesktopNotiferUI


class VirtualDesktopNotifier(QWidget):
    def __init__(self, theme: Theme, config: Config):
        super().__init__()

        self._ui: VirtualDesktopNotiferUI
        self._theme: Theme = theme
        self._config: Config = config
        self._label_text: str = ""
        self._timer: QTimer = self._get_timer()
        self._constructor = NotiferConstructor(self._theme)
        
        self._setup_animations()
        self._connect_events()
        self.load()

    def _setup_animations(self):
        vdn_style: VirtualDesktopNotifierConfig = (
            self._config.virtual_desktop.notifier
        )
        window_animation = vdn_style.window_animation
        
        self.fade_out_animation: QPropertyAnimation = (
            self._get_fade_out_animation(config=window_animation.fade_out)
        )
        self.fade_out_animation.finished.connect(self._on_window_fade_out)
        
        self.fade_in_animation: QPropertyAnimation = (
            self._get_fade_in_animation(config=window_animation.fade_in)
        )
        self.fade_in_animation.finished.connect(self._on_window_fade_in)
        
    def _connect_events(self):
        eventBus.vDesktopNotiferShow.connect(self._show_notifier)


    def _get_timer(self) -> QTimer:
        timer: QTimer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(self._hide_window)

        return timer


    def _get_fade_out_animation(self, config: Animation) -> QPropertyAnimation:
        
        animation: QPropertyAnimation = QPropertyAnimation(
            self, b"windowOpacity"
        )
        animation.setDuration(config.duration)
        animation.setLoopCount(1)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        return animation


    def _get_fade_in_animation(self, config: Animation) -> QPropertyAnimation:
        
        animation: QPropertyAnimation = QPropertyAnimation(
            self, b"windowOpacity"
        )
        animation.setDuration(config.duration)
        animation.setLoopCount(1)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        
        return animation


    def _load_window(self) -> QVBoxLayout:
        style = self._theme.virtual_desktop_notifer

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

        screen_size: tuple[int, int] = self._get_screen_size()

        pos_x: int = int(
            ((style.position.x / 100) * screen_size[0]) -
            (style.size.x / 2)
        )
        pos_y: int = int(
            ((style.position.y / 100) * screen_size[1]) -
            (style.size.y / 2)
        )

        self.move(
            pos_x,
            pos_y
        )
        self.setMouseTracking(True)

        return layout


    def _get_screen_size(self) -> tuple[int, int]:
        screen = QGuiApplication.primaryScreen()
        size = screen.size()
        return size.width(), size.height()


    def _start_timer(self):
        style: VirtualDesktopNotifierConfig = self._config.virtual_desktop.notifier

        self._timer.start(style.auto_hide_time)


    def _on_window_fade_out(self):
        self.fade_out_animation.stop()
        self.hide()


    def _on_window_fade_in(self):
        self.fade_in_animation.stop()


    def _hide_window(self):
        self._timer.stop()
        self.fade_out_animation.start()


    def _show_window(self):
        if self.fade_out_animation.state() == QPropertyAnimation.State.Running:
            self.fade_out_animation.stop()
    
        if self.isVisible() and self.windowOpacity() >= 1.0:
            return
            
        self.show()
        self.fade_in_animation.start()


    def _update_label(self):
        style: VirtualDesktopNotifierConfig = (
            self._config.virtual_desktop.notifier
        )
        
        self._ui.label.setText(
            f"{
                style.desktop_name.prefix
            }{self._label_text}{
                style.desktop_name.suffix
            }"
        )
        self._ui.label.repaint()


    def _enterEvent(self, event: QEnterEvent) -> None:
        if self._config.virtual_desktop.notifier.hide_on_hover:
            self._hide_window()
            
        super().enterEvent(event)


    def _leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        
    
    def _show_notifier(self, desktop: VirtualDesktop):

        desktop_name: str = desktop.name
        display_name: str
        if not desktop_name or desktop_name.isspace():
            display_name = f"Desktop {desktop.number}"
        else:
            display_name = desktop_name

        self._label_text = display_name

        self._update_label()
        self._start_timer()
        self._show_window()


    def load(self):
        layout = self._load_window()

        self._ui = self._constructor.get_ui()
        layout.addWidget(self._ui.label)
