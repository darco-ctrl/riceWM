from math import comb
from pathlib import Path

import tomllib

import src.app.paths as rice_paths


class AppConfig:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.data = self.load()

    def load(self) -> dict:
        with self.config_path.open("rb") as file:
            return tomllib.load(file)

    def reload(self) -> None:
        self.data = self.load()

    @property
    def get_current_theme(self) -> str:
        return self.data["data"]["active_theme"]

    @property
    def get_current_config(self) -> str:
        return self.data["data"]["active_config"]
