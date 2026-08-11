from PySide6.QtCore import QTimer
from pyvda import VirtualDesktop


class VirtualDesktopWatcher:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.current_desktop = VirtualDesktop.current()

        self.timer = QTimer()
        self.timer.timeout.connect(self._check)
        self.timer.start(100)

    def _check(self):
        desktop = VirtualDesktop.current()

        if desktop == self.current_desktop:
            return

        old = self.current_desktop
        self.current_desktop = desktop

        self.event_bus.virtualDesktopChanged.emit(old, desktop)
