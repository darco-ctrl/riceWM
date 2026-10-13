import shutil

import src.app.paths as rice_paths


class BootStrap:
    """Initializes required application directories and default configuration files."""
    
    @staticmethod
    def _ensure_dir(path):
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _ensure_file(path, default_path):
        if not path.exists():
            shutil.copyfile(default_path, path)

    # Ensure if all configs file and folders exists if not create new
    def ensure_config(self):
        self._ensure_dir(rice_paths.rice_config_path)
        self._ensure_dir(rice_paths.log_folder)
        self._ensure_dir(rice_paths.themes_dir)
        self._ensure_dir(rice_paths.config_dir)
        self._ensure_dir(rice_paths.window_cache_icon_dir)
    
        self._ensure_file(
            rice_paths.app_config_path,
            rice_paths.default_app_config_path,
        )
        self._ensure_file(
            rice_paths.themes_dir / "default_theme.json",
            rice_paths.default_theme_path,
        )
        self._ensure_file(
            rice_paths.config_dir / "default_config.json",
            rice_paths.default_config_path,
        )
        self._ensure_file(
            rice_paths.key_map_file,
            rice_paths.default_keymap_path,
        )

    # Deletes any cached files, like icons
    def delete_cache(self):
        shutil.rmtree(rice_paths.window_cache_icon_dir, ignore_errors=True)
