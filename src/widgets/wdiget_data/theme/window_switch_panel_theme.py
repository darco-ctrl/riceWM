class WindowSwitchPanelTheme:
    def __init__(self, data: dict):
        self.data = data

        self.apply()

    def apply(self):
        # window - config
        self.window_width = self.data.get("window_width", 0)
        self.max_window_shown = self.data.get("max_window_shown", 0)
        self.background_color = self.data.get("background_color", 0)

        # search box
        self.search_box_height = self.data.get("height", 0)
        self.search_box_corne_radius = self.data.get("corne_radius", 0)
        self.saerch_box_border_width = self.data.get("border_width", 0)

        self.line_edit_background = self.data.get("background_color", 0)
        self.line_edit_background = self.data.get("border_color")
