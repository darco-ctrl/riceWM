import threading

from src.ui.window_search.window_item.model import WindowItem


class Searcher:
    def __init__(self):
        self.stop_process: bool = False
        self.is_running: bool = False

    def start(self, query: str, window_items: list[WindowItem]):

        thread = threading.Thread(
            target=self.search,
            args=(query, window_items),
            daemon=True
        )
        thread.start()

    def search(self, query: str, window_items: list[WindowItem]):
        pass

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
