from PySide6.QtWidgets import QVBoxLayout

from src.core.config.config import Config
from src.core.events.event_bus import eventBus
from src.core.theme.theme import Theme
from src.services.window.scanner import WindowScanner
from src.ui.window_search.window_item.constructor import WinItemConstructor
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
        self.window_items: list[WindowItem] = []
        self.reconciler: StateReconciler = StateReconciler(
            window_scanner=window_scanner
        )
        self.theme_applier: WinItemThemeApplier = WinItemThemeApplier(
            theme=theme
        )
        self.constructor: WinItemConstructor = WinItemConstructor(
            theme_applier=self.theme_applier,
            config=config,
            theme=theme
        )
        self.scroller_layout: QVBoxLayout = scroller_layout
        self.current_selection: int = 0

    def sync(self):
        task_list: TaskList = self.reconciler.get_plan(
            window_item_lists=self.window_items
        )

        self.constructor.update_window_items(
            task_list.update, self.window_items
        )
        _ = self.constructor.create_window_items(
            task_list.new, self.window_items
        )
        self.constructor.delete_window_items(
            task_list.delete, self.window_items
        )

        self.sort(self.window_items)

        if len(self.window_items) != 0:
            select_window_item = self.window_items[0]
            self.theme_applier.select_window(
                window=select_window_item
            )

    def focus_selected_window(self):
        window = self.window_items[self.current_selection]

        eventBus.focusWindow.emit(window.info.hwnd)

    def change_sel_window(self, window: WindowItem, prev_window: WindowItem):
        self.theme_applier.deselect_window(prev_window)
        self.theme_applier.select_window(window)
        
    def select_next(
        self
    ):
        prev_index: int = self.current_selection
        window_count = len(self.window_items)

        if prev_index < 0:
            prev_index = 0
        elif prev_index >= window_count:
            prev_index = window_count - 1

        next_index: int = prev_index + 1
        index = next_index % len(self.window_items)

        prev_widnow = self.window_items[self.current_selection]
        window = self.window_items[index]
        self.change_sel_window(
            prev_window=prev_widnow, window=window
        )

        self.current_selection = index

    def select_prev(
        self
    ):
        prev_index: int = self.current_selection
        window_count: int = len(self.window_items)

        if prev_index < 0:
            prev_index = 0
        elif prev_index >= window_count:
            prev_index = window_count - 1

        p_index = prev_index - 1
        index = p_index % window_count
        
        window = self.window_items[index]
        prev_window = self.window_items[prev_index]
        self.change_sel_window(
            prev_window=prev_window, window=window
        )

        self.current_selection = index
        
    def hide(self):
        window = self.window_items[self.current_selection]

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
        for i in range(len(self.window_items)):
            window = self.window_items[i]
            self.theme_applier.recolor_item(window)
            window.reload()

            if i == self.current_selection:
                self.theme_applier.select_window(window)
