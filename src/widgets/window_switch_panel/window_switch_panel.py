from typing import cast

from PySide6.QtCore import QSize, Qt, QVersionNumber, QWaitCondition
from PySide6.QtGui import QFont, QGuiApplication, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

import app.paths as rice_paths
from data.config.data_class import C_WindowSwitchPanel
from data.theme.data_class import T_WindowSwitchPanel, WindowItemFrame
from widgets.window_switch_panel.builder import Builder
from widgets.window_switch_panel.search import TitleSearcher
from widgets.window_switch_panel.window_item import WindowItem
from windows.window_manager import WindowManager
from windows.window_scanner import WindowScanner


class WindowSwitchPanelWidget(QWidget):
    def __init__(self, config: C_WindowSwitchPanel, theme: T_WindowSwitchPanel):
        super().__init__()
        self.config = config
        self.theme = theme

        self.window_scanner = WindowScanner()

        self.root_layout = QVBoxLayout(self)

        self.main_panel: QWidget = self.create_window()

        self.search_line_edit: QLineEdit = self.create_search_box()
        self.scroll_container: QWidget = self.create_list_scroller()

        self.window_items: list[WindowItem] = []

        self.title_searcher = TitleSearcher()

        self.builder = Builder(
            config=self.config,
            theme=self.theme,
            scroller_widget=self.scroll_container,
            window_scanner=self.window_scanner,
        )
        self.builder.sync_window_items(window_items=self.window_items)

    def create_window(self) -> QWidget:

        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        window_margin = 12

        screen_width, screen_height = self.get_screen_size()

        window_height = int(screen_height * 0.9)

        position_x = int((screen_width / 2) - (self.theme.window_width / 2))
        position_y = int((screen_height / 2) - (window_height / 2))

        self.setFixedWidth(self.theme.window_width)
        self.setFixedHeight(window_height)
        self.move(position_x, position_y)

        # Main panel
        main_panel = QWidget()

        main_panel.setStyleSheet(f"""
            background-color: {self.theme.background_color};
        """)

        # main_panel.setFixedHeight(100)

        # Main panel layout
        main_panel_layout = QVBoxLayout(main_panel)
        main_panel_layout.setContentsMargins(0, 0, 0, 0)
        main_panel_layout.setSpacing(0)

        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)
        self.root_layout.addWidget(main_panel)

        return main_panel

    def create_search_box(self) -> QLineEdit:
        panel_layout: QVBoxLayout = cast(QVBoxLayout, self.main_panel.layout())

        if not panel_layout:
            return

        container = QWidget()

        container.setFixedHeight(self.theme.search_box.height)

        container.setStyleSheet(f"""
            background-color: {self.theme.search_box.background_color};
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(
            self.theme.search_box.line_edit.margin[0],
            self.theme.search_box.line_edit.margin[1],
            self.theme.search_box.line_edit.margin[2],
            self.theme.search_box.line_edit.margin[3],
        )
        layout.setSpacing(0)

        line_edit = QLineEdit()

        # line_edit.setFixedHeight(self.theme.search_box.height)

        size_policy = line_edit.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
        line_edit.setSizePolicy(size_policy)

        line_edit.setStyleSheet(self.theme.search_box.line_edit.to_style_sheet())

        line_edit.setTextMargins(
            self.theme.search_box.line_edit.text_margin[0],
            self.theme.search_box.line_edit.text_margin[1],
            self.theme.search_box.line_edit.text_margin[2],
            self.theme.search_box.line_edit.text_margin[3],
        )

        font = self.theme.search_box.line_edit.font.to_qfont(line_edit.font())
        line_edit.setFont(font)

        line_edit.returnPressed.connect(self.on_search)

        layout.addWidget(line_edit)
        panel_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignTop)

        return line_edit

    def create_list_scroller(self) -> QWidget:
        panel_layout: QVBoxLayout = cast(QVBoxLayout, self.main_panel.layout())

        scroll: QScrollArea = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container: QWidget = QWidget()
        layout: QVBoxLayout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)

        container.setStyleSheet("background-color: blue;")

        scroll.setWidget(container)

        panel_layout.addWidget(scroll)

        return container

    def on_search(self):

        query = self.search_line_edit.text()
        self.title_searcher.search(query)

    def get_screen_size(self) -> tuple[int, int]:
        screen = QGuiApplication.primaryScreen()
        return screen.size().width(), screen.size().height()

    def start(self):
        print("start")
        for window_info in self.window_scanner.get_windows_info():
            print(f"title: {window_info.title}")

        self.show()
