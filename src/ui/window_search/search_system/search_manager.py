import threading

from src.core.events.event_bus import eventBus
from src.models.window import WindowInfo
from src.ui.window_search.window_item.model import WindowItem

class Searcher:
    def __init__(self):
        self.stop_process: bool = False
        self.is_running: bool = False

        self.queue_window_info: list[WindowInfo]

    def get_queue_window_info(self) -> list[WindowInfo]:
        return self.queue_window_info

    def start(self, query: str, window_info: list[WindowInfo]):

        thread = threading.Thread(
            target=self.search,
            args=(query, window_info),
            daemon=True
        )
        thread.start()

    def search(self, query: str, windows_info: list[WindowInfo]):
        result: list[WindowInfo] = []
        
        for window_info in windows_info:
           if query.lower() in window_info.title.lower():
               result.append(window_info)

        self.queue_window_info = result
        eventBus.updateWindowItemList.emit()

    def stop(self): 
        self.stop_process = True

class SearchManager:
    def __init__(self) -> None:
        self.is_running: bool = False

        self.searcher: Searcher = Searcher()

    def search(self, query: str, window_items: list[WindowItem]):
        result: list[WindowItem] = []

        if self.is_running:
            self.searcher.stop()
            self.searcher = Searcher()
            self.is_running = False

        self.searcher.start(
            query=query,
            window_items=window_items
        )

        return result
