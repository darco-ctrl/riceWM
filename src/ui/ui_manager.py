from src.core.config.config import Config
from src.core.theme.theme import Theme
from src.services.window.scanner import WindowScanner
from src.ui.window_search.window_search import WindowSearch


class UIManager:
    def __init__(self, config: Config, theme: Theme, window_scanner: WindowScanner):
        self.config = config
        self.theme = theme
        self.window_scanner = window_scanner

        self.window_search: WindowSearch

    def load(self):
        self.window_search = WindowSearch(
            config=self.config, theme=self.theme, window_scanner=self.window_scanner
        )
