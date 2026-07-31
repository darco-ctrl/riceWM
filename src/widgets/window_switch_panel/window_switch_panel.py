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
from core.hotkey.event_bus import events
from data.config.data_class import C_WindowSwitchPanel
from data.theme.data_class import T_WindowSwitchPanel, WindowItemFrame
from src.widgets.window_switch_panel.panel_constructor import PanelConstructor
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

        self.panel: PanelConstructor = PanelConstructor(self.theme, self.root_layout)

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

        self.connect_event()

    def connect_event(self):
        events.wspToggleRequested.connect(self.toggle_window)
        events.reloadWSPThemeRequested.connect(self.reload_theme)

    def reload_theme(self):
        print("reloading theme")

    def toggle_window(self):
        if self.isVisible():
            self.hide()

        else:
            self.show()

    def create_window(self) -> QWidget:

        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        window_margin = 12
        screen_width, screen_height = self.get_screen_size()
        window_height = int(screen_height * 0.9)

        position_x = int((screen_width / 2) - (self.config.window_width / 2))
        position_y = int((screen_height / 2) - (window_height / 2))

        self.setFixedWidth(self.config.window_width)
        self.setFixedHeight(window_height)
        self.move(position_x, position_y)

        # Main panel
        main_panel = self.panel.create_panel()
        return main_panel

    def create_search_box(self) -> QLineEdit:
        line_edit = self.panel.create_searchbox()
        line_edit.returnPressed.connect(self.on_search)

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
