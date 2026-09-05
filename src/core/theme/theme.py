import json
from typing import Any

from src.core.events.event_bus import eventBus
from src.core.theme.constructor import ThemeConstructor
from src.core.theme.helper import ThemeHelper
from src.core.theme.virtual_desktop_notifier.virtual_desktop_notifier import (
    VirtualDesktopNotiferStyle,
)
from src.core.theme.window_search.window_search import WindowSearchStyle


class Theme:
    def __init__(self, theme_path: str):

        self.constructor: ThemeConstructor = ThemeConstructor() 
        self.helper: ThemeHelper = ThemeHelper()
        self.theme_file_path = theme_path
        self.name: str = ""
        
        self.window_search: WindowSearchStyle 
        self.virtual_desktop_notifer: VirtualDesktopNotiferStyle

        self.load()

    def reload(self):
        print("reloading themes")
        self.load()
        print(f"applying new theme: {self.name}")

    def load(self):
        with open(self.theme_file_path, "r") as file:
            # text = file.read()
            # print(f"\n\n {text} \n\n")
            print(f"Loading Theme: {self.theme_file_path}.")

            file.seek(0)
            data = json.load(file)
            self.create_data_classes(data)

            del data

    def create_data_classes(self, data: dict):
        self.name = data["name"]
        self.window_search = self.get_window_search(data["window_search"])

        self.virtual_desktop_notifer = self.get_virtual_desktop_notifer(
            data["virtual_desktop_notifier"]
        )

    def get_virtual_desktop_notifer(self, style: dict):
        return self.constructor.create_virtual_desktop_notifer_style(
            style=style
        )

    def get_window_search(self, style: dict) -> WindowSearchStyle:

        return self.constructor.create_window_search(
            style=style
        )
