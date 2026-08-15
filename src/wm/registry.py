import win32gui
import win32api
import win32con

import pyvda
from pynput.keyboard import Controller, Key
from pyvda.pyvda import VirtualDesktop

from src.core.events.event_bus import eventBus
from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner
from src.wm.desktop import Desktop


class WindowRegistry:
    def __init__(self, window_scanner: WindowScanner):
        self.window_scanner = window_scanner
        self.focused_window: WindowInfo | None = None

        self.focus_window_index: int = -1
        self.desktop_windows: list[WindowInfo]
        self.windows: list[WindowInfo] = self.load_windows()
        self.update_window_list()

        self.keyboard = Controller()

        self.connect_events()

    def connect_events(self):
        eventBus.vDesktopGoLeft.connect(self.v_desktop_go_left)
        eventBus.vDesktopGoRight.connect(self.v_desktop_go_right)
        eventBus.createNewVDesktop.connect(self.v_desktop_create_new)
        eventBus.deleteCurrentVDesktop.connect(self.v_desktop_delete_current)


    def load_windows(self) -> list[WindowInfo]:
        windows = self.window_scanner.get_windows_info()
        return windows

    def update_window_list(self):
        # print("updating window list")
        self.desktop_windows = []
        
        desktop = VirtualDesktop.current()
        hwnds = self.window_scanner.get_desktops_hwnds(desktop)

        for i in range(len(self.windows)):
            window = self.windows[i]
            if not window.hwnd in hwnds:
                continue

            focus_hwnd = win32gui.GetForegroundWindow()
            if focus_hwnd == window.hwnd:
                self.focus_window_index = i

            self.desktop_windows.append(window)

    def get_window_index(self, hwnd: int) -> int:
        for i in range(len(self.windows)):
            window = self.windows[i]

            if window.hwnd != hwnd:
                continue

            return i

        return -1

    def add_window(self, window: WindowInfo):
        self.windows.append(window)

    def get_window(self, hwnd) -> WindowInfo | None:
        window_index: int = self.get_window_index(hwnd)
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

    def v_desktop_go_right(self):
        current = VirtualDesktop.current()
        desktop_count = len(pyvda.get_virtual_desktops())
    
        next_number = current.number % desktop_count + 1
    
        VirtualDesktop(next_number).go()

        self.update_window_list()
    
    
    def v_desktop_go_left(self):
        current = VirtualDesktop.current()
        desktop_count = len(pyvda.get_virtual_desktops())
    
        previous_number = (current.number - 2) % desktop_count + 1
    
        VirtualDesktop(previous_number).go()
        self.update_window_list()

    def v_desktop_create_new(self):
        desktop = VirtualDesktop.create()
        desktop.go()
        self.update_window_list()

    def v_desktop_delete_current(self):
        desktops = pyvda.get_virtual_desktops()
        current = VirtualDesktop.current()

        current_index = current.number

        if len(desktops) > current_index:
            if current_index > 0:
                fallback = desktops[current_index - 1]
            else:
                fallback = desktops[current_index + 1]

        # print(f"fallback: {current_index}")
        current.remove(fallback)
        self.update_window_list()

    def get_left_window(self) -> WindowInfo | None:
        # This is for future
        pass
            
    def get_right_window(self) -> WindowInfo | None:
        # This is for future
        pass

    def print_all(self):
        for i in range(len(self.desktop_windows)):
            win = self.desktop_windows[i]
            text = f"{i+1}. {win.hwnd}: {win.title}."
            print(text)
