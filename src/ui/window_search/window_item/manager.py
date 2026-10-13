

from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout

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
        self._initialize_state(searcher, scroll_area, scroller_layout)
        self._initialize_helpers(theme, config, window_scanner)
        self._initialize_constructor(theme, config)
        self._initialize_empty_label()
        self._connect_events()
    
    
    def _initialize_state(
        self,
        searcher: SearchManager,
        scroll_area: QScrollArea,
        scroller_layout: QVBoxLayout,
    ) -> None:
        self._searcher = searcher
        self._scroll_area = scroll_area
        self._scroller_layout = scroller_layout
    
        self._current_selection = 0
        
        self.windows_item: list[WindowItem] = []
        self.windows_info: list[WindowInfo] = []
    
    
    def _initialize_helpers(
        self,
        theme: Theme,
        config: Config,
        window_scanner: WindowScanner,
    ) -> None:
        self._helper = WindowItemHelper()
    
        self._reconciler = StateReconciler(
            window_scanner=window_scanner,
            helper=self._helper,
        )
    
        self._theme_applier = WinItemThemeApplier(theme=theme)
    
    
    def _initialize_constructor(
        self,
        theme: Theme,
        config: Config,
    ) -> None:
        self._constructor = WinItemConstructor(
            theme_applier=self._theme_applier,
            scroll_layout=self._scroller_layout,
            config=config,
            theme=theme,
            helper=self._helper,
        )
    
    
    def _initialize_empty_label(self) -> None:
        self._empty_label = self._constructor.create_empty_label()
        self._scroller_layout.addWidget(self._empty_label)

    
    def _connect_events(self):
        _ = eventBus.updateWindowItemList.connect(
            self._update_to_search
        )
    

    def _get_emtpy_label(self) -> QLabel:
        empty_label: QLabel = self._constructor.create_empty_label()

        self._scroller_layout.addWidget(empty_label)

        return empty_label


    def _check_is_empty(self):
        if self.windows_item:
            self._empty_label.hide()

        else:
            self._empty_label.show()


    def _update_to_search(
        self, 
        windows_info: list[WindowInfo]
    ):
        self.sync_to(
            windows_info=windows_info
        )

    def _select_first(self):
        if not self.windows_item:
            return

        self._select_window(
            window=self.windows_item[0]
        )
        self._current_selection = 0
        

    def _change_sel_window(self, new_index: int, old_index: int):

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
            if self._current_selection < winitem_len:
                prev_window = self.windows_item[
                    self._current_selection
                ]

        if prev_window:        
            self._deselect_window(prev_window)

        if new_window:
            self._current_selection = new_index
            self._select_window(new_window)

            
    def _select_window(self, window: WindowItem):
        self._scroll_area.ensureWidgetVisible(window.frame)
        self._theme_applier.select_window(
            win_item=window
        )
        

    def _deselect_window(self, window: WindowItem):
        self._theme_applier.deselect_window(
            win_item=window
        )


    def hide(self):
        self._change_sel_window(
            new_index=0,
            old_index=self._current_selection
        )


    def reapply_theme(self):
        for i in range(len(self.windows_item)):
            window = self.windows_item[i]
            self._theme_applier.recolor_item(window)
            
            window.reload()

            if i == self._current_selection:
                self._select_window(window)


    def sync_to(self, windows_info: list[WindowInfo]):
        self._constructor.delete_all_winitems(
            window_items=self.windows_item
        )
        
        self._constructor.create_window_items(
            new_info=windows_info,
            window_items=self.windows_item
        )

        self._select_first()
        self._check_is_empty()


    def sync_to_new(self):
        task_list: TaskList = self._reconciler.get_new_plan(
            windows_info_list=self.windows_info
        )

        self._constructor.update_window_items(
            items=task_list.update,
            windows=self.windows_item
        )
        self._constructor.create_new_window_items(
            current_info=self.windows_info,
            new_info=task_list.new,
            window_items=self.windows_item
        )
        self._constructor.delete_windows_info(
            items=task_list.delete,
            windows_info=self.windows_info,
            windows_item=self.windows_item
        )

        self._select_first()
        self._check_is_empty()

        
    def select_next(
        self
    ):
        if not self.windows_item:
            return
        
        prev_index: int = self._current_selection
        window_count = len(self.windows_item)

        if prev_index < 0:
            prev_index = 0
        elif prev_index >= window_count:
            prev_index = window_count - 1

        next_index: int = prev_index + 1
        index = next_index % len(self.windows_item)

        self._change_sel_window(
            new_index=index, old_index=self._current_selection
        )

    def select_prev(
        self
    ):
        if not self.windows_item:
            return
        
        prev_index: int = self._current_selection
        window_count: int = len(self.windows_item)

        if prev_index < 0:
            prev_index = 0
        elif prev_index >= window_count:
            prev_index = window_count - 1

        p_index = prev_index - 1
        index = p_index % window_count
        
        self._change_sel_window(
            new_index=index, old_index=self._current_selection
        )

    def focus_selected_window(self):
        

        if self._current_selection < 0:
            return

        count = len(self.windows_item)
        if self._current_selection >= count:
           return 
           
        window = self.windows_item[self._current_selection]

        eventBus.focusWindow.emit(window.info.hwnd)
