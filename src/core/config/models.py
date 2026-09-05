from dataclasses import dataclass


@dataclass
class Behavior:
    max_results_shown: int

@dataclass
class SearchBoxConfig:
    placeholder_text: str

@dataclass
class C_WindowSearch:
    search_box: SearchBoxConfig
    behavior: Behavior
    window_width: int

@dataclass 
class Animation:
    duration: int

@dataclass
class AnimationConfig:
    fade_in: Animation
    fade_out: Animation
    
@dataclass 
class DesktopNameConfig:
    max_char_length: int
    prefix: str
    suffix: str

@dataclass
class VirtualDesktopNotifierConfig:
    enabled: bool
    auto_hide_time: int
    hide_on_hover: bool
    desktop_name: DesktopNameConfig
    window_animation: AnimationConfig
    label_animation: AnimationConfig
