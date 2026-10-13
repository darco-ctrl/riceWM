from src.core.config.config import Config
from src.core.theme.theme import Theme
from src.services.commands.command_service import CommandService
from src.services.window.scanner import WindowScanner
from src.ui.virtual_desktop_notifier.virtual_desktop_notifier import (
    VirtualDesktopNotifier,
)
from src.ui.window_search.window_search import WindowSearch


class UIManager:
    def __init__(
        self, 
        config: Config, 
        theme: Theme, 
        window_scanner: WindowScanner,
        command_service: CommandService
    ):
        self._config = config
        self._theme = theme
        self._window_scanner = window_scanner
        self._command_service = command_service

        self._window_search: WindowSearch
        self._virtual_desktop_notifier: VirtualDesktopNotifier

    def load(self):
        config = self._config.virtual_desktop.notifier
        
        self._window_search = WindowSearch(
            config=self._config, theme=self._theme, window_scanner=self._window_scanner,
            command_service=self._command_service
        )

        if not config.enabled:
            return
        
        self._virtual_desktop_notifier = VirtualDesktopNotifier(
            config=self._config,
            theme=self._theme
        )
