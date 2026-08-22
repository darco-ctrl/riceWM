
from dataclasses import dataclass


@dataclass
class FontStyle:
    family: str
    pixel_size: int
    letter_spacing: float
    is_bold: bool
    is_italic: bool
    is_underline: bool
    is_strike_out: bool
    weight: str
