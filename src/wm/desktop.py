from uuid import UUID

from src.models.window import WindowInfo
from src.services.window.scanner import WindowScanner


class Desktop:
    def __init__(
        self, 
        window_scanner: WindowScanner,
        name: str,
        id: UUID
    ):
        self.window_scanner: WindowScanner = window_scanner
        self.name: str = name
