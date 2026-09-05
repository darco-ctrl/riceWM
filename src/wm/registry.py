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

        self.keyboard = Controller()

        self.connect_events()

    def connect_events(self):
        _ = eventBus.vDesktopGoLeft.connect(self.v_desktop_go_left)
        _ = eventBus.vDesktopGoRight.connect(self.v_desktop_go_right)
        _ = eventBus.createNewVDesktop.connect(self.v_desktop_create_new)
        _ = eventBus.deleteCurrentVDesktop.connect(self.v_desktop_delete_current)


    def load_windows(self) -> list[WindowInfo]:
        windows = self.window_scanner.get_windows_info()
        return windows

    def v_desktop_go_right(self):
        current = VirtualDesktop.current()
        desktop_count = len(pyvda.get_virtual_desktops())
    
        next_number = current.number % desktop_count + 1
    
        self.go_to_desktop(VirtualDesktop(next_number))

    
    def v_desktop_go_left(self):
        current = VirtualDesktop.current()
        desktop_count = len(pyvda.get_virtual_desktops())
    
        previous_number = (current.number - 2) % desktop_count + 1
    
        self.go_to_desktop(VirtualDesktop(previous_number))

    def v_desktop_create_new(self):
        desktop = VirtualDesktop.create()

        self.go_to_desktop(desktop)

    def v_desktop_delete_current(self):
        desktops = pyvda.get_virtual_desktops()
        current = VirtualDesktop.current()

        current_index = current.number

        fallback: VirtualDesktop
        if len(desktops) > current_index:
            if current_index > 0:
                fallback = desktops[current_index - 1]
            else:
                fallback = desktops[current_index + 1]

        # print(f"fallback: {current_index}")
            current.remove(fallback)

    def go_to_desktop(self, desktop: VirtualDesktop):
        desktop.go()

        
        
        eventBus.vDesktopNotiferShow.emit(desktop)

    def get_left_window(self) -> WindowInfo | None:
        # This is for future
        pass
            
    def get_right_window(self) -> WindowInfo | None:
        # This is for future
        pass
