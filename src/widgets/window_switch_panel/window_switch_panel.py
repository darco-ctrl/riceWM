from typing import cast

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QSizePolicy, QVBoxLayout, QWidget

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

        position_x = int((screen_width / 2) - (self.theme.main_panel.window_width / 2))
        position_y = int((screen_height / 2) - (window_height / 2))

        self.setFixedWidth(self.theme.main_panel.window_width)
        self.setFixedHeight(window_height)
        self.move(position_x, position_y)

        # Main panel
        main_panel = QWidget()

        main_panel.setStyleSheet(f"""
            background-color: {self.theme.main_panel.background_color};
        """)

        #main_panel.setFixedHeight(100)

        # Main panel layout
        main_panel_layout = QVBoxLayout(main_panel)
        main_panel_layout.setContentsMargins(0, 0, 0, 0)
        main_panel_layout.setSpacing(0)

        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)
        self.root_layout.addWidget(main_panel)

        return main_panel

    def create_search_box(self):
        panel_layout: QVBoxLayout = cast(QVBoxLayout, self.main_panel.layout())

        if not panel_layout:
            return

        container = QWidget()

        container.setFixedHeight(self.theme.search_box.height)

        container.setStyleSheet(f"""
            background-color: {self.theme.search_box.background_color};
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(
            self.theme.line_edit.margin[0],
            self.theme.line_edit.margin[1],
            self.theme.line_edit.margin[2],
            self.theme.line_edit.margin[3]
        )
        layout.setSpacing(0)

        line_edit = QLineEdit()

        #line_edit.setFixedHeight(self.theme.search_box.height)

        size_policy = line_edit.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
        line_edit.setSizePolicy(size_policy)

        line_edit.setStyleSheet(f"""
            border-style: {self.theme.line_edit.border_style};
            border-radius: {self.theme.line_edit.border_radius}px;
            border-top-width: {self.theme.line_edit.border_width[0]}px;
            border-right-width: {self.theme.line_edit.border_width[1]}px;
            border-bottom-width: {self.theme.line_edit.border_width[2]}px;
            border-left-width: {self.theme.line_edit.border_width[3]}px;
            background-color: {self.theme.line_edit.background_color};
            border-color: {self.theme.line_edit.border_color};
            color: {self.theme.font_style.color}
        """)

        line_edit.setTextMargins(
            self.theme.line_edit.text_margin[0],
            self.theme.line_edit.text_margin[1],
            self.theme.line_edit.text_margin[2],
            self.theme.line_edit.text_margin[3]
        )

        font = line_edit.font()
        font.setFamily(self.theme.font_style.family)
        font.setPixelSize(self.theme.font_style.pixel_size)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, self.theme.font_style.letter_spacing)
        font.setBold(self.theme.font_style.is_bold)
        font.setItalic(self.theme.font_style.is_italic)
        font.setUnderline(self.theme.font_style.is_underline)
        font.setStrikeOut(self.theme.font_style.is_strike_out)

        line_edit.setFont(font)

        layout.addWidget(line_edit)
        panel_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignTop)

    def get_screen_size(self) -> tuple[int, int]:
        screen = QGuiApplication.primaryScreen()
        return screen.size().width(), screen.size().height()

    def start(self):
        print("start")
        for window_info in self.window_manager.windows:
            print(f"title: {window_info.title}")

        self.show()
