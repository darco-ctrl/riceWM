import win32gui
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from src.models.elided_label import ElidedLabel
from src.models.window import WindowInfo


class WindowItem:
    def __init__(
        self,
        window_info: WindowInfo,
        frame: QFrame,
        selection_indicator_parent: QWidget,
        selection_indicator: QFrame,
        icon_outer_layout: QVBoxLayout,
        icon_container: QWidget,
        icon_inner_layout: QVBoxLayout,
        icon_label: QLabel,
        title_label: ElidedLabel
    ) -> None:
        self.info: WindowInfo = window_info
        self.frame: QFrame = frame
        self.selection_indicator_parent: QWidget = selection_indicator_parent
        self.selection_indicator: QFrame = selection_indicator
        self.icon_background: QVBoxLayout = icon_outer_layout
        self.icon_container: QWidget = icon_container
        self.icon_layout: QVBoxLayout = icon_inner_layout
        self.icon_label: QLabel = icon_label
        self.title_label: ElidedLabel = title_label

        self.is_selected: bool = False
        self.is_focus_window: bool = False


    def set_selected(self, selected: bool):
        self.is_selected = selected

        self.update_indicator()

    def update_indicator(self):
        if not self.selection_indicator:
            return
            
        if self.is_selected:

            self.selection_indicator_parent.setVisible(True)
            # self.selection_indicator.setStyleSheet(f"""
            #selectionIndicator {{
                # background-color: {self.indicator_color};
            # }}
            # """)
            
        else:

            self.selection_indicator_parent.setVisible(False)
            # self.selection_indicator.setStyleSheet("""
            # selectionIndicator {
                # background-color: transparent;
            # }
            # """)

    def set_focused(self, focused: bool):
        self.is_focus_window = focused

    def load(self):
        self.update_title_label()
        self.update_window_icon()

    def reload(self):
        self.load()

    def update(self):

        self.info.title = win32gui.GetWindowText(self.info.hwnd)

        self.update_title_label()
        self.update_indicator()

    def delete(self):
        self.frame.deleteLater()

    def update_title_label(self):

        if not self.title_label:
            self.title_label.set_elided_text(
                text="Window title not available :("
            )
            return

        self.title_label.set_elided_text(
            text=self.info.title
        )

    def update_window_icon(self):

        pixmap = QPixmap(self.info.icon_path)
        scaled_pixmap = pixmap.scaled(
            self.icon_label.size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.icon_label.setPixmap(scaled_pixmap)
