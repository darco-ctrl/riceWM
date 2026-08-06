import shutil
from pathlib import Path

import src.app.paths as rice_paths


class BootStrap:
    def ensure_config(self):
        self.check_config()
        self.check_app_config()
        self.check_theme_dir()
        self.check_config_dir()
        self.check_window_icon_dir()
        self.check_keymap_file()

    def check_config(self):
        if not rice_paths.rice_config_path.exists():
            # create the config directory if it doesn't exist
            rice_paths.rice_config_path.mkdir(parents=True, exist_ok=True)

    def check_app_config(self):
        if not rice_paths.app_config_path.exists():
            # create the app config file if it doesn't exist

            shutil.copyfile(
                rice_paths.default_app_config_path, rice_paths.app_config_path
            )

    def check_theme_dir(self):

        # create the themes directory if it doesn't exist
        if not rice_paths.themes_dir.exists():
            rice_paths.themes_dir.mkdir(parents=True, exist_ok=True)

        # copy the default theme to the themes directory
        if not (rice_paths.themes_dir / "default_theme.json").exists():
            shutil.copyfile(
                rice_paths.default_theme_path,
                rice_paths.themes_dir / "default_theme.json",
            )

    def check_config_dir(self):
        # create the themes directory if it doesn't exist
        if not rice_paths.config_dir.exists():
            rice_paths.config_dir.mkdir(parents=True, exist_ok=True)
            print(
                f"create parents becuase file '{rice_paths.config_dir}' does not exists"
            )

        # copy the default theme to the themes directory
        if not (rice_paths.config_dir / "default_config.json").exists():
            shutil.copyfile(
                rice_paths.default_config_path,
                rice_paths.config_dir / "default_config.json",
            )
            print(f"copying json '{rice_paths.config_dir}' does not exists")

    def check_keymap_file(self):
        if not (rice_paths.key_map_file).exists():
            shutil.copyfile(rice_paths.default_keymap_path, rice_paths.rice_config_path)

    def check_window_icon_dir(self):
        if not rice_paths.window_cache_icon_dir.exists():
            rice_paths.window_cache_icon_dir.mkdir(parents=True, exist_ok=True)

    def delete_cache(self):
        pass
        # self.del_window_icon_dir()

    def del_window_icon_dir(self):
        if rice_paths.window_cache_icon_dir.exists():
            shutil.rmtree(rice_paths.window_cache_icon_dir)
