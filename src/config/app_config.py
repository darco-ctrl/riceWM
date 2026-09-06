
from pathlib import Path

import tomllib


class AppConfig:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.data = self.load()

    def get_app_config_path(self) -> str:
        return str(self.config_path)

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
