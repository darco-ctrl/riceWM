import json
from pathlib import Path

import tomllib

import app.paths as rice_paths
from config.app_config import AppConfig


class ThemeLoader:
    def __init__(self, theme_path: Path):
        self.theme_path = theme_path
        self.data = self.load()

        print(self.data)

    def load(self) -> dict:
        with open(self.theme_path, "r") as file:
            print(f"Loading theme: {self.theme_path}.")
            return json.load(file)


class ConfigLoader:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.data = self.load()

        print(self.data)

    def load(self) -> dict:
        with open(self.config_path, "r") as file:
            print(f"Loading config: {self.config_path}.")
            return json.load(file)


class DataManager:
    def __init__(
        self, app_config: AppConfig, config_dir: Path, themes_dir: Path
    ) -> None:
        self.app_config = app_config
        self.config_dir = config_dir
        self.themes_dir = themes_dir
        self.current_theme = None
        self.current_config = None

    # Returns the path to the active theme and congfig based on the app config.
    def get_active_theme_path(self) -> Path:
        theme_name = self.app_config.get_current_theme
        return self.themes_dir / theme_name

    def get_active_config_Path(self) -> Path:
        config_name = self.app_config.get_current_config
        return self.config_dir / config_name

    # Loads the current theme based on the app config.
    def load_current_theme(self) -> ThemeLoader:
        theme_name = self.get_active_theme_path()

        if not theme_name.exists():
            raise FileNotFoundError(f"Theme not found: {theme_name}")

        self.current_theme = ThemeLoader(theme_name)
        return self.current_theme

    def load_current_config(self) -> ConfigLoader:
        config_name = self.get_active_config_Path()

        if not config_name.exists():
            raise FileNotFoundError(f"Config not found: {config_name}")

        self.current_config = ConfigLoader(config_name)
        return self.current_config
