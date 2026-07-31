from typing import cast

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLayout, QVBoxLayout, QWidget

import app.paths as rice_paths
from data.config.config import Config
from data.theme.theme import Theme
from widgets.window_switch_panel.window_item import WindowItem
from widgets.window_switch_panel.window_state_reconciler import (
    StateReconciler,
    TaskList,
)
from windows.window import WindowInfo
from windows.window_scanner import WindowScanner


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

    def sync_window_items(self, window_items: list[WindowItem]):

        task_list: TaskList = self.state_reconciler.get_plan(window_items)

        self.update_window_items(task_list.update, window_items)
        self.create_window_items(task_list.new, window_items)
        self.delete_window_items(task_list.delete, window_items)

        self.sort(window_items)

    def update_window_items(self, items: list[int], windows: list[WindowItem]):

        for item_index in items:
            windows[item_index].update()

    def delete_window_items(self, items: list[int], window_items: list[WindowItem]):

        for index in sorted(items, reverse=True):
            print(f"removing index: {index}")

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
        icon_label = self.create_icon_label(f_layout)
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
            icon_label=icon_label,
            selection_indicator=selection_indicator,
            title_label=title_label,
        )

        return window_item

    def create_item_frame(self) -> QFrame:
        style = self.theme.window_switch_panel.window_item_frame

        frame = QFrame()
        frame.setFixedHeight(style.height)

        frame_layout: QHBoxLayout = QHBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        return frame

    def create_selection_indicator(self, layout: QHBoxLayout) -> QWidget:
        style = self.theme.window_switch_panel.window_item_frame.selection_indicator

        indicator: QWidget = QWidget()

        layout.addWidget(indicator)

        return indicator

    def create_icon_label(self, layout: QHBoxLayout) -> QLabel:
        style = self.theme.window_switch_panel.window_item_frame.icon_label

        icon_label: QLabel = QLabel()
        icon_label.setFixedSize(QSize(style.width, style.height))

        pixmap = QPixmap(str(rice_paths.wait_icon))
        scaled_pixmap = pixmap.scaled(
            icon_label.size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        icon_label.setPixmap(scaled_pixmap)

        layout.addWidget(icon_label)

        return icon_label

    def create_window_title_label(self, layout: QHBoxLayout) -> QLabel:
        style = self.theme.window_switch_panel.window_item_frame.title_label

        title_label: QLabel = QLabel()
        title_label.setText(style.preload_text)

        layout.addWidget(title_label, stretch=1)

        return title_label

    def create_key_bind_label(self, layout: QHBoxLayout) -> QLabel:
        style = self.theme.window_switch_panel.window_item_frame.key_bind_lable

        key_bind_label: QLabel = QLabel()
        key_bind_label.setText(" Alt + T")
        key_bind_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(key_bind_label)

        return key_bind_label

    def hide(self, window_items: list[WindowItem]):
        for window_item in window_items:
            window_item.frame.setParent(None)

    def sort(self, window_items: list[WindowItem]):
        print(" sorting ")

        window_items.sort(key=lambda item: item.title)

        for window_item in window_items:
            self.scroller_layout.addWidget(window_item.frame)

    def reapply_theme(self, window_items: list[WindowItem]):
        for window_item in window_items:
            self.recolor_item(window_item)

    def recolor_item(self, window_item: WindowItem):
        style = self.theme.window_switch_panel.window_item_frame

        print(f"changing: background_color: {style.background_color}")
        self.recolor_frame(window_item.frame)
        self.recolor_selection_indicator(window_item.selection_indicator)
        self.recolor_icon_label(window_item.icon_label)
        self.recolor_title_label(window_item.title_label)
        self.recolor_keybind_label(window_item.key_bind_label)

    def recolor_frame(self, frame: QWidget):
        frame_style = self.theme.window_switch_panel.window_item_frame

        frame.setFixedHeight(frame_style.height)
        frame.setStyleSheet(f"""
            background-color: {frame_style.background_color}
        """)
        frame_layout: QHBoxLayout = cast(QHBoxLayout, frame.layout())
        frame_layout.setContentsMargins(
            frame_style.contents_margin[0],
            frame_style.contents_margin[1],
            frame_style.contents_margin[2],
            frame_style.contents_margin[3],
        )

    def recolor_selection_indicator(self, selection_indicator: QWidget):
        style = self.theme.window_switch_panel.window_item_frame.selection_indicator

        selection_indicator.setFixedSize(QSize(style.width, style.height))
        selection_indicator.setStyleSheet(f"""
            background-color: {style.background_color};
        """)

    def recolor_icon_label(self, icon_label: QLabel):
        style = self.theme.window_switch_panel.window_item_frame.icon_label

        icon_label.setFixedSize(QSize(style.width, style.height))

    def recolor_title_label(self, label: QLabel):
        style = self.theme.window_switch_panel.window_item_frame.title_label

        label.setStyleSheet(f"""
            background-color: {style.background_color};
            color: {style.color};
        """)

    def recolor_keybind_label(self, label: QLabel):
        style = self.theme.window_switch_panel.window_item_frame.key_bind_lable

        label.setFixedSize(QSize(style.width, style.height))
        label.setStyleSheet(f"""
            background-color: {style.background_color};
            color: {style.color}
        """)
