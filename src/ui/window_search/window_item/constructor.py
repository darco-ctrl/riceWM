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
from src.ui.window_search.window_item.helper import WindowItemHelper
from src.ui.window_search.window_item.window_item import WindowItem
from src.ui.window_search.window_item.theme_applier import WinItemThemeApplier


class WinItemConstructor:
    def __init__(
        self, 
        scroll_layout: QVBoxLayout,
        config: Config, 
        theme: Theme,
        theme_applier: WinItemThemeApplier,
        helper: WindowItemHelper
    ):
        self.config: Config = config
        self.theme: Theme = theme

        self.scroll_layout: QVBoxLayout = scroll_layout
        self.theme_applier: WinItemThemeApplier = theme_applier
        self.helper: WindowItemHelper = helper
        
    def update_window_items(self, items: list[int], windows: list[WindowItem]):

        for item_index in items:
            if item_index >= len(windows):
                continue
            windows[item_index].update()

    def delete_windows_info(
        self, 
        items: list[int],
        windows_item: list[WindowItem], 
        windows_info: list[WindowInfo]
    ):
        for index in sorted(items, reverse=True):
            self.delete_window_info(
                index=index,
                windows_info=windows_info,
                windows_item=windows_item
            )

    def delete_window_info(
        self, 
        index: int, 
        windows_item: list[WindowItem],
        windows_info: list[WindowInfo]
    ):
        window_item: WindowItem = windows_item[index]
        info_index = self.helper.get_info_index(
            info=window_item.info,
            list=windows_info
        )
        if info_index != -1:
            _ = windows_info.pop(info_index)
            _ = windows_item.pop(index)
        
        window_item.delete()
        del window_item

    def create_window_items(
        self,
        new_info: list[WindowInfo],
        window_items: list[WindowItem]
    ):
        keybind_count = 0
        for i in range(len(new_info)):
            keybind_count += 1
            
            window_info: WindowInfo = new_info[i]
            # print(f"{i}. window info : {window_info.title}")
            _ = self.create_window_item(
                count=keybind_count,
                window_info=window_info,
                window_items=window_items
            )

    def create_new_window_items(
        self, 
        new_info: list[WindowInfo], 
        window_items: list[WindowItem],
        current_info: list[WindowInfo],
    ):
        count = 1

        new_info.sort(key=lambda item: item.title)
        for window_info in new_info:
            _ = self.create_window_item(
                count=count,
                window_info=window_info,
                window_items=window_items
            )

            count += 1
            
            current_info.append(window_info)
    
    def create_window_item(
        self, 
        count: int, 
        window_info: WindowInfo,
        window_items: list[WindowItem]
    ) -> WindowItem:  # m layout is main scroller layout
        frame = self.create_item_frame()
        f_layout: QHBoxLayout = cast(QHBoxLayout, frame.layout())

        parent, selection_indicator = self.create_selection_indicator(f_layout)
        outer_layout, icon_container, c_layout, icon_label = self.create_icon_label(f_layout)
        title_label = self.create_window_title_label(f_layout)
        key_bind_label = self.create_key_bind_label(f_layout)
        
        window_item: WindowItem = WindowItem(
            window_info=window_info,
            index=count,
            frame=frame,
            key_bind_label=key_bind_label,
            icon_outer_layout=outer_layout,
            icon_container=icon_container,
            icon_inner_layout=c_layout,
            icon_label=icon_label,
            selection_indicator_parent=parent,
            selection_indicator=selection_indicator,
            title_label=title_label
        )
        

        window_item.update_indicator()
        window_item.load()

        window_items.append(window_item)

        self.theme_applier.recolor_item(window_item=window_item)
        self.scroll_layout.addWidget(window_item.frame)
        
        return window_item

    def create_item_frame(self) -> QFrame:
        style = self.theme.window_search.window_item.frame_style

        frame = QFrame()
        frame.setObjectName("itemFrame")
        frame.setFixedHeight(style.height)

        frame_layout: QHBoxLayout = QHBoxLayout(frame)
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        return frame

    def create_selection_indicator(
        self, layout: QHBoxLayout
    ) -> tuple[QWidget, QFrame]:
        style = self.theme.window_search.window_item.selection_indicator

        container: QWidget = QWidget()
        c_layout: QVBoxLayout = QVBoxLayout(container)

        c_layout.setContentsMargins(
            style.margin[0],
            style.margin[1],
            style.margin[2],
            style.margin[3],
        )
        
        indicator: QFrame = QFrame()
        indicator.setObjectName("selectionIndicator")

        c_layout.addWidget(
            indicator, alignment=Qt.AlignmentFlag.AlignVCenter
        )

        layout.addWidget(container)

        return container, indicator

    def create_icon_label(
        self, layout: QHBoxLayout
    ) -> tuple[QVBoxLayout, QWidget, QVBoxLayout, QLabel]:
        style = self.theme.window_search.window_item.icon_container

        

        container: QWidget = QWidget()
        container.setObjectName("iconContainer")
        container.setFixedSize(QSize(
            style.dimension.x, style.dimension.y
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
            style.dimension.x - style.margin[0] - style.margin[2]
        )
        icon_height = (
            style.dimension.y - style.margin[1] - style.margin[3]
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

    def delete_all_winitems(self, window_items: list[WindowItem]):
        for i in range(len(window_items)):
            window_item =  window_items[i]
            window_item.delete()

        window_items.clear()
