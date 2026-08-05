from dataclasses import dataclass

from PySide6.QtWidgets import QLineEdit, QVBoxLayout, QWidget


@dataclass
class Panel:
    widget: QWidget
    layout: QVBoxLayout


@dataclass
class SearchBox:
    container: QWidget
    layout: QVBoxLayout
    line_edit: QLineEdit
