from dataclasses import dataclass

from src.core.theme.components.line_edit_style import LineEditStyle


@dataclass
class SearchBoxLineEditStyle(LineEditStyle):
    place_holder_text: str
    margin: list
    text_margin: list
