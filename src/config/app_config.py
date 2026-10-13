import tomllib
from pathlib import Path


class AppConfig:
    """Holds and handles apps config which is app.toml"""
    
    def __init__(self, config_path: Path):
        self._config_path = config_path
        self._data = self.load()

    def get_app_config_path(self) -> str:
        return str(self._config_path)

    def load(self) -> dict:
        with self._config_path.open("rb") as file:
            return tomllib.load(file)

    def reload(self) -> None:
        self._data = self.load()

    @property
    def get_current_theme(self) -> str:
        return self._data["data"]["active_theme"]

    @property
    def get_current_config(self) -> str:
        return self._data["data"]["active_config"]
