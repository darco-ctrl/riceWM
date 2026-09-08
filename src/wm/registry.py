import pyvda
from pynput.keyboard import Controller
from pyvda.pyvda import VirtualDesktop

from src.core.config.config import Config
from src.core.events.event_bus import eventBus
from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner


class WindowRegistry:
    def __init__(
        self, 
        window_scanner: WindowScanner,
        config: Config
    ):
        self.config: Config = config
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
    
        next_number = self.get_next_index(
            current=current.number,
            total=desktop_count
        )

        if next_number == -1:
            return
    
        self.go_to_desktop(VirtualDesktop(next_number))

    
    def v_desktop_go_left(self):
        current = VirtualDesktop.current()
        desktop_count = len(pyvda.get_virtual_desktops())
    
        previous_number = self.get_previous_index(
            current=current.number, 
            total=desktop_count
        )

        if previous_number == -1:
            return
    
        self.go_to_desktop(VirtualDesktop(previous_number))

    def v_desktop_create_new(self):
        desktop = VirtualDesktop.create()

        self.go_to_desktop(desktop)

    def get_next_index(self, current: int, total: int):

        if self.config.virtual_desktop.loop:
            return current % total + 1

        next_number = current + 1
        if next_number <= total:
            return next_number

        return -1 

    def get_previous_index(self, current: int, total: int):
        
        if self.config.virtual_desktop.loop:
            return (current - 2) % total + 1
            
        previous_number = current - 1
        if previous_number >= 1:
            return previous_number
            
        return -1

    def v_desktop_delete_current(self):
        print("delete")
        desktops = pyvda.get_virtual_desktops()
        current = VirtualDesktop.current()
        current_index = current.number - 1  # convert 1-indexed -> 0-indexed
    
        if len(desktops) <= 1:
            return
    
        fallback: VirtualDesktop
        if current_index > 0:
            fallback = desktops[current_index - 1]
        else:
            fallback = desktops[current_index + 1]

        current.remove(fallback)
        eventBus.vDesktopNotiferShow.emit(fallback)

    def go_to_desktop(self, desktop: VirtualDesktop):
        desktop.go()

        eventBus.vDesktopNotiferShow.emit(desktop)

    def get_left_window(self) -> WindowInfo | None:
        # This is for future
        pass
            
    def get_right_window(self) -> WindowInfo | None:
        # This is for future
        pass
