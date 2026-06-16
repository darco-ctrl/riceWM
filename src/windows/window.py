from dataclasses import dataclass

from PySide6.QtGui import QIcon


@dataclass
class WindowInfo:
    hwnd: int
    title: str
    process_id: int
    icon_path: str
    is_focused: bool = False
    is_minimized: bool = False
    is_pwa: bool = False
    pwa_arg: str | None = None
