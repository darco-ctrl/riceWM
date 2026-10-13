from app.event_logger import EventLogger
from src.core.config.config import Config
from src.services.window.scanner import WindowScanner
from src.wm.controller import WindowController
from src.wm.registry import WindowRegistry


class WindowManager:
    def __init__(
        self, 
        logger: EventLogger,
        window_scanner: WindowScanner,
        config: Config
    ) -> None:
        self._config: Config = config
        
        self._registry = WindowRegistry(
            window_scanner=window_scanner,
            config=config
        )
        self._controller = WindowController(
            logger, self._registry, window_scanner
        )
        self._window_scanner = window_scanner
