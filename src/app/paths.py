from pathlib import Path

rice_config_path = Path.home() / ".config" / "rice"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
default_app_config_path = PROJECT_ROOT / "default_config" / "app.toml"
default_theme_path = PROJECT_ROOT / "default_config" / "theme.toml"

app_config_path = rice_config_path / "app.toml"
themes_dir = rice_config_path / "themes"

cache_ico_dir = rice_config_path / "cache" / ".ico"
cache_icon_dir = rice_config_path / "cache" / "icons"
