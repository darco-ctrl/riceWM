import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

user32.IsZoomed.argtypes = [wintypes.HWND]
user32.IsZoomed.restype = wintypes.BOOL

user32.IsIconic.argtypes = [wintypes.HWND]
user32.IsIconic.restype = wintypes.BOOL

from src.core.events.event_bus import eventBus

user32 = ctypes.windll.user32

EVENT_SYSTEM_FOREGROUND = 0x0003
EVENT_SYSTEM_MINIMIZESTART = 0x0016
EVENT_SYSTEM_MINIMIZEEND = 0x0017

EVENT_OBJECT_CREATE = 0x8000
EVENT_OBJECT_DESTROY = 0x8001
EVENT_OBJECT_LOCATIONCHANGE = 0x800B

OBJID_WINDOW = 0
WINEVENT_OUTOFCONTEXT = 0x0000

WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.HWND,
    wintypes.LONG,
    wintypes.LONG,
    wintypes.DWORD,
    wintypes.DWORD,
)


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


MONITOR_DEFAULTTONEAREST = 2

user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(RECT)]
user32.GetWindowRect.restype = wintypes.BOOL

user32.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
user32.MonitorFromWindow.restype = wintypes.HANDLE


class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", RECT),
        ("rcWork", RECT),
        ("dwFlags", wintypes.DWORD),
    ]


user32.GetMonitorInfoW.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(MONITORINFO),
]
user32.GetMonitorInfoW.restype = wintypes.BOOL


class WindowListener:
    def __init__(self):
        self._callback = WinEventProcType(self._win_event_proc)
        self._hooks = []

        for event in (
            EVENT_SYSTEM_FOREGROUND,
            EVENT_SYSTEM_MINIMIZESTART,
            EVENT_SYSTEM_MINIMIZEEND,
            EVENT_OBJECT_CREATE,
            EVENT_OBJECT_DESTROY,
            EVENT_OBJECT_LOCATIONCHANGE,
        ):
            hook = user32.SetWinEventHook(
                event,
                event,
                0,
                self._callback,
                0,
                0,
                WINEVENT_OUTOFCONTEXT,
            )

            self._hooks.append(hook)

    def _win_event_proc(
        self,
        hook,
        event,
        hwnd,
        id_object,
        id_child,
        thread,
        time,
    ):
        if id_object != OBJID_WINDOW or not hwnd:
            return

        self._handle_event(event, hwnd)

    def _handle_event(self, event, hwnd):
        if event == EVENT_OBJECT_CREATE:
            eventBus.windowCreated.emit(hwnd)

        elif event == EVENT_OBJECT_DESTROY:
            eventBus.windowDeystroyed.emit(hwnd)

        elif event == EVENT_SYSTEM_FOREGROUND:
            eventBus.windowFocused.emit(hwnd)

        elif event == EVENT_SYSTEM_MINIMIZESTART:
            eventBus.windowMinimized.emit(hwnd)

        elif event == EVENT_SYSTEM_MINIMIZEEND:
            eventBus.windowRestore.emit(hwnd)

        elif event == EVENT_OBJECT_LOCATIONCHANGE:
            if user32.IsIconic(hwnd):
                return

            if self._is_fullscreen(hwnd):
                eventBus.windowFullscreen.emit(hwnd)

            elif user32.IsZoomed(hwnd):
                eventBus.windowMaximized.emit(hwnd)

            else:
                eventBus.windowRestore.emit(hwnd)

    def _is_fullscreen(self, hwnd):
        window_rect = RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(window_rect))

        monitor = user32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)

        monitor_info = MONITORINFO()
        monitor_info.cbSize = ctypes.sizeof(MONITORINFO)

        user32.GetMonitorInfoW(monitor, ctypes.byref(monitor_info))

        monitor_rect = monitor_info.rcMonitor

        return (
            window_rect.left == monitor_rect.left
            and window_rect.top == monitor_rect.top
            and window_rect.right == monitor_rect.right
            and window_rect.bottom == monitor_rect.bottom
        )
