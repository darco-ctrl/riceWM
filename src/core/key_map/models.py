from dataclasses import dataclass


@dataclass
class ApplicationKM:
    restart_application: str


@dataclass
class WindowSearchKM:
    toggle: str
    close_window: str
    select_up: str
    select_down: str

@dataclass
class WindowControlsKB:
    maximize: str
    minimize: str
    close: str
    restore: str

@dataclass
class VirtualDesktopKB:
    go_left: str
    go_right: str
    create_new: str
    delete_current: str

@dataclass
class WindowManagerKM:
    virtual_desktop: VirtualDesktopKB
    window_controls: WindowControlsKB
