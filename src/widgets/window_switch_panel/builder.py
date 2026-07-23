from PySide6.QtCore import QSize
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLayout, QVBoxLayout, QWidget

from src.data.config.data_class import C_WindowSwitchPanel
from src.data.theme.data_class import T_WindowSwitchPanel, WindowItemFrame


class Builder:
    def __init__(self, theme: T_WindowSwitchPanel, config: C_WindowSwitchPanel) -> None:
        self.theme = theme
        self.config = config

    def create_item_frame(self, layout: QVBoxLayout) -> QFrame:
        frame_style: WindowItemFrame = self.theme.window_item_frame

        frame = QFrame()
        frame.setFixedHeight(frame_style.height)

        frame_layout: QHBoxLayout = QHBoxLayout(frame)
        frame_layout.setContentsMargins(
            frame_style.contents_margin[0],
            frame_style.contents_margin[1],
            frame_style.contents_margin[2],
            frame_style.contents_margin[3],
        )
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        frame.setStyleSheet(f"""
            background-color: {frame_style.background_color};
            """)
        return frame

    def create_selection_indicator(self):
        style = self.theme.window_item_frame.selection_indicator

        indicator: QWidget = QWidget()
        indicator.setFixedSize(QSize(style.width, style.height))
        indicator.setStyleSheet(f"""
            background-color: {style.background_color};
        """)

        return indicator
