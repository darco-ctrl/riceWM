

from dataclasses import dataclass

from PySide6.QtWidgets import QFrame, QLabel, QWidget


@dataclass
class VirtualDesktopNotiferUI:
    frame: QFrame
    label: QLabel
