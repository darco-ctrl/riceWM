from src.data.config.config import Config
from src.core.theme.theme import Theme
from src.widgets.search_window.window_search import SearchWindow


class WidgetManager:
    def __init__(self, config: Config, theme: Theme):
        self.config = config
        self.theme = theme
        self.widgets = {}

        self.load_widgets()

    def load_widgets(self):
        self.widgets["window_switch_panel"] = SearchWindow(
            config=self.config, theme=self.theme
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
