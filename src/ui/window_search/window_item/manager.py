from PySide6.QtWidgets import QVBoxLayout

from src.core.config.config import Config
from src.core.events.event_bus import eventBus
from src.core.theme.theme import Theme
from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner
from src.ui.window_search.window_item.constructor import WinItemConstructor
from src.ui.window_search.window_item.helper import WindowItemHelper
from src.ui.window_search.window_item.model import WindowItem
from src.ui.window_search.window_item.reconciler import StateReconciler, TaskList
from src.ui.window_search.window_item.theme_applier import WinItemThemeApplier


class WinItemManager:
    def __init__(
        self, 
        theme: Theme, 
        config: Config,
        scroller_layout: QVBoxLayout,
        window_scanner: WindowScanner
    ):

        self.helper: WindowItemHelper = WindowItemHelper()
        
        self.windows_item: list[WindowItem] = []
        self.windows_info: list[WindowInfo] = []
        self.reconciler: StateReconciler = StateReconciler(
            window_scanner=window_scanner,
            helper=self.helper
        )
        self.theme_applier: WinItemThemeApplier = WinItemThemeApplier(
            theme=theme
        )
        self.constructor: WinItemConstructor = WinItemConstructor(
            theme_applier=self.theme_applier,
            config=config,
            theme=theme,
            helper=self.helper
        )
        self.scroller_layout: QVBoxLayout = scroller_layout
        self.current_selection: int = 0

    def sync_to_search(self, windows_info: list[WindowInfo]):
        self.constructor.delete_all_winitems(
            window_items=self.windows_item
        )

        self.constructor.create_window_items(
            new_info=windows_info,
            window_items=self.windows_item
        )

    def sync(self):
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

        self.sort(self.windows_item)

        if len(self.windows_item) != 0:
            select_window_item = self.windows_item[0]
            self.theme_applier.select_window(
                window=select_window_item
            )

    def focus_selected_window(self):
        window = self.windows_item[self.current_selection]

        eventBus.focusWindow.emit(window.info.hwnd)

    def change_sel_window(self, window: WindowItem, prev_window: WindowItem):
        self.theme_applier.deselect_window(prev_window)
        self.theme_applier.select_window(window)
        
    def select_next(
        self
    ):
        prev_index: int = self.current_selection
        window_count = len(self.windows_item)

        if prev_index < 0:
            prev_index = 0
        elif prev_index >= window_count:
            prev_index = window_count - 1

        next_index: int = prev_index + 1
        index = next_index % len(self.windows_item)

        prev_widnow = self.windows_item[self.current_selection]
        window = self.windows_item[index]
        self.change_sel_window(
            prev_window=prev_widnow, window=window
        )

        self.current_selection = index

    def select_prev(
        self
    ):
        prev_index: int = self.current_selection
        window_count: int = len(self.windows_item)

        if prev_index < 0:
            prev_index = 0
        elif prev_index >= window_count:
            prev_index = window_count - 1

        p_index = prev_index - 1
        index = p_index % window_count
        
        window = self.windows_item[index]
        prev_window = self.windows_item[prev_index]
        self.change_sel_window(
            prev_window=prev_window, window=window
        )

        self.current_selection = index
        
    def hide(self):
        window = self.windows_item[self.current_selection]

        self.theme_applier.deselect_window(window)
        self.current_selection = 0

    def sort(self, window_items: list[WindowItem]):
        print(" sorting ")

        window_items.sort(key=lambda item: item.info.title)

        for i in range(len(window_items)):
            window_item = window_items[i]
            window_item.index = i + 1
            window_item.update_key_bind_label()

            self.scroller_layout.addWidget(window_item.frame)

    def reapply_theme(self):
        for i in range(len(self.windows_item)):
            window = self.windows_item[i]
            self.theme_applier.recolor_item(window)
            window.reload()

            if i == self.current_selection:
                self.theme_applier.select_window(window)
