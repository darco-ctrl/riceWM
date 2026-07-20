
from PySide6.QtWidgets import QFrame

class WindowData():

    def __init__(self, name: str, title: str, frame: QFrame) -> None:
        self.name = name
        self.title = title
        self.frame = frame
