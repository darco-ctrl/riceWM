from typing import cast

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.config.config import Config
from src.core.events.event_bus import eventBus
from src.core.theme.theme import Theme
from src.services.window.scanner import WindowScanner
from src.ui.window_search.constructor import PanelConstructor
from src.ui.window_search.search_system.search_manager import SearchManager
from src.ui.window_search.window_item.manager import WinItemManager


class WindowSearch(QWidget):
    def __init__(self, config: Config, theme: Theme, window_scanner: WindowScanner):
        super().__init__()
        self.config: Config = config
        self.theme: Theme = theme

        self.is_visible: bool = False

        self.window_scanner: WindowScanner = window_scanner

        self.root_layout: QVBoxLayout = QVBoxLayout(self)

        self.panel_constructor: PanelConstructor = PanelConstructor(
            config=self.config,
            theme=self.theme,
            root_layout=self.root_layout
        )

        self.main_panel: QWidget = self.create_window()

        self.search_line_edit: QLineEdit = self.create_search_box()

        self.scroller: QScrollArea = QScrollArea()
        self.scroll_container: QWidget = self.panel_constructor.create_list_scroller(
            main_panel=self.main_panel,
            scroll_area=self.scroller
        )

        self.searcher: SearchManager = SearchManager()

        scroller_layout: QVBoxLayout = cast(QVBoxLayout, self.scroll_container.layout())
        self.winitem_manager: WinItemManager = WinItemManager(
            config=self.config,
            theme=self.theme,
            window_scanner=self.window_scanner,
            searcher=self.searcher,
            scroll_area=self.scroller,
            scroller_layout=scroller_layout,
        )
        self.winitem_manager.sync_to_new()

        self.connect_event()

    def connect_event(self):
        _ = eventBus.wspToggleRequested.connect(self.toggle_window)
        _ = eventBus.itemSelectUp.connect(self.on_wsp_select_up)
        _ = eventBus.itemSelectDown.connect(self.on_wsp_select_down)
        _ = eventBus.wspCloseRequested.connect(self.hide_window)
        _ = eventBus.reloadWSPThemeRequested.connect(
            self.reload_theme
        )
        _ = eventBus.wspFocusSelectedWindow.connect(
            self.focus_selected_window
        )
        

    def focus_selected_window(self):

        if not self.is_visible:
            return
        
        self.winitem_manager.focus_selected_window()
        self.hide_window()
        
    def on_wsp_select_up(self):
        if not self.isVisible():
            return

        self.winitem_manager.select_prev()

    def on_wsp_select_down(self):
        if not self.isVisible():
            return

        self.winitem_manager.select_next()

    def key_input(self):
        pass

    def reload_theme(self):
        self.panel_constructor.reapply_theme()
        self.winitem_manager.reapply_theme()
        self.recolor_container()

    def recolor_container(self):
        style = self.theme.window_search.window_item.color_style
        self.scroll_container.setStyleSheet(f"""
        #scrollContainer {{
            background-color: {style.background_color};
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
        self.winitem_manager.hide()

        self.is_visible = False

    def show_window(self):
        self.winitem_manager.sync_to_new()

        self.show()
        self.raise_()
        self.activateWindow()

        self.search_line_edit.setFocus()

        self.is_visible = True

    def create_window(self) -> QWidget:

        config = self.config.window_search
        theme = self.theme.window_search

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )

        window_margin = 12
        screen_width, screen_height = self.get_screen_size()
        window_height = theme.search_box.height + (
            theme.window_item.frame_style.height
            * config.behavior.max_results_shown
        )

        print(f"sw: x={screen_width}, y={screen_height}")

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
        _ = line_edit.textChanged.connect(
            self.on_search_box_changed
        )

        return line_edit

    def on_search_box_changed(self, text: str):
        if not text.strip():
           self.winitem_manager.sync_to(
               windows_info=self.winitem_manager.windows_info
           )
           return
        
        self.searcher.search(
            query=text,
            windows_info=self.winitem_manager.windows_info
        )

    def get_screen_size(self) -> tuple[int, int]:
        screen = QGuiApplication.primaryScreen()
        return screen.size().width(), screen.size().height()

    def start(self):
        print("start")
        for window_info in self.window_scanner.get_windows_info():
            print(f"title: {window_info.title}")
