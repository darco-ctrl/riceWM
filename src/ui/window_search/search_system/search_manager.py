import threading

from src.core.events.event_bus import eventBus
from src.models.window import WindowInfo


class Searcher:
    def __init__(self):
        self._stop_process: bool = False
        
    def _start(self, query: str, window_info: list[WindowInfo]):

        thread = threading.Thread(
            target=self._search,
            args=(query, window_info),
            daemon=True
        )
        thread.start()

    def _search(self, query: str, windows_info: list[WindowInfo]):
        result: list[WindowInfo] = []
        
        for window_info in windows_info:
            if self._stop_process:
                return
            
            if query.lower() in window_info.title.lower():
                result.append(window_info)
                # print(f"window: - {window_info.title}")
                
        # print("emit")
        if self._stop_process:
            return
        
        result.sort(key=lambda item: item.title, reverse=True)
        eventBus.updateWindowItemList.emit(result)

    def _stop(self): 
        self._stop_process = True

class SearchManager:
    def __init__(self) -> None:
        self._is_running: bool = False
        self._searcher = Searcher()
        
        self._connect_events()

    def _connect_events(self):
        _ = eventBus.updateWindowItemList.connect(
            lambda _: self._search_finished()
        )

    def _search_finished(self):
        self._is_running = False

    def search(self, query: str, windows_info: list[WindowInfo]):

        if self._is_running:
            self._searcher._stop()
            self._searcher = Searcher()
            self._is_running = False

        self._is_running = True
        self._searcher._start(
            query=query,
            window_info=windows_info
        )
