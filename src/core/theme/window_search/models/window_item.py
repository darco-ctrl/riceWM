from dataclasses import dataclass

from src.core.theme.components.frame_style import FrameStyle
from src.core.theme.components.label_style import LabelStyle
from src.core.theme.primitives.color_style import ColorStyle
from src.core.theme.window_search.models.frame_style import SelectableFrameStyle
from src.core.theme.window_search.models.icon_container import IconContainerStyle
from src.core.theme.window_search.models.item_frame import ItemFrame
from src.core.theme.window_search.models.keybind_label import KeybindLabelStyle
from src.core.theme.window_search.models.label_style import SelectableLabelStyle
from src.core.theme.window_search.models.selection_indicator import SelectionIndicatorStyle
from src.core.theme.window_search.models.title_label import TitleLabelStyle


@dataclass
class WindowItemStyle:
    color_style: ColorStyle
    frame_style: ItemFrame 
    selection_indicator: SelectionIndicatorStyle
    icon_container: IconContainerStyle
    title_label: TitleLabelStyle
    keybind_label: KeybindLabelStyle
