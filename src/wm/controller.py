import pywintypes
import win32con
import win32gui
from pyvda.pyvda import AppView, VirtualDesktop

from app.event_logger import EventLogger, LogEventType
from src.core.events.event_bus import eventBus
from src.services.window.scanner import WindowScanner
from src.wm.registry import WindowRegistry


class WindowController:
    """Controls window states and operations such as minimizing, maximizing, restoring, and closing."""
    
    def __init__(self, logger: EventLogger, registry, window_scanner):
        self._logger = logger
        self._window_scanner: WindowScanner = window_scanner
        self._registry: WindowRegistry = registry
        
        self._connect_window_events()

    def _connect_window_events(self):
        _ = eventBus.focusWindow.connect(self._focus_window)
        _ = eventBus.closeWindow.connect(self._close_Window)
        _ = eventBus.restoreWindow.connect(self._restore_window)
        _ = eventBus.maximizeWindow.connect(self._maximize_window)
        _ = eventBus.minimizeWindow.connect(self._minimize_window)

    def _close_Window(self):
        hwnd = self._get_focused_window()

        if not hwnd:
            return

        self._close(hwnd)

    def _minimize_window(self):
        hwnd = self._get_focused_window()

        if not hwnd:
            return

        self._minimize(hwnd)

    def _maximize_window(self):
        hwnd = self._get_focused_window()

        if not hwnd:
            return

        self._maximize(hwnd)

    def _restore_window(self):
        hwnd = self._get_focused_window()

        if not hwnd:
            return

        self._restore(hwnd)

    def _get_focused_window(self) -> int:
        hwnd: int = win32gui.GetForegroundWindow()

        if self._window_scanner.is_regular_window(hwnd):
            return hwnd
            
        self._logger.log(
            log_type=LogEventType.INFO,
            message="The window tried to focus is not regular window"
        )
        return 0

    def _focus_window(self, hwnd: int):
        window_view: AppView = AppView(hwnd=hwnd)

        desktop: VirtualDesktop = window_view.desktop
        desktop.go()

        self._set_focus(hwnd)
        self._maximize(hwnd)

    def _close(self, hwnd: int):
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    def _minimize(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def _restore(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    def _maximize(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def _set_focus(self, hwnd: int):

        foreground_hwnd = win32gui.GetForegroundWindow()

        if not win32gui.IsWindow(hwnd):
            return

        if foreground_hwnd == hwnd:
            return

        # print(prt_text_hwnd)
        # print(prt_text_title)
        # print(f"Target hwnd: {hwnd}")
        # print(f"Target title: {win32gui.GetWindowText(hwnd)}")

        try:
            win32gui.SetForegroundWindow(hwnd)
        except pywintypes.error as error:
            self._logger.log(
                log_type=LogEventType.ERROR,
                message=f"Could not focus HWND: {hwnd}, error: {error}"
            )
