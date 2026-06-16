from plistlib import load

from windows.window import WindowInfo
from windows.window_scanner import WindowScanner


class WindowManager:
    def __init__(self):
        self.scanner: WindowScanner = WindowScanner()
        self.windows: list[WindowInfo] = []

        self.load_windows()

    def load_windows(self):
        self.windows = self.scanner.get_windows_info()

    def reload_windows(self):
        self.windows.clear()
        self.load_windows()
