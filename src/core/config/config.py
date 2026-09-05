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

    def get_animation(self, data: dict):
        dict_fade_in: dict = data["fade_in"]
        dict_fade_out: dict = data["fade_out"]

        fade_in: Animation = Animation(
            duration=dict_fade_in["duration"]
        )
        fade_out: Animation = Animation(
            duration=dict_fade_out["duration"]
        )

        return AnimationConfig(
            fade_in=fade_in,
            fade_out=fade_out
        )

    def create_virtual_desktop_notifier(self, data: dict):
       
        dict_desktop_name = data["desktop_name"] 
        dict_window_aniamtion = data["window_animation"]
        dict_label_animation =data["label_animation"]

        window_aniamtion: AnimationConfig = self.get_animation(
            data=dict_window_aniamtion
        )
        label_animation: AnimationConfig = self.get_animation(
            data=dict_label_animation
        )
    
        desktop_name: DesktopNameConfig = DesktopNameConfig(
            max_char_length=dict_desktop_name["max_char_length"],
            prefix=dict_desktop_name["prefix"],
            suffix=dict_desktop_name["suffix"]
        )
    
        auto_hide_time: int = data["auto_hide_time"] - (
            window_aniamtion.fade_out.duration
        )
        
        self.virtual_destkop_notifer = VirtualDesktopNotifierConfig(
            enabled=data["enabled"],
            auto_hide_time=auto_hide_time,
            hide_on_hover=data["hide_on_hover"],
            desktop_name=desktop_name,
            window_animation=window_aniamtion,
            label_animation=label_animation
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
