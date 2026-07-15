from data.data_manager import Theme, Config
from widgets.widget_data.theme.widget_theme import WidgetTheme
from widgets.window_switch_panel.window_switch_panel import WindowSwitchPanelWidget


class WidgetManager:
    def __init__(self, config: Config, theme: Theme):
        self.config = config
        self.theme = theme
        self.widgets = {}

        self.load_widgets()

    def load_widgets(self):
        self.widgets["window_switch_panel"] = WindowSwitchPanelWidget(
            self.config.data, self.theme.data
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

    def update_theme(self):
        for widget in self.widgets.values():
            widget.set_theme(WidgetTheme(self.theme.data[widget.name]))
