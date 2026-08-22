from dataclasses import dataclass


@dataclass
class BorderStyle:
    style: str
    radius: int
    width: list
    color: str
