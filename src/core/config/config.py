import json

from src.core.config.models import (
    Animation,
    AnimationConfig,
    Behavior,
    C_WindowSearch,
    DesktopNameConfig,
    SearchBoxConfig,
    VirtualDesktopNotifierConfig,
)


class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path

        self.name: str
        self.window_search: C_WindowSearch
        self.virtual_destkop_notifer: VirtualDesktopNotifierConfig
        self.load()

    def reload(self):
        self.load()

    def load(self):
        with open(self.config_path, "r") as file:
            print(f"Loading config: {self.config_path}.")

            data = json.load(file)
            # print(data)
            self.create_data_classes(data)
            del data

    def create_data_classes(self, data: dict):
        self.name = data["name"]

        self.create_window_search(dict=data["window_search"])
        self.create_virtual_desktop_notifier(
            data=data["virtual_desktop_notifier"]
        )

    def create_virtual_desktop_notifier(self, data: dict):
       
        dict_desktop_name = data["desktop_name"] 
        dict_animation = data["animation"]
        dict_fade_in = dict_animation["fade_in"]
        dict_fade_out = dict_animation["fade_out"]

        fade_in: Animation = Animation(
            duration=dict_fade_in["duration"]
        )
        fade_out: Animation = Animation(
            duration=dict_fade_out["duration"]
        )
        animation_op: AnimationConfig = AnimationConfig(
            fade_in=fade_in,
            fade_out=fade_out
        )
    
        desktop_name: DesktopNameConfig = DesktopNameConfig(
            max_char_length=dict_desktop_name["max_char_length"],
            prefix=dict_desktop_name["prefix"],
            suffix=dict_desktop_name["suffix"]
        )
    
        auto_hide_time: int = data["auto_hide_time"] - fade_out.duration
        print(f"auto_hide_time: {auto_hide_time}")
        
        self.virtual_destkop_notifer = VirtualDesktopNotifierConfig(
            enabled=data["enabled"],
            auto_hide_time=auto_hide_time,
            hide_on_hover=data["hide_on_hover"],
            desktop_name=desktop_name,
            animation=animation_op
        )

    def create_window_search(self, dict: dict):
        search_box_dict = dict["search_box"]
        behavior_dict = dict["behavior"]
        # Behavior
        behavior: Behavior = Behavior(
            max_results_shown=behavior_dict["max_results_shown"]
        )

        search_box: SearchBoxConfig = SearchBoxConfig(
            placeholder_text=search_box_dict["placeholder_text"]
        )

        # Window Switch Panel
        self.window_search = C_WindowSearch(
            search_box=search_box,
            behavior=behavior,
            window_width=dict["window_width"]
        )
