from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLineEdit, QSizePolicy, QVBoxLayout, QWidget

from src.data.theme.theme import T_WindowSwitchPanel
from src.widgets.window_switch_panel.widgets import Panel, SearchBox


class PanelConstructor:
    def __init__(self, theme: T_WindowSwitchPanel, root_layout: QVBoxLayout) -> None:
        self.theme = theme
        self.root_layout: QVBoxLayout = root_layout

        self.panel: Panel
        self.search_box: SearchBox

    def create_panel(self) -> QWidget:

        panel = QWidget()

        # main_panel.setFixedHeight(100)

        # Main panel layout
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)
        self.root_layout.addWidget(panel)

        self.panel = Panel(widget=panel, layout=layout)

        self.color_panel()
        return panel

    def color_panel(self):
        self.panel.widget.setStyleSheet(f"""
            background-color: {self.theme.background_color};
        """)

    def create_searchbox(self) -> QLineEdit:
        container = QWidget()

        layout = QVBoxLayout(container)
        layout.setSpacing(0)

        line_edit = QLineEdit()

        # line_edit.setFixedHeight(self.theme.search_box.height)

        size_policy = line_edit.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
        line_edit.setSizePolicy(size_policy)

        layout.addWidget(line_edit)
        self.panel.layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignTop)

        self.search_box = SearchBox(
            container=container, layout=layout, line_edit=line_edit
        )

        self.color_search_box()
        return line_edit

    def color_search_box(self):

        self.search_box.container.setFixedHeight(self.theme.search_box.height)

        self.search_box.container.setStyleSheet(f"""
            background-color: {self.theme.search_box.background_color};
        """)

        self.search_box.layout.setContentsMargins(
            self.theme.search_box.line_edit.margin[0],
            self.theme.search_box.line_edit.margin[1],
            self.theme.search_box.line_edit.margin[2],
            self.theme.search_box.line_edit.margin[3],
        )

        self.search_box.line_edit.setStyleSheet(
            self.theme.search_box.line_edit.to_style_sheet()
        )

        self.search_box.line_edit.setTextMargins(
            self.theme.search_box.line_edit.text_margin[0],
            self.theme.search_box.line_edit.text_margin[1],
            self.theme.search_box.line_edit.text_margin[2],
            self.theme.search_box.line_edit.text_margin[3],
        )

        font = self.theme.search_box.line_edit.font.to_qfont(
            self.search_box.line_edit.font()
        )
        self.search_box.line_edit.setFont(font)
