import pyvda
from pyvda.pyvda import VirtualDesktop

from src.core.events.event_bus import eventBus
from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner
from src.wm.desktop import Desktop


class WindowRegistry:
    def __init__(self, window_scanner: WindowScanner):
        self.window_scanner = window_scanner
        self.focused_window: WindowInfo | None = None

        self.desktop_windows: list[WindowInfo]
        self.windows: list[WindowInfo] = self.load_windows()

        self.connect_events()

    def load_windows(self) -> list[WindowInfo]:
        windows = self.window_scanner.get_windows_info()
        return windows

    def get_window_index(self, hwnd) -> int:
        for i in range(len(self.windows)):
            window = self.windows[i]

            if window.hwnd != hwnd:
                continue

            return i

        return -1

    def add_window(self, window: WindowInfo):
        self.windows.append(window)

    def get_window(self, hwnd) -> WindowInfo | None:
        window_index = self.get_window_index(hwnd)
        if window_index == -1:
            return None

        window = self.windows[window_index]

        return window

    def remove_window(self, hwnd) -> WindowInfo | None:
        window_index = self.get_window_index(hwnd)

        if window_index == -1:
            return None
        
        window = self.windows.pop(window_index)

        return window


    def connect_events(self):
        eventBus.vDesktopGoLeft.connect(self.v_desktop_go_left)
        eventBus.vDesktopGoRight.connect(self.v_desktop_go_right)
        eventBus.createNewVDesktop.connect(self.v_desktop_create_new)
        eventBus.deleteCurrentVDesktop.connect(self.v_desktop_delete_current)

        eventBus.windowGoLeft.connect(self.window_go_left)
        eventBus.windowGoRight.connect(self.window_go_right)

    def v_desktop_go_right(self):
        current = VirtualDesktop.current()
        desktop_count = len(pyvda.get_virtual_desktops())
    
        next_number = current.number % desktop_count + 1
    
        VirtualDesktop(next_number).go()
    
    
    def v_desktop_go_left(self):
        current = VirtualDesktop.current()
        desktop_count = len(pyvda.get_virtual_desktops())
    
        previous_number = (current.number - 2) % desktop_count + 1
    
        VirtualDesktop(previous_number).go()

    def v_desktop_create_new(self):
        print("v_desktop_create_new")

    def v_desktop_delete_current(self):
        print("v_desktop_delete_current")

    def window_go_left(self):
        print("window_go_left")

    def window_go_right(self):
        print("window_go_right")
