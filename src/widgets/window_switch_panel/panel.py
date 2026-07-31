from PySide6.QtWidgets import QVBoxLayout, QWidget

from src.data.theme.theme import T_WindowSwitchPanel


class Panel:
    def __init__(self, theme: T_WindowSwitchPanel, root_layout: QVBoxLayout) -> None:
        self.theme = theme
        self.root_layout: QVBoxLayout = root_layout

        self.panel: QWidget

    def create_panel(self) -> QWidget:

        self.panel = QWidget()

        # main_panel.setFixedHeight(100)

        # Main panel layout
        layout = QVBoxLayout(self.panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)
        self.root_layout.addWidget(self.panel)

        self.color_panel()
        return self.panel

    def color_panel(self):
        self.panel.setStyleSheet(f"""
            background-color: {self.theme.background_color};
        """)
