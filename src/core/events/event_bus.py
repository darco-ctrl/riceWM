from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    windowCreated = Signal(int)
    windowDeystroyed = Signal(int)
    windowMaximized = Signal(int)
    windowMinimized = Signal(int)
    windowRestore = Signal(int)
    windowFullscreen = Signal(int)
    windowFocused = Signal(int)

    wspToggleRequested = Signal()
    dataReloadRequested = Signal()

    reloadWSPThemeRequested = Signal()


eventBus = EventBus()
