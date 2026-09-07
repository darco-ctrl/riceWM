from pyvda.pyvda import AppView, VirtualDesktop
import pywintypes
import win32con
import win32gui

from src.core.events.event_bus import eventBus
from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner
from src.wm.registry import WindowRegistry


class WindowController:
    def __init__(self, registry, window_scanner):
        self.connect_window_events()

        self.window_scanner: WindowScanner = window_scanner
        self.registry: WindowRegistry = registry

    def connect_window_events(self):
        _ = eventBus.focusWindow.connect(self.focus_window)

    def focus_window(self, hwnd: int):
        try:
            window_view: AppView = AppView(hwnd=hwnd)

            desktop: VirtualDesktop = window_view.desktop
            desktop.go()

            self.set_focus(hwnd)
        except Exception as e:
            print(f"Failed to retrive Virtual Desktop,\n error: {e}")

    def minimize(self, hwnd: int):
        print("minimizing window")
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    def maximize(self, hwnd: int):
        self.set_focus(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def fullscreen(self, hwnd: int):
        win32gui.ShowWindow(hwnd, win32con.SHOW_FULLSCREEN)

    def set_focus(self, hwnd: int):

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
            print(f"Could not focus hwnd {hwnd}: {error}")
