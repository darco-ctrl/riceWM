from typing import cast

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

import src.app.paths as rice_paths
from src.core.config.config import Config
from src.core.theme.theme import Theme
from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner
from src.ui.window_search.item import WindowItem
from src.ui.window_search.reconciler import (
    StateReconciler,
    TaskList,
)


class ItemBuilder:
    def __init__(
        self,
        theme: Theme,
        config: Config,
        window_scanner: WindowScanner,
        scroller_widget: QWidget,
    ) -> None:
        self.theme: Theme = theme
        self.config: Config = config
        self.window_scanner: WindowScanner = window_scanner
        self.scroller_layout: QVBoxLayout = cast(QVBoxLayout, scroller_widget.layout())

        self.state_reconciler = StateReconciler(self.window_scanner)

    def sync_window_items(self, window_items: list[WindowItem], c_index: int):

        task_list: TaskList = self.state_reconciler.get_plan(window_items)

        self.update_window_items(task_list.update, window_items)
        _ = self.create_window_items(task_list.new, window_items)
        self.delete_window_items(task_list.delete, window_items)
        
        self.sort(window_items)

        if len(window_items) != 0:   
            select_window_item = window_items[0]
            self.set_sel_window(window=select_window_item)

    def update_window_items(self, items: list[int], windows: list[WindowItem]):

        for item_index in items:
            windows[item_index].update()

    def delete_window_items(self, items: list[int], window_items: list[WindowItem]):

        for index in sorted(items, reverse=True):
            # print(f"removing index: {index}")

            window_items[index].delete()
            del window_items[index]

    def create_window_items(
        self, windows_info: list[WindowInfo], window_items: list[WindowItem]
    ):

        count = 1
        for window in windows_info:
            window_item: WindowItem = self.create_window_item(count, window)
            window_item.load()

            count += 1
            window_items.append(window_item)
            self.recolor_item(window_item=window_item)

        return window_items

    def create_window_item(
        self, count: int, window_info: WindowInfo
    ) -> WindowItem:  # m layout is main scroller layout
        frame = self.create_item_frame()
        f_layout: QHBoxLayout = cast(QHBoxLayout, frame.layout())

        selection_indicator = self.create_selection_indicator(f_layout)
        icon_container, c_layout, icon_label = self.create_icon_label(f_layout)
        title_label = self.create_window_title_label(f_layout)
        key_bind_label = self.create_key_bind_label(f_layout)

        # self.scroller_layout.addWidget(frame)

        window_item: WindowItem = WindowItem(
            hwnd=window_info.hwnd,
            name=window_info.name,
            title=window_info.title,
            icon_path=window_info.icon_path,
            index=count,
            frame=frame,
            key_bind_label=key_bind_label,
            icon_container=icon_container,
            c_layout=c_layout,
            icon_label=icon_label,
            selection_indicator=selection_indicator,
            title_label=title_label,
        )

        return window_item

    def create_item_frame(self) -> QFrame:
        style = self.theme.window_search.window_item_container.item_frame

        frame = QFrame()
        frame.setObjectName("itemFrame")
        frame.setFixedHeight(style.height)

        frame_layout: QHBoxLayout = QHBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        return frame

    def create_selection_indicator(self, layout: QHBoxLayout) -> QWidget:
        style = self.theme.window_search.window_item_container.item_frame.selection_indicator

        indicator: QWidget = QWidget()
        indicator.setObjectName("selectionIndicator")

        layout.addWidget(indicator, alignment=Qt.AlignmentFlag.AlignVCenter)

        return indicator

    def create_icon_label(
        self, layout: QHBoxLayout
    ) -> tuple[QWidget, QVBoxLayout, QLabel]:
        style = self.theme.window_search.window_item_container.item_frame.icon_container

        container: QWidget = QWidget()
        container.setObjectName("iconContainer")
        container.setFixedSize(QSize(style.width, style.height))

        c_layout: QVBoxLayout = QVBoxLayout(container)

        icon_width = style.width - style.margin[0] - style.margin[2]
        icon_height = style.height - style.margin[1] - style.margin[3]

        icon_label: QLabel = QLabel()
        icon_label.setObjectName("iconLabel")
        icon_label.setFixedSize(QSize(icon_width, icon_height))
        icon_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        c_layout.addWidget(icon_label)

        pixmap = QPixmap(str(rice_paths.wait_icon))
        scaled_pixmap = pixmap.scaled(
            icon_label.size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        icon_label.setPixmap(scaled_pixmap)

        layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignVCenter)

        return container, c_layout, icon_label

    def get_next_index(self, c_index: int, window_items: list[WindowItem]) -> int:
        next_index: int = c_index + 1
        index = next_index % len(window_items)

        window = window_items[index]
        self.select_window_item(c_index, window)

        return index

    def get_prev_index(self, c_index: int, window_items: list[WindowItem]) -> int:
        prev_index: int = c_index
        index = prev_index % len(window_items) - 1

        window = window_items[index]
        self.select_window_item(c_index, window)

        return index

    def change_sel_window(self, window: WindowItem, c_index: int):
        pass

    def select_window(self, window: WindowItem):
        pass

    def deselect_window(self, window: WindowItem):
        pass

    def create_window_title_label(self, layout: QHBoxLayout) -> QLabel:
        style = (
            self.theme.window_search.window_item_container.item_frame.title_label
        )

        title_label: QLabel = QLabel()
        title_label.setObjectName("titleLabel")
        title_label.setText(style.preload_text)

        title_label.setWordWrap(True)

        title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout.addWidget(
            title_label, stretch=1, alignment=Qt.AlignmentFlag.AlignVCenter
        )

        return title_label

    def create_key_bind_label(self, layout: QHBoxLayout) -> QLabel:
        style = self.theme.window_search.window_item_container.item_frame.key_bind_lable

        key_bind_label: QLabel = QLabel()
        key_bind_label.setObjectName("keyBindLabel")
        key_bind_label.setText(" Alt + T")
        key_bind_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(key_bind_label, alignment=Qt.AlignmentFlag.AlignVCenter)

        return key_bind_label

    def hide(self, window_items: list[WindowItem]):
        for window_item in window_items:
            window_item.frame.setParent(None)

    def sort(self, window_items: list[WindowItem]):
        print(" sorting ")

        window_items.sort(key=lambda item: item.title)

        for i in range(len(window_items)):
            window_item = window_items[i]
            window_item.index = i + 1
            window_item.update_key_bind_label()

            self.scroller_layout.addWidget(window_item.frame)

    def reapply_theme(self, window_items: list[WindowItem]):
        for window_item in window_items:
            self.recolor_item(window_item)
            window_item.reload()

    def recolor_item(self, window_item: WindowItem):

        # print(f"changing: background_color: {style.background_color}")
        self.recolor_frame(window_item.frame)
        self.recolor_selection_indicator(window_item.selection_indicator)
        self.recolor_icon_label(
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
        self, container: QWidget, layout: QVBoxLayout, icon_label: QLabel
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
