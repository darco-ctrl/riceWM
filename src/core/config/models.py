from dataclasses import dataclass


@dataclass
class Behavior:
    max_results_shown: int
    auto_adjust_height: bool


@dataclass
class C_WindowSearch:
    behavior: Behavior
    window_width: int
