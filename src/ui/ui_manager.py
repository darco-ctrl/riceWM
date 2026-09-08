from src.core.config.config import Config
from src.core.config.models import VirtualDesktopNotifierConfig
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
        self.config = config
        self.theme = theme
        self.window_scanner = window_scanner
        self.command_service = command_service

        self.window_search: WindowSearch
        self.virtual_desktop_notifier: VirtualDesktopNotifier

    def load(self):
        config: VirtualDesktopNotifierConfig = self.config.virtual_desktop.notifier
        
        self.window_search = WindowSearch(
            config=self.config, theme=self.theme, window_scanner=self.window_scanner,
            command_service=self.command_service
        )

        if not config.enabled:
            return
        
        self.virtual_desktop_notifier = VirtualDesktopNotifier(
            config=self.config,
            theme=self.theme
        )
