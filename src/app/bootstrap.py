import shutil
from pathlib import Path

import app.paths as rice_paths


def ensure_config():
    check_config()
    check_app_config()
    check_theme_dir()
    check_config_dir()
    check_window_icon_dir()


def check_config():
    if not rice_paths.rice_config_path.exists():
        # create the config directory if it doesn't exist
        rice_paths.rice_config_path.mkdir(parents=True, exist_ok=True)


def check_app_config():
    if not rice_paths.app_config_path.exists():
        # create the app config file if it doesn't exist

        shutil.copyfile(rice_paths.default_app_config_path, rice_paths.app_config_path)


def check_theme_dir():

    # create the themes directory if it doesn't exist
    if not rice_paths.themes_dir.exists():
        rice_paths.themes_dir.mkdir(parents=True, exist_ok=True)

    # copy the default theme to the themes directory
    if not (rice_paths.themes_dir / "default_theme.toml").exists():
        shutil.copyfile(
            rice_paths.default_theme_path, rice_paths.themes_dir / "default_theme.toml"
        )

def check_config_dir():
    # create the themes directory if it doesn't exist
    if not rice_paths.config_dir.exists():
        rice_paths.config_dir.mkdir(parents=True, exist_ok=True)

    # copy the default theme to the themes directory
    if not (rice_paths.config_dir / "default_theme.toml").exists():
        shutil.copyfile(
            rice_paths.default_config_path, rice_paths.config_dir / "default_config.toml"
        )

def check_window_icon_dir():
    if not rice_paths.window_cache_icon_dir.exists():
        rice_paths.window_cache_icon_dir.mkdir(parents=True, exist_ok=True)


def delete_cache():
    del_window_icon_dir()


def del_window_icon_dir():
    if rice_paths.window_cache_icon_dir.exists():
        shutil.rmtree(rice_paths.window_cache_icon_dir)
