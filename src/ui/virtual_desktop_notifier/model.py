

from dataclasses import dataclass

from PySide6.QtWidgets import QFrame, QLabel, QWidget


@dataclass
class VirtualDesktopNotiferUI:
    window: QWidget
    frame: QFrame
    label: QLabel