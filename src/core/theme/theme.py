import json

from app.event_logger import EventLogger, LogEventType
from src.core.theme.constructor import ThemeConstructor
from src.core.theme.helper import ThemeHelper
from src.core.theme.virtual_desktop_notifier.virtual_desktop_notifier import (
    VirtualDesktopNotiferStyle,
)
from src.core.theme.window_search.window_search import WindowSearchStyle


class Theme:
    """Manages application theme loading and styling."""
    
    def __init__(self, logger: EventLogger, theme_path: str):
        self.logger = logger
        self.constructor: ThemeConstructor = ThemeConstructor() 
        self.helper: ThemeHelper = ThemeHelper()
        self.theme_file_path = theme_path
        self.name: str = ""
        
        self.window_search: WindowSearchStyle 
        self.virtual_desktop_notifer: VirtualDesktopNotiferStyle

        self.load()

    def reload(self):
        self.logger.log(
            log_type=LogEventType.LOAD_DATA,
            message=f"Applying Theme: {self.name}"
        )

        self.load()

    def load(self):
        with open(self.theme_file_path, "r") as file:
            self.logger.log(
                log_type=LogEventType.LOAD_DATA,
                message=f"Loading Theme: {self.theme_file_path}"
            )

            file.seek(0)
            data = json.load(file)
            self._create_data_classes(data)

            del data

    def _create_data_classes(self, data: dict):
        self.name = data["name"]
        self.window_search = self._get_window_search(data["window_search"])

        self.virtual_desktop_notifer = self._get_virtual_desktop_notifer(
            data["virtual_desktop_notifier"]
        )

    def _get_virtual_desktop_notifer(self, style: dict):
        return self.constructor.create_virtual_desktop_notifer_style(
            style=style
        )

    def _get_window_search(self, style: dict) -> WindowSearchStyle:

        return self.constructor.create_window_search(
            style=style
        )
