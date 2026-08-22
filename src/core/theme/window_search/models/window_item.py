from dataclasses import dataclass

from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.components.label_style import LabelStyle
from src.core.theme.window_search.models.frame_style import SelectableFrameStyle
from src.core.theme.window_search.models.label_style import SelectableLabelStyle


@dataclass
class WindowItemTheme:
    frame_style: SelectableFrameStyle
    selection_indicator: SelectableFrameStyle
    icon_container: SelectableFrameStyle
    title_label: SelectableLabelStyle
    keybind_label: SelectableLabelStyle
