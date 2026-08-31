from PySide6.QtCore import QObject, Signal

from src.models.window import WindowInfo


class EventBus(QObject):
    windowCreated: Signal = Signal(int)
    windowShow: Signal = Signal(int)
    windowDeystroyed: Signal = Signal(int)
    windowMaximized: Signal = Signal(int)
    windowMinimized: Signal = Signal(int)
    windowRestore: Signal = Signal(int)
    windowFullscreen: Signal = Signal(int)
    windowFocused: Signal = Signal(int)

    wspToggleRequested: Signal = Signal()
    wspCloseRequested: Signal = Signal()
    dataReloadRequested: Signal = Signal()
    itemSelectDown: Signal = Signal()
    itemSelectUp: Signal = Signal()
    wspFocusSelectedWindow: Signal = Signal()

    updateWindowItemList: Signal = Signal(list)

    createNewVDesktop: Signal = Signal()
    deleteCurrentVDesktop: Signal = Signal()
    vDesktopGoLeft: Signal = Signal()
    vDesktopGoRight: Signal = Signal()
    focusWindow: Signal = Signal(int)

    windowGoLeft: Signal = Signal()
    windowGoRight: Signal = Signal()

    reloadWSPThemeRequested: Signal = Signal()
    

eventBus = EventBus()
