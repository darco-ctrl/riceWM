from dataclasses import dataclass

from src.services.window import WindowInfo
from src.services.window_scanner import WindowScanner
from src.ui.window_search.item import WindowItem


@dataclass
class TaskList:
    update: list[int]
    new: list[WindowInfo]
    delete: list[int]


class StateReconciler:
    def __init__(self, window_scanner: WindowScanner):
        self.window_scanner = window_scanner

    def get_plan(self, window_item_lists: list[WindowItem]) -> TaskList:

        open_windows: list[WindowInfo] = self.window_scanner.get_windows_info()

        update_window: list[int] = []
        new_window: list[WindowInfo] = []
        delete_window: list[int] = []

        for window in open_windows:
            match = next(
                (
                    (index, item)
                    for index, item in enumerate(window_item_lists)
                    if item.hwnd == window.hwnd
                ),
                None,
            )

            if match:
                index, item = match
                update_window.append(index)

            else:
                new_window.append(window)

        for i in range(0, len(window_item_lists)):
            if not i in update_window:
                delete_window.append(i)

        task_list: TaskList = TaskList(
            delete=delete_window, new=new_window, update=update_window
        )

        return task_list
