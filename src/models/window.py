from dataclasses import dataclass


@dataclass
class WindowInfo:
    hwnd: int
    name: str
    title: str
    icon_path: str
    is_focused: bool = False
    is_pwa: bool = False
    pwa_arg: str | None = None

    def set_focused(self, focused: bool):
        self.is_focused = focused
