from widgets.window_switch_panel.window_item import WindowItem
from widgets.window_switch_panel.window_switch_panel import WindowSwitchPanelWidget


class WindowStateController:
    def __init__(self, window: WindowSwitchPanelWidget):
        self.window = window
        self.focus_window: WindowItem | None = None

    def set_focus_window(self, window_item: WindowItem):
        if self.focus_window:
            self.focus_window.set_focused(False)

        window_item.set_focused(True)
