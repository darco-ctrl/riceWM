import json
from pathlib import Path

import tomllib

import app.paths as rice_paths
from config.app_config import AppConfig
from data.config.config import Config
from data.theme.theme import Theme


class DataManager:
    def __init__(
        self,
        app_config: AppConfig,
        config_dir: Path,
        themes_dir: Path,
        keybinds_file: Path,
    ) -> None:
        self.app_config = app_config
        self.config_dir = config_dir
        self.themes_dir = themes_dir
        self.keybinds_file = keybinds_file

        self.active_config: Config = Config(
            config_path=str(self.get_active_config_Path())
        )
        self.active_theme: Theme = Theme(theme_path=str(self.get_active_theme_path()))

    # Returns the path to the active theme and congfig based on the app config.
    def get_active_theme_path(self) -> Path:
        theme_name = self.app_config.get_current_theme
        return self.themes_dir / theme_name

    def get_active_config_Path(self) -> Path: 
        config_name = self.app_config.get_current_config
        return self.config_dir / config_name
                                                                                                                                                                                                                                                                                                                                                                                                                                       