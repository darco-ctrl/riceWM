import win32gui
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class WindowItem:
    def __init__(
        self,
        hwnd: int,
        name: str,
        title: str,
        icon_path: str,
        index: int,
        frame: QFrame,
        selection_indicator: QWidget,
        icon_layout: QVBoxLayout,
        icon_container: QWidget,
        c_layout: QVBoxLayout,
        icon_label: QLabel,
        title_label: QLabel,
        key_bind_label: QLabel
    ) -> None:
        self.hwnd: int = hwnd
        self.name: str = name
        self.title: str = title
        self.icon_path: str = icon_path
        self.index: int = index
        self.frame: QFrame = frame
        self.selection_indicator: QWidget = selection_indicator
        self.icon_layout: QWidget = icon_layout
        self.icon_container: QWidget = icon_container
        self.icon_layout: QVBoxLayout = c_layout
        self.icon_label: QLabel = icon_label
        self.title_label: QLabel = title_label
        self.key_bind_label: QLabel = key_bind_label

        self.is_selected: bool = False
        self.is_focus_window: bool = False

    def set_selected(self, selected: bool):
        self.is_selected = selected

        self.update_indicator()

    def update_indicator(self):
        if not self.selection_indicator:
            return
            
        if self.is_selected:

            self.selection_indicator.setVisible(True)
            # self.selection_indicator.setStyleSheet(f"""
            #selectionIndicator {{
                # background-color: {self.indicator_color};
            # }}
            # """)
            
        else:

            self.selection_indicator.setVisible(False)
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
        self.update_key_bind_label()

    def reload(self):
        self.load()

    def update(self):

        self.title = win32gui.GetWindowText(self.hwnd)

        self.update_title_label()
        self.update_indicator()

    def delete(self):
        self.frame.deleteLater()

    def update_title_label(self):

        if not self.title_label:
            print("Title Label of window item is Empty refrence.")

        self.title_label.setText(self.title)

    def update_window_icon(self):

        pixmap = QPixmap(self.icon_path)
        scaled_pixmap = pixmap.scaled(
            self.icon_label.size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.icon_label.setPixmap(scaled_pixmap)

    def update_key_bind_label(self):
        index = self.index
        if self.index == 10:
            index = 0

        if self.index < 10:
            text = f"Alt + {index}"
            self.key_bind_label.setText(text)
