from PySide6.QtWidgets import QWidget

from widgets.widget_themes.window_switch_panel_theme import WindowSwitchPanelTheme
from windows.window_manager import WindowInfo, WindowManager


class WindowSwitchPanelWidget(QWidget):
    def __init__(self, theme_dict: dict):
        super().__init__()
        self.theme = WindowSwitchPanelTheme(theme_dict)

        self.window_manager = WindowManager()

    def start(self):
        print("start")
        for window_info in self.window_manager.windows:
            print(f"title: {window_info.title}")
