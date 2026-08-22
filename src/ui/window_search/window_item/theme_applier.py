from typing import cast

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.theme.theme import Theme
from src.ui.window_search.window_item.model import WindowItem


class WinItemThemeApplier:
    def __init__(self, theme: Theme):
        self.theme: Theme = theme
    
    def recolor_item(self, window_item: WindowItem):
        # print(f"changing: background_color: {style.background_color}")
        self.recolor_frame(window_item.frame)
        self.recolor_selection_indicator(window_item.selection_indicator)
        self.recolor_icon_label(
            outer_layout=window_item.icon_layout,
            container=window_item.icon_container,
            layout=window_item.icon_layout,
            icon_label=window_item.icon_label,
        )
        self.recolor_title_label(window_item.title_label)
        self.recolor_keybind_label(window_item.key_bind_label)

    def recolor_frame(self, frame: QWidget):
        frame_style = self.theme.window_search.window_item_container.item_frame
        border_style = frame_style.border_style

        frame.setFixedHeight(frame_style.height)
        frame.setStyleSheet(f"""
        #itemFrame {{
                border-style: {border_style.style};
                border-radius: {border_style.radius}px;
                border-left-width: {border_style.width[0]}px;
                border-top-width: {border_style.width[1]}px;
                border-right-width: {border_style.width[2]}px;
                border-bottom-width: {border_style.width[3]}px;
                border-color: {border_style.color};
                background-color: {frame_style.background_color};
            }}
        """)
        frame_layout: QHBoxLayout = cast(QHBoxLayout, frame.layout())
        frame_layout.setContentsMargins(
            frame_style.contents_margin[0],
            frame_style.contents_margin[1],
            frame_style.contents_margin[2],
            frame_style.contents_margin[3],
        )

    def recolor_selection_indicator(self, selection_indicator: QWidget):
        style = self.theme.window_search.window_item_container.item_frame.selection_indicator

        selection_indicator.setFixedSize(QSize(style.width, style.height))
        selection_indicator.setStyleSheet(f"""
        #selectionIndicator {{
                background-color: {style.background_color};
            }}
        """)

    def recolor_icon_label(
        self, outer_layout: QVBoxLayout, container: QWidget, layout: QVBoxLayout, icon_label: QLabel
    ):  

        style = self.theme.window_search.window_item_container.item_frame.icon_container
        
        container.setFixedSize(QSize(style.width, style.height))
        container.setStyleSheet(f"""
            #iconContainer {{
                border-style: {style.border_style.style};
                border-radius: {style.border_style.radius}px;
                border-left-width: {style.border_style.width[0]}px;
                border-top-width: {style.border_style.width[1]}px;
                border-right-width: {style.border_style.width[2]}px;
                border-bottom-width: {style.border_style.width[3]}px;
                border-color: {style.border_style.color};
                background-color: {style.background_color};
            }}
        """)
        layout.setContentsMargins(
            style.margin[0],
            style.margin[1],
            style.margin[2],
            style.margin[3],
        )

        icon_width = style.width - style.margin[0] - style.margin[2]
        icon_height = style.height - style.margin[1] - style.margin[3]

        icon_label.setFixedSize(QSize(icon_width, icon_height))

    def recolor_title_label(self, label: QLabel):
        style = (
            self.theme.window_search.window_item_container.item_frame.title_label
        )

        # label.setFixedSize(QSize(style.width, style.height))
        label.setStyleSheet(f"""
        #titleLabel {{
            border-style: {style.border_style.style};
            border-radius: {style.border_style.radius}px;
            border-left-width: {style.border_style.width[0]}px;
            border-top-width: {style.border_style.width[1]}px;
            border-right-width: {style.border_style.width[2]}px;
            border-bottom-width: {style.border_style.width[3]}px;
            border-color: {style.border_style.color};
            background-color: {style.background_color};
            color: {style.color}
        }}
        """)

        label.setMargin(style.margin)

        font = style.font_style.to_qfont(label.font())
        label.setFont(font)

        # print("reapplied theme to window title...")

    def recolor_keybind_label(self, label: QLabel):
        style = self.theme.window_search.window_item_container.item_frame.key_bind_lable

        # print(f"setting keybind label background color to : {style.background_color}")
        label.setFixedSize(QSize(style.width, style.height))
        label.setStyleSheet(f"""
        #keyBindLabel {{
            border-style: {style.border_style.style};
            border-radius: {style.border_style.radius}px;
            border-left-width: {style.border_style.width[0]}px;
            border-top-width: {style.border_style.width[1]}px;
            border-right-width: {style.border_style.width[2]}px;
            border-bottom-width: {style.border_style.width[3]}px;
            border-color: {style.border_style.color};
            background-color: {style.background_color};
            color: {style.color}
        }}
        """)

        label.setMargin(style.margin)

        font = style.font_style.to_qfont(label.font())
        label.setFont(font)

    def select_window(self, window: WindowItem):

        style = self.theme.window_search.window_item_container.item_frame

        frame_style = style.on_selected
        label_style = style.title_label.on_selected
        icon_style = style.icon_container.on_selected
        keybind_style = style.key_bind_lable.on_selected
        
        frame = window.frame
        title_label = window.title_label
        icon = window.icon_container
        keybind = window.key_bind_label

        # SELECTION INDICATOR
        window.set_selected(True)

        # FRAME
        frame.setStyleSheet(f"""
        #itemFrame {{
            background-color: {frame_style.background_color};
        }}
        """)

        # TITLE LABEL
        title_label.setStyleSheet(f"""
        #titleLabel {{
            background-color: {label_style.background_color};
            color: {label_style.color}
        }}
        """)

        # ICON CONTAINER
        icon.setStyleSheet(f"""
        #iconContainer {{
            background-color: {icon_style.background_color}
        }}
        """)

        # KEYBIND LABEL
        keybind.setStyleSheet(f"""
        #keyBindLabel {{
            background-color: {keybind_style.background_color};
            color: {keybind_style.color}
        }}
        """)

    def deselect_window(self, window: WindowItem):
        
        style = self.theme.window_search.window_item_container.item_frame
        
        label_style = style.title_label
        icon_style = style.icon_container
        keybind_style = style.key_bind_lable
        
        frame = window.frame
        title_label = window.title_label
        icon = window.icon_container
        keybind = window.key_bind_label

        # SELECTION INDICATOR
        window.set_selected(False)

        # FRAME
        frame.setStyleSheet(f"""
        #itemFrame {{
            background-color: {style.background_color};
        }}
        """)

        # TITLE LABEL
        title_label.setStyleSheet(f"""
        #titleLabel {{
            background-color: {label_style.background_color};
            color: {label_style.color}
        }}
        """)

        # ICON CONTAINER
        icon.setStyleSheet(f"""
        #iconContainer {{
            background-color: {icon_style.background_color}
        }}
        """)

        # KEYBIND LABEL
        keybind.setStyleSheet(f"""
        #keyBindLabel {{
            background-color: {keybind_style.background_color};
            color: {keybind_style.color}
        }}
        """)
