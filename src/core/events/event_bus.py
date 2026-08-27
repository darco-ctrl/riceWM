from PySide6.QtCore import QObject, Signal


class EventBus(QObject):
    windowCreated = Signal(int)
    windowShow = Signal(int)
    windowDeystroyed = Signal(int)
    windowMaximized = Signal(int)
    windowMinimized = Signal(int)
    windowRestore = Signal(int)
    windowFullscreen = Signal(int)
    windowFocused = Signal(int)

    wspToggleRequested = Signal()
    wspCloseRequested = Signal()
    dataReloadRequested = Signal()
    itemSelectDown = Signal()
    itemSelectUp = Signal()

    createNewVDesktop = Signal()
    deleteCurrentVDesktop = Signal()
    vDesktopGoLeft = Signal()
    vDesktopGoRight = Signal()

    windowGoLeft = Signal()
    windowGoRight = Signal()

    reloadWSPThemeRequested = Signal()


eventBus = EventBus()
