from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    windowSwitchPanelRequested = Signal()


events = EventBus()
