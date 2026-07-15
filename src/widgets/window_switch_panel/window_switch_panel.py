from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QVBoxLayout, QWidget

from widgets.widget_data.theme.window_switch_panel_theme import WindowSwitchPanelTheme
from widgets.widget_data.config.window_switch_panel_config import WindowSwitchPanelConfig
from windows.window_manager import WindowManager


class WindowSwitchPanelWidget(QWidget):
    def __init__(self, config_dict: dict, theme_dict: dict):
        super().__init__()
        self.config = WindowSwitchPanelConfig(config_dict)
        self.theme = WindowSwitchPanelTheme(theme_dict)

        self.window_manager = WindowManager()

        self.root_layout = QVBoxLayout(self)

        self.main_panel: QWidget = self.create_window()

        self.create_search_box()


    def create_window(self) -> QWidget:

        #self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
        )


        window_margin = 12

        screen_width, screen_height = self.get_screen_size()

        window_height = int(screen_height * 0.9)

        position_x = int((screen_width / 2) - (self.config.window_panel.width / 2))
        position_y = int((screen_height / 2) - (window_height / 2))

        self.setFixedWidth(self.config.window_panel.width)
        self.setFixedHeight(window_height)
        self.move(position_x, position_y)

        # Main panel
        main_panel = QWidget()

        main_panel.setStyleSheet(f"""
            background-color: {self.theme.main_panel.background_color};
        """)

        main_panel.setFixedHeight(100)

        # Main panel layout
        main_panel_layout = QVBoxLayout(main_panel)
        main_panel_layout.setContentsMargins(0, 0, 0, 0)
        main_panel_layout.setSpacing(0)

        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)
        self.root_layout.addWidget(main_panel)

        return main_panel

    def create_search_box(self):
        panel_layout = self.main_panel.layout()

        if not panel_layout:
            return

        container = QWidget()

        container.setFixedHeight(self.config.search_box.height)

        container.setStyleSheet("""
            background-color: transparent;
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        line_edit = QLineEdit()
        line_edit.setStyleSheet(f"""
            background_color:
        """)

        panel_layout.addWidget(container)

    def get_screen_size(self) -> tuple[int, int]:
        screen = QGuiApplication.primaryScreen()
        return screen.size().width(), screen.size().height()

    def start(self):
        print("start")
        for window_info in self.window_manager.windows:
            print(f"title: {window_info.title}")

        self.show()
