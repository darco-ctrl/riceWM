from dataclasses import dataclass

from PySide6.QtGui import QFont


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

    def to_qfont(self, qfont: QFont) -> QFont:

        QWEIGHT = {
            "Thin": QFont.Weight.Thin,
            "Light": QFont.Weight.Light,
            "Normal": QFont.Weight.Normal,
            "Medium": QFont.Weight.Medium,
            "Bold": QFont.Weight.Bold,
            "Black": QFont.Weight.Black,
        }

        qfont.setFamily(self.family)
        qfont.setPixelSize(self.pixel_size)
        qfont.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, self.letter_spacing)
        qfont.setBold(self.is_bold)
        qfont.setItalic(self.is_italic)
        qfont.setUnderline(self.is_underline)
        qfont.setStrikeOut(self.is_strike_out)
        qfont.setWeight(QWEIGHT[self.weight])

        return qfont


@dataclass
class Border:
    style: str
    radius: int
    width: list
    color: str


@dataclass
class LineEdit:
    margin: list
    text_margin: list
    background_color: str
    color: str
    border: Border
    font: FontStyle

    def to_style_sheet(self) -> str:
        return f"""
            border-style: {self.border.style};
            border-radius: {self.border.radius}px;
            border-left-width: {self.border.width[0]}px;
            border-top-width: {self.border.width[1]}px;
            border-right-width: {self.border.width[2]}px;
            border-bottom-width: {self.border.width[3]}px;
            background-color: {self.background_color};
            border-color: {self.border.color};
            color: {self.color}
        """


@dataclass
class SearchBox:
    height: int
    background_color: str
    line_edit: LineEdit


@dataclass
class KeyBindLabel:
    width: int
    height: int
    background_color: str
    color: str


@dataclass
class TitleLabel:
    preload_text: str
    background_color: str
    color: str


@dataclass
class WindowIconLabel:
    width: int
    height: int


@dataclass
class SelectionIndicator:
    width: int
    height: int
    background_color: str


@dataclass
class WindowItemFrame:
    height: int
    contents_margin: list
    background_color: str
    selection_indicator: SelectionIndicator
    icon_label: WindowIconLabel
    title_label: TitleLabel
    key_bind_lable: KeyBindLabel


@dataclass
class T_WindowSwitchPanel:
    window_width: int
    background_color: str
    search_box: SearchBox
