from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QLabel, QSizePolicy


class ElidedLabel(QLabel):
    def __init__(self, text:str="", parent=None):
        super().__init__(parent)

        self.setWordWrap(False)
        self.setMinimumWidth(0)

        self.setSizePolicy(
            QSizePolicy.Policy.Ignored,
            QSizePolicy.Policy.Fixed
        )

        self._raw_text: str = text
        self.setText(text)

    def set_elided_text(self, text: str):
        self._raw_text = text
        self.update_elision()

    def update_elision(self):
        metrics = QFontMetrics(self.font())
        
        elided = metrics.elidedText(
            self._raw_text, 
            Qt.TextElideMode.ElideRight, 
            self.width()
        )
        super().setText(elided)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_elision()
