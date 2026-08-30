from dataclasses import dataclass

from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner
from src.ui.window_search.window_item.model import WindowItem


@dataclass
class TaskList:
    update: list[int]
    new: list[WindowInfo]
    delete: list[int]


class StateReconciler:
    def __init__(self, window_scanner: WindowScanner):
        self.window_scanner: WindowScanner = window_scanner

    def get_plan(
        self, windows_info_list: list[WindowInfo]
    ) -> TaskList:

        open_windows: list[WindowInfo] = self.window_scanner.get_windows_info()

        update_window: list[int] = []
        new_window: list[WindowInfo] = []
        delete_window: list[int] = []

        for window in open_windows:
            match = next(
                (
                    (index, item)
                    for index, item in enumerate(windows_info_list)
                    if item.hwnd == window.hwnd
                ),
                None,
            )

            if match:
                index, item = match
                update_window.append(index)

            else:
                new_window.append(window)

        for i in range(0, len(windows_info_list)):
            if not i in update_window:
                delete_window.append(i)

        task_list: TaskList = TaskList(
            delete=delete_window, new=new_window, update=update_window
        )

        return task_list
