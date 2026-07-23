from data.config.config import Config
from data.theme.theme import Theme
from widgets.window_switch_panel.window_switch_panel import WindowSwitchPanelWidget


class WidgetManager:
    def __init__(self, config: Config, theme: Theme):
        self.config = config
        self.theme = theme
        self.widgets = {}

        self.load_widgets()

    def load_widgets(self):
        self.widgets["window_switch_panel"] = WindowSwitchPanelWidget(
            config=self.config.window_switch_panel, theme=self.theme.window_switch_panel
        )

        # self.widgets["dock"] = DockWidget(WidgetTheme(self.theme.data["dock"]))

    def show_widgets(self):
        for widget in self.widgets.values():
            widget.start()

    def hide_widgets(self):
        for widget in self.widgets.values():
            widget.hide()

    def hide_widget(self, widget_name: str):
        if widget_name in self.widgets:
            self.widgets[widget_name].hide()
how to 