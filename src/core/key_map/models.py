from dataclasses import dataclass


@dataclass
class DataManagerKB:
    reload_data: str


@dataclass
class WindowSwitchPanelKB:
    toggle: str

@dataclass
class WindowControlsKB:
    go_left: str
    go_right: str

@dataclass
class VirtualDesktopKB:
    go_left: str
    go_right: str
    create_new: str
    delete_current: str

@dataclass
class WindowManagerKB:
    virtual_desktop: VirtualDesktopKB
    window_controls: WindowControlsKB
