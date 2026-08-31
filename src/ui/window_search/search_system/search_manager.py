import threading

from src.core.events.event_bus import eventBus
from src.models.window import WindowInfo
from src.ui.window_search.window_item.model import WindowItem

class Searcher:
    def __init__(self):
        self.stop_process: bool = False
        
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
            if self.stop_process:
                return
            
            if query.lower() in window_info.title.lower():
                result.append(window_info)
                # print(f"window: - {window_info.title}")
                
        # print("emit")
        if self.stop_process:
            return
        
        result.sort(key=lambda item: item.title, reverse=True)
        eventBus.updateWindowItemList.emit(result)

    def stop(self): 
        self.stop_process = True

class SearchManager:
    def __init__(self) -> None:
        self.is_running: bool = False

        self.searcher: Searcher = Searcher()
        self.connect_events()

    def connect_events(self):
        _ = eventBus.updateWindowItemList.connect(
            lambda _: self.search_finished()
        )

    def search_finished(self):
        self.is_running = False

    def search(self, query: str, windows_info: list[WindowInfo]):

        if self.is_running:
            self.searcher.stop()
            self.searcher = Searcher()
            self.is_running = False

        self.is_running = True
        self.searcher.start(
            query=query,
            window_info=windows_info
        )
