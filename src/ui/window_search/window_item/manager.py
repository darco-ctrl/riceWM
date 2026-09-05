from typing import cast

from PySide6.QtWidgets import QScrollArea, QVBoxLayout

from src.core.config.config import Config
from src.core.events.event_bus import eventBus
from src.core.theme.theme import Theme
from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner
from src.ui.window_search.search_system.search_manager import SearchManager
from src.ui.window_search.window_item.constructor import WinItemConstructor
from src.ui.window_search.window_item.helper import WindowItemHelper
from src.ui.window_search.window_item.reconciler import StateReconciler, TaskList
from src.ui.window_search.window_item.theme_applier import WinItemThemeApplier
from src.ui.window_search.window_item.window_item import WindowItem


class WinItemManager:
    def __init__(
        self, 
        theme: Theme, 
        config: Config,
        scroll_area: QScrollArea,
        window_scanner: WindowScanner,
        searcher: SearchManager,
        scroller_layout: QVBoxLayout,
    ):
        self.connect_events()
        self.helper: WindowItemHelper = WindowItemHelper()
        self.searcher: SearchManager = searcher
        
        self.windows_item: list[WindowItem] = []
        self.windows_info: list[WindowInfo] = []
        self.reconciler: StateReconciler = StateReconciler(
            window_scanner=window_scanner,
            helper=self.helper
        )
        self.theme_applier: WinItemThemeApplier = WinItemThemeApplier(
            theme=theme
        )

        self.scroll_area: QScrollArea = scroll_area
        self.scroller_layout: QVBoxLayout = scroller_layout
        
        self.constructor: WinItemConstructor = WinItemConstructor(
            theme_applier=self.theme_applier,
            scroll_layout=self.scroller_layout,
            config=config,
            theme=theme,
            helper=self.helper
        )
        self.current_selection: int = 0

    def connect_events(self):
        _ = eventBus.updateWindowItemList.connect(
            self.update_to_search
        )

    def update_to_search(
        self, 
        windows_info: list[WindowInfo]
    ):
        self.sync_to(
            windows_info=windows_info
        )

    def select_first(self):
        if not self.windows_item:
            return

        self.select_window(
            window=self.windows_item[0]
        )
        self.current_selection = 0

    def sync_to(self, windows_info: list[WindowInfo]):
        self.constructor.delete_all_winitems(
            window_items=self.windows_item
        )
        
        self.constructor.create_window_items(
            new_info=windows_info,
            window_items=self.windows_item
        )

        self.select_first()

    def sync_to_new(self):
        task_list: TaskList = self.reconciler.get_new_plan(
            windows_info_list=self.windows_info
        )

        self.constructor.update_window_items(
            items=task_list.update,
            windows=self.windows_item
        )
        self.constructor.create_new_window_items(
            current_info=self.windows_info,
            new_info=task_list.new,
            window_items=self.windows_item
        )
        self.constructor.delete_windows_info(
            items=task_list.delete,
            windows_info=self.windows_info,
            windows_item=self.windows_item
        )

        self.select_first()

    def focus_selected_window(self):
        window = self.windows_item[self.current_selection]

        eventBus.focusWindow.emit(window.info.hwnd)

    def change_sel_window(self, new_index: int, old_index: int):

        if not self.windows_item:
            return
        
        winitem_len = len(self.windows_item)

        new_window: WindowItem | None = None
        prev_window: WindowItem | None = None
        
        if new_index < winitem_len:
            new_window = self.windows_item[new_index]
        else:
            new_window = self.windows_item[0]

        if old_index < winitem_len:
            prev_window = self.windows_item[old_index]
        else:
            if self.current_selection < winitem_len:
                prev_window = self.windows_item[
                    self.current_selection
                ]

        if prev_window:        
            self.deselect_window(prev_window)

        if new_window:
            self.current_selection = new_index
            self.select_window(new_window)
        
    def select_next(
        self
    ):
        if not self.windows_item:
            return
        
        prev_index: int = self.current_selection
        window_count = len(self.windows_item)

        if prev_index < 0:
            prev_index = 0
        elif prev_index >= window_count:
            prev_index = window_count - 1

        next_index: int = prev_index + 1
        index = next_index % len(self.windows_item)

        self.change_sel_window(
            new_index=index, old_index=self.current_selection
        )

    def select_prev(
        self
    ):
        if not self.windows_item:
            return
        
        prev_index: int = self.current_selection
        window_count: int = len(self.windows_item)

        if prev_index < 0:
            prev_index = 0
        elif prev_index >= window_count:
            prev_index = window_count - 1

        p_index = prev_index - 1
        index = p_index % window_count
        
        self.change_sel_window(
            new_index=index, old_index=self.current_selection
        )

    def select_window(self, window: WindowItem):
        self.scroll_area.ensureWidgetVisible(window.frame)
        self.theme_applier.select_window(
            win_item=window
        )
        

    def deselect_window(self, window: WindowItem):
        self.theme_applier.deselect_window(
            win_item=window
        )
        
    def hide(self):
        self.change_sel_window(
            new_index=0,
            old_index=self.current_selection
        )

    def reapply_theme(self):
        for i in range(len(self.windows_item)):
            window = self.windows_item[i]
            self.theme_applier.recolor_item(window)
            
            window.reload()

            if i == self.current_selection:
                self.select_window(window)
