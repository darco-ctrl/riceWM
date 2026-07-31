from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    wspToggleRequested = Signal()
    dataReloadRequested = Signal()

    reloadWSPThemeRequested = Signal()


events = EventBus()
