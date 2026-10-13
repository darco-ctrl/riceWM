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
from src.services.commands.command_service import CommandService
from src.services.window.scanner import WindowScanner
from src.ui.window_search.constructor import PanelConstructor
from src.ui.window_search.search_system.search_manager import SearchManager
from src.ui.window_search.window_item.manager import WinItemManager


class WindowSearch(QWidget):
    def __init__(
        self,
        config: Config,
        theme: Theme,
        window_scanner: WindowScanner,
        command_service: CommandService,
    ):
        super().__init__()
    
        self._initialize_dependencies(config, theme, window_scanner, command_service)
        self._initialize_layout()
        self._initialize_window_items()
    
        self._connect_event()
        self.winitem_manager.sync_to_new()
    
    
    def _initialize_dependencies(
        self,
        config: Config,
        theme: Theme,
        window_scanner: WindowScanner,
        command_service: CommandService,
    ) -> None:
        self._config = config
        self._theme = theme
        self._window_scanner = window_scanner
        self._command_service = command_service
        self._searcher = SearchManager()
    
    
    def _initialize_layout(self) -> None:
        self._root_layout = QVBoxLayout(self)
        self._panel_constructor = PanelConstructor(
            config=self._config,
            theme=self._theme,
            root_layout=self._root_layout,
        )
    
        self._main_panel = self._create_window()
        self._search_line_edit = self._create_search_box()
        self._scroller = QScrollArea()
    
        self._scroll_container = self._panel_constructor.create_list_scroller(
            main_panel=self._main_panel,
            scroll_area=self._scroller,
        )
    
    
    def _initialize_window_items(self) -> None:
        scroller_layout = cast(
            QVBoxLayout,
            self._scroll_container.layout(),
        )
    
        self.winitem_manager = WinItemManager(
            config=self._config,
            theme=self._theme,
            window_scanner=self._window_scanner,
            searcher=self._searcher,
            scroll_area=self._scroller,
            scroller_layout=scroller_layout,
        )

        
    def _connect_event(self):
        _ = eventBus.wspToggleRequested.connect(self._toggle_window)
        _ = eventBus.itemSelectUp.connect(self._on_wsp_select_up)
        _ = eventBus.itemSelectDown.connect(self._on_wsp_select_down)
        _ = eventBus.wspCloseRequested.connect(self._hide_window)
        _ = eventBus.reloadWSPThemeRequested.connect(
            self._reload_theme
        )
        

    def _focus_selected_window(self):

        if not self.isVisible():
            return

        if not self.winitem_manager.windows_item:
            return

        text = self._search_line_edit.text()
        
        if text and text[0] == ':':
            return
        
        self.winitem_manager.focus_selected_window()
        self._hide_window()
        
    def _on_wsp_select_up(self):
        if not self.isVisible():
            return

        self.winitem_manager.select_prev()

    def _on_wsp_select_down(self):
        if not self.isVisible():
            return

        self.winitem_manager.select_next()


    def _reload_theme(self):
        self._panel_constructor.reapply_theme()
        self.winitem_manager.reapply_theme()
        self._recolor_container()


    def _recolor_container(self):
        style = self._theme.window_search.window_item.color_style
        self._scroll_container.setStyleSheet(f"""
        #scrollContainer {{
            background-color: {style.background_color};
        }}
        """)


    def _toggle_window(self):
        if self.isVisible():
            self._hide_window()

        else:
            self._show_window()


    def _event(self, event):
        if event.type() == QEvent.Type.WindowDeactivate:
            self._hide_window()

        return super().event(event)


    def _hide_window(self):
        if not self.isVisible():
            return

        eventBus.disablePanelKeys.emit()
        self.hide()
        self._search_line_edit.setText("")
        self.winitem_manager.hide()


    def _show_window(self):
        if self.isVisible():
            return
        
        self.winitem_manager.sync_to_new()

        eventBus.enablePanelKeys.emit()
        self.show()
        self.raise_()
        self.activateWindow()

        self.setFocus()
        self._search_line_edit.setFocus()


    def _get_window_height(self):
        style_search_box = self._theme.window_search.search_box
        style_window_item =  self._theme.window_search.window_item

        max_result_shown = self._config.window_search.behavior.max_results_shown

        items_height = (
            style_window_item.frame_style.height
        ) * max_result_shown
        
        height = (
            style_search_box.height + items_height
        )

        return height


    def _create_window(self) -> QWidget:
        config = self._config.window_search

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.Popup
        )
        
        screen_width, screen_height = self._get_screen_size()
        window_height = self._get_window_height()

        position_x = int((screen_width / 2) - (config.window_width / 2))
        position_y = int((screen_height / 2) - (window_height / 2))

        self.setFixedWidth(config.window_width)
        self.setFixedHeight(window_height)
        self.move(position_x, position_y)

        # Main panel
        main_panel = self._panel_constructor.create_panel()
        return main_panel


    def _create_search_box(self) -> QLineEdit:
        line_edit = self._panel_constructor.create_searchbox()
        _ = line_edit.textChanged.connect(
            self._on_search_box_changed
        )
        _ = line_edit.returnPressed.connect(
            self._on_searchbox_enter_pressed
        )

        return line_edit


    def _is_command(self, text: str) -> bool:
        if not text:
            return False
        
        if text[0] != ':':
            return False
        
        return self._command_service.is_command(text)


    def _on_searchbox_enter_pressed(self):
        text = self._search_line_edit.text()
        
        if self._is_command(text):
            self._command_service.execute(command=text)
            self._hide_window()
            return
            
        if self.winitem_manager.windows_item:
            self._focus_selected_window()


    def _on_search_box_changed(self, text: str):
        if not text.strip():
           self.winitem_manager.sync_to(
               windows_info=self.winitem_manager.windows_info
           )
           return

        if text[0] == ':':
            return
        
        self._searcher.search(
            query=text,
            windows_info=self.winitem_manager.windows_info
        )


    def _get_screen_size(self) -> tuple[int, int]:
        screen = QGuiApplication.primaryScreen()
        return screen.size().width(), screen.size().height()
