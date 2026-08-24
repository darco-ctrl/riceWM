
from PySide6.QtGui import QFont

from src.core.theme.components.line_edit_style import LineEditStyle
from src.core.theme.primitives.font_style import FontStyle


class ThemeHelper:
    def to_qfont(self, qfont: QFont, font_style: FontStyle) -> QFont:
        QWEIGHT = {
            "Thin": QFont.Weight.Thin,
            "Light": QFont.Weight.Light,
            "Normal": QFont.Weight.Normal,
            "Medium": QFont.Weight.Medium,
            "Bold": QFont.Weight.Bold,
            "Black": QFont.Weight.Black,
        }

        qfont.setFamily(font_style.family)
        qfont.setPixelSize(font_style.pixel_size)
        qfont.setLetterSpacing(
            QFont.SpacingType.AbsoluteSpacing, font_style.letter_spacing
        )
        qfont.setBold(font_style.is_bold)
        qfont.setItalic(font_style.is_italic)
        qfont.setUnderline(font_style.is_underline)
        qfont.setStrikeOut(font_style.is_strike_out)
        qfont.setWeight(QWEIGHT[font_style.weight])

        return qfont

    def get_line_edit_style(self, style: LineEditStyle) -> str:
        return f"""
            border-style: {style.border_style.style};
            border-radius: {style.border_style.radius}px;
            border-left-width: {style.border_style.width[0]}px;
            border-top-width: {style.border_style.width[1]}px;
            border-right-width: {style.border_style.width[2]}px;
            border-bottom-width: {style.border_style.width[3]}px;
            background-color: {style.color_style.background_color};
            border-color: {style.border_style.color};
            color: {style.color_style.color}
        """
