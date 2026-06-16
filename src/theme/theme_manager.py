from pathlib import Path

import tomllib

import app.paths as rice_paths
from config.app_config import AppConfig


class Theme:
    def __init__(self, theme_path: Path):
        self.theme_path = theme_path
        self.data = self.load()

    def load(self) -> dict:
        with open(self.theme_path, "rb") as file:
            print(f"Loading theme: {self.theme_path}")
            return tomllib.load(file)


class ThemeManager:
    def __init__(self, themes_dir: Path, app_config: AppConfig) -> None:
        self.app_config = app_config
        self.themes_dir = themes_dir
        self.current_theme = None

    # Returns the path to the active theme based on the app config.
    def get_active_theme_path(self) -> Path:
        theme_name = self.app_config.get_current_theme
        return self.themes_dir / theme_name

    # Loads the current theme based on the app config.
    def load_current_theme(self) -> Theme:
        theme_name = self.get_active_theme_path()

        if not theme_name.exists():
            raise FileNotFoundError(f"Theme not found: {theme_name}")

        self.current_theme = Theme(theme_name)
        return self.current_theme
