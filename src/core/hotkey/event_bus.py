from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    helloRequested = Signal()


events = EventBus()
