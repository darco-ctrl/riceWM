from dataclasses import dataclass

from PySide6.QtWidgets import QFrame, QLineEdit, QVBoxLayout, QWidget


@dataclass
class Panel:
    frame: QFrame
    layout: QVBoxLayout


@dataclass
class SearchBox:
    container: QWidget
    layout: QVBoxLayout
    line_edit: QLineEdit
