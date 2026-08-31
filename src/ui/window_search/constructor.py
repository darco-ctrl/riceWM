from typing import cast

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLineEdit, QScrollArea, QSizePolicy, QVBoxLayout, QWidget

from src.core.config.config import Config
from src.core.theme.theme import Theme
from src.ui.window_search.widgets import Panel, SearchBox


class PanelConstructor:
    def __init__(self, config: Config, theme: Theme, root_layout: QVBoxLayout) -> None:
        self.config: Config = config
        self.theme: Theme = theme
        self.root_layout: QVBoxLayout = root_layout

        self.panel: Panel
        self.search_box: SearchBox

    def create_list_scroller(self, main_panel: QWidget) -> QWidget:
        style = self.theme.window_search.window_item.color_style

        panel_layout: QVBoxLayout = cast(QVBoxLayout, main_panel.layout())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        container: QWidget = QWidget()
        container.setObjectName("scrollContainer")

        layout: QVBoxLayout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)

        container.setStyleSheet(f"""
        #scrollContainer {{
            background-color: {style.background_color};
        }}
        """)

        scroll.setWidget(container)

        panel_layout.addWidget(scroll)

        return container

    def reapply_theme(self):
        self.color_panel()
        self.color_search_box()

    def create_panel(self) -> QWidget:

        panel = QWidget()
        panel.setObjectName("Panel")

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
        style = self.theme.window_search.color_style

        self.panel.widget.setStyleSheet(f"""
        #Panel {{
            background-color: {style.background_color};
        }}
        """)

    def create_searchbox(self) -> QLineEdit:
        container = QWidget()
        container.setObjectName("searchBox")

        layout = QVBoxLayout(container)
        layout.setSpacing(0)

        line_edit = QLineEdit()
        line_edit.setObjectName("lineEdit")

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
        style = self.theme.window_search.search_box

        self.search_box.container.setFixedHeight(style.height)

        self.search_box.container.setStyleSheet(f"""
        #searchBox {{
            background-color: {style.color_style.background_color};
        }}
        """)

        self.search_box.layout.setContentsMargins(
            style.line_edit.margin[0],
            style.line_edit.margin[1],
            style.line_edit.margin[2],
            style.line_edit.margin[3],
        )

        line_edit_style = self.theme.helper.get_line_edit_style(
            style=style.line_edit
        )
        self.search_box.line_edit.setStyleSheet(f"""#lineEdit {{
            {line_edit_style}
        }}""")

        self.search_box.line_edit.setPlaceholderText(
            self.config.window_search.search_box.placeholder_text
        )

        self.search_box.line_edit.setTextMargins(
            style.line_edit.text_margin[0],
            style.line_edit.text_margin[1],
            style.line_edit.text_margin[2],
            style.line_edit.text_margin[3],
        )

        font = self.theme.helper.to_qfont(
            qfont=self.search_box.line_edit.font(),
            font_style=style.line_edit.font_style
        )
        self.search_box.line_edit.setFont(font)
