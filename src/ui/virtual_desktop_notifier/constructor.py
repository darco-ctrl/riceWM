from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from src.core.theme.theme import Theme, VirtualDesktopNotiferStyle
from src.core.theme.virtual_desktop_notifier.styles.frame import (
    VirtualDesktopNotifierFrameStyle,
)
from src.core.theme.virtual_desktop_notifier.styles.label import (
    VirtualDesktopNotifierLabelStyle,
)
from src.ui.virtual_desktop_notifier.model import VirtualDesktopNotiferUI
from src.ui.virtual_desktop_notifier.theme_applier import NotifierThemeApplier


class NotiferConstructor:
    def __init__(self, theme: Theme):
        self.theme = theme
        self.theme_applier:NotifierThemeApplier = NotifierThemeApplier(
            theme=self.theme
        )

    def get_ui(self) -> VirtualDesktopNotiferUI:

        label: QLabel = self.get_label()
        frame: QFrame = self.get_frame(label)

        return VirtualDesktopNotiferUI(
            frame=frame,
            label=label
        )

    def get_frame(self, label: QLabel) -> QFrame:
        style: VirtualDesktopNotifierFrameStyle = (
            self.theme.virtual_desktop_notifer.frame
        )

        frame: QFrame = QFrame()
        layout: QHBoxLayout = QHBoxLayout(frame)

        frame.setContentsMargins(
            style.margin[0],
            style.margin[1],
            style.margin[2],
            style.margin[3],
        )
        
        self.theme_applier.set_frame_style(frame=frame)

        layout.addWidget(label)

        return frame

    def get_label(self) -> QLabel:
        style: VirtualDesktopNotifierLabelStyle = (
            self.theme.virtual_desktop_notifer.label
        )
        
        label: QLabel = QLabel()
        label.setObjectName("VDesktopNotifierLabel")

        label.setContentsMargins(
            style.text_margin[0],
            style.text_margin[1],
            style.text_margin[2],
            style.text_margin[3]
        )

        self.theme_applier.set_label_style(label=label)
        return label
