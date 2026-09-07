from PySide6.QtCore import QObject, Signal
from pyvda.pyvda import VirtualDesktop


class EventBus(QObject):
    requestRestartApplication: Signal = Signal()
    requestQuitApplication: Signal = Signal()

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

    vDesktopNotiferShow: Signal = Signal(VirtualDesktop)

    closeWindow: Signal = Signal()
    maximizeWindow: Signal = Signal()
    minimizeWindow: Signal = Signal()
    fullscreenWindow: Signal = Signal()

    reloadWSPThemeRequested: Signal = Signal()
    
    

eventBus = EventBus()
