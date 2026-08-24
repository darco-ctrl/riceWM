from typing import cast

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

import src.app.paths as rice_paths
from src.core.config.config import Config
from src.core.theme.theme import Theme
from src.models.window import WindowInfo
from src.ui.window_search.window_item.model import WindowItem
from src.ui.window_search.window_item.theme_applier import WinItemThemeApplier


class WinItemConstructor:
    def __init__(
        self, 
        config: Config, 
        theme: Theme,
        theme_applier: WinItemThemeApplier
    ):
        self.config: Config = config
        self.theme: Theme = theme
        self.theme_applier: WinItemThemeApplier = theme_applier
        
    def update_window_items(self, items: list[int], windows: list[WindowItem]):

        for item_index in items:
            windows[item_index].update()

    def delete_window_items(self, items: list[int], window_items: list[WindowItem]):
        for index in sorted(items, reverse=True):
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
            self.theme_applier.recolor_item(window_item=window_item)

        return window_items

    
    def create_window_item(
        self, count: int, window_info: WindowInfo
    ) -> WindowItem:  # m layout is main scroller layout
        frame = self.create_item_frame()
        f_layout: QHBoxLayout = cast(QHBoxLayout, frame.layout())

        selection_indicator = self.create_selection_indicator(f_layout)
        outer_layout, icon_container, c_layout, icon_label = self.create_icon_label(f_layout)
        title_label = self.create_window_title_label(f_layout)
        key_bind_label = self.create_key_bind_label(f_layout)
        
        window_item: WindowItem = WindowItem(
            hwnd=window_info.hwnd,
            name=window_info.name,
            title=window_info.title,
            icon_path=window_info.icon_path,
            index=count,
            frame=frame,
            key_bind_label=key_bind_label,
            icon_layout=outer_layout,
            icon_container=icon_container,
            c_layout=c_layout,
            icon_label=icon_label,
            selection_indicator=selection_indicator,
            title_label=title_label
        )

        window_item.update_indicator()

        return window_item

    def create_item_frame(self) -> QFrame:
        style = self.theme.window_search.window_item.frame_style

        frame = QFrame()
        frame.setObjectName("itemFrame")
        frame.setFixedHeight(style.height)

        frame_layout: QHBoxLayout = QHBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        return frame

    def create_selection_indicator(self, layout: QHBoxLayout) -> QWidget:
        style = self.theme.window_search.window_item.selection_indicator

        indicator: QWidget = QWidget()
        indicator.setObjectName("selectionIndicator")

        layout.addWidget(indicator, alignment=Qt.AlignmentFlag.AlignVCenter)

        return indicator

    def create_icon_label(
        self, layout: QHBoxLayout
    ) -> tuple[QVBoxLayout, QWidget, QVBoxLayout, QLabel]:
        style = self.theme.window_search.window_item.icon_container

        

        container: QWidget = QWidget()
        container.setObjectName("iconContainer")
        container.setFixedSize(QSize(
            style.dimension.width, style.dimension.height
        ))

        outer_container: QWidget = QWidget()
        outer_layout: QVBoxLayout = QVBoxLayout(outer_container)
        outer_layout.setContentsMargins(
            style.container_margin[0],
            style.container_margin[0],
            style.container_margin[0],
            style.container_margin[0]
        )

        outer_layout.addWidget(
            container,
            alignment=Qt.AlignmentFlag.AlignVCenter
        )
        
        c_layout: QVBoxLayout = QVBoxLayout(container)

        icon_width = (
            style.dimension.width - style.margin[0] - style.margin[2]
        )
        icon_height = (
            style.dimension.height - style.margin[1] - style.margin[3]
        )

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

        layout.addWidget(outer_container)

        return outer_layout, container, c_layout, icon_label

    def create_window_title_label(self, layout: QHBoxLayout) -> QLabel:
        style = (
            self.theme.window_search.window_item.title_label
        )

        title_label: QLabel = QLabel()
        title_label.setObjectName("titleLabel")
        title_label.setText("Loading . . .")

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
        style = self.theme.window_search.window_item.keybind_label

        key_bind_label: QLabel = QLabel()
        key_bind_label.setObjectName("keyBindLabel")
        key_bind_label.setText(" Alt + T")
        key_bind_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(key_bind_label, alignment=Qt.AlignmentFlag.AlignVCenter)

        return key_bind_label
