from dataclasses import dataclass


@dataclass
class Behavior:
    max_results_shown: int
    auto_adjust_height: bool


@dataclass
class C_WindowSwitchPanel:
    behavior: Behavior
    window_width: int
