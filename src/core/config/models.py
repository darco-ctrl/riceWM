from dataclasses import dataclass


@dataclass
class Behavior:
    max_results_shown: int
    auto_adjust_height: bool

@dataclass
class SearchBoxConfig:
    placeholder_text: str

@dataclass
class C_WindowSearch:
    search_box: SearchBoxConfig
    behavior: Behavior
    window_width: int
