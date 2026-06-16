from theme.theme_manager import Theme
from widgets.widget_theme import WidgetTheme


class WidgetManager:
    def __init__(self, theme: Theme):
        self.theme = theme
        self.widgets = {}

        self.load_widgets()

    def load_widgets(self):
        pass
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
