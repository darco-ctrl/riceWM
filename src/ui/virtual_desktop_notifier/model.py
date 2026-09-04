

from dataclasses import dataclass

from PySide6.QtWidgets import QLabel


@dataclass
class VirtualDesktopNotiferUI:
    label: QLabel
