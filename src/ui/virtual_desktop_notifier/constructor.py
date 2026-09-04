from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from src.core.theme.theme import Theme
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

        return VirtualDesktopNotiferUI(
            label=label
        )

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
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setText("hello world")
        return label
