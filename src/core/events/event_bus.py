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
    wspFocusSelectedWindow = Signal()

    createNewVDesktop = Signal()
    deleteCurrentVDesktop = Signal()
    vDesktopGoLeft = Signal()
    vDesktopGoRight = Signal()
    focusWindow = Signal(int)

    windowGoLeft = Signal()
    windowGoRight = Signal()

    reloadWSPThemeRequested = Signal()
    

eventBus = EventBus()
