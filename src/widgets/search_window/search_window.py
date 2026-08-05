from typing import cast

from PySide6.QtCore import QEvent, QSize, Qt, QVersionNumber, QWaitCondition
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

import src.app.paths as rice_paths
from src.core.config.config import Config
from src.core.events.event_bus import events
from src.core.theme.theme import Theme
from src.widgets.search_window.item import WindowItem
from src.widgets.search_window.item_builder import ItemBuilder
from src.widgets.search_window.panel_builder import PanelBuilder
from src.widgets.search_window.search import TitleSearcher
from src.services.window_scanner import WindowScanner


class SearchWindow(QWidget):
    def __init__(self, config: Config, theme: Theme):
        super().__init__()
        self.config = config
        self.theme = theme

        self.window_scanner = WindowScanner()

        self.root_layout = QVBoxLayout(self)

        self.panel_constructor = PanelBuilder(self.theme, self.root_layout)

        self.main_panel: QWidget = self.create_window()

        self.search_line_edit: QLineEdit = self.create_search_box()
        self.scroll_container: QWidget = self.create_list_scroller()

        self.window_items: list[WindowItem] = []
        self.focus_window_item: WindowItem | None = None
        self.selected_window_item: WindowItem | None = None

        self.title_searcher = TitleSearcher()

        self.item_builder = ItemBuilder(
            config=self.config,
            theme=self.theme,
            scroller_widget=self.scroll_container,
            window_scanner=self.window_scanner,
        )
        self.item_builder.sync_window_items(window_items=self.window_items)

        self.connect_event()

    def connect_event(self):
        events.wspToggleRequested.connect(self.toggle_window)
        events.reloadWSPThemeRequested.connect(self.reload_theme)

    def reload_theme(self):

        self.panel_constructor.reapply_theme()
        self.item_builder.reapply_theme(self.window_items)
        self.recolor_container()

    def recolor_container(self):
        container_style = self.theme.window_switch_panel.window_item_container
        self.scroll_container.setStyleSheet(f"""
        #scrollContainer {{
            background-color: {container_style.background_color};
        }}
        """)

    def toggle_window(self):
        if self.isVisible():
            self.hide_window()

        else:
            self.show_window()

    def event(self, event):

        if event.type() == QEvent.Type.WindowDeactivate:
            self.hide_window()

        return super().event(event)

    def hide_window(self):
        self.hide()
        self.search_line_edit.setText("")

    def show_window(self):
        self.item_builder.sync_window_items(self.window_items)

        self.show()
        self.raise_()
        self.activateWindow()

        self.search_line_edit.setFocus()

    def create_window(self) -> QWidget:

        config = self.config.window_switch_panel
        theme = self.theme.window_switch_panel

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )

        window_margin = 12
        screen_width, screen_height = self.get_screen_size()
        window_height = theme.search_box.height + (
            theme.window_item_container.item_frame.height
            * config.behavior.max_results_shown
        )

        position_x = int((screen_width / 2) - (config.window_width / 2))
        position_y = int((screen_height / 2) - (window_height / 2))

        self.setFixedWidth(config.window_width)
        self.setFixedHeight(window_height)
        self.move(position_x, position_y)

        # Main panel
        main_panel = self.panel_constructor.create_panel()
        return main_panel

    def create_search_box(self) -> QLineEdit:
        line_edit = self.panel_constructor.create_searchbox()
        line_edit.returnPressed.connect(self.on_search)

        return line_edit

    def create_list_scroller(self) -> QWidget:
        container_style = self.theme.window_switch_panel.window_item_container

        panel_layout: QVBoxLayout = cast(QVBoxLayout, self.main_panel.layout())

        scroll: QScrollArea = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container: QWidget = QWidget()
        container.setObjectName("scrollContainer")

        layout: QVBoxLayout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)

        container.setStyleSheet(f"""
        #scrollContainer {{
            background-color: {container_style.background_color};
        }}
        """)

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
