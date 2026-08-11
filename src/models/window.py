from dataclasses import dataclass

from win32 import win32gui


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

    def update(self):
        self.title = win32gui.GetWindowText(self.hwnd).strip()
