

from src.core.theme.theme import Theme
from src.core.theme.virtual_desktop_notifier.styles.frame import VirtualDesktopNotifierFrameStyle
from src.core.theme.virtual_desktop_notifier.styles.label import VirtualDesktopNotifierLabelStyle
from src.ui.virtual_desktop_notifier.model import QFrame, QLabel


class NotifierThemeApplier:
    def __init__(self, theme: Theme):
        self.theme = theme

    def set_frame_style(self, frame: QFrame):

        style: VirtualDesktopNotifierFrameStyle = (
            self.theme.virtual_desktop_notifer.frame
        ) 

        frame.setStyleSheet(f"""
        #VDesktopNotiferFrame {{
            background-color: {style.color_style.background_color};
            border-style: {style.border_style.style};
            border-radius: {style.border_style.radius}px;
            border-left-width: {style.border_style.width[0]}px;
            border-top-width: {style.border_style.width[1]}px;
            border-right-width: {style.border_style.width[2]}px;
            border-bottom-width: {style.border_style.width[3]}px;
            border-color: {style.border_style.color};
        }}
        """)

    def set_label_style(self, label: QLabel):   

        style: VirtualDesktopNotifierLabelStyle = (
            self.theme.virtual_desktop_notifer.label
        )

        label.setStyleSheet(f"""
        #VDesktopNotifierLabel {{
            background-color: {style.color_style.background_color};
            color: {style.color_style.color};
            border-style: {style.border_style.style};
            border-radius: {style.border_style.radius}px;
            border-left-width: {style.border_style.width[0]}px;
            border-top-width: {style.border_style.width[1]}px;
            border-right-width: {style.border_style.width[2]}px;
            border-bottom-width: {style.border_style.width[3]}px;
            border-color: {style.border_style.color};
        }}
        """)

        q_font = self.theme.helper.to_qfont(
            font_style=style.font_style,
            qfont=label.font()
        )
        label.setFont(q_font)
