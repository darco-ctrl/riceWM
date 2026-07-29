from pathlib import Path

rice_config_path = Path.home() / ".config" / "riceWM"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
assets_dir = PROJECT_ROOT / "assets"
default_app_config_path = PROJECT_ROOT / "default_config" / "app.toml"
default_theme_path = PROJECT_ROOT / "default_config" / "default_theme.json"
default_config_path = PROJECT_ROOT / "default_config" / "default_config.json"
default_keybinds_path = PROJECT_ROOT / "default_config" / "keybinds.json"

app_config_path = rice_config_path / "app.toml"
themes_dir = rice_config_path / "themes"
config_dir = rice_config_path / "config"
keybinds_file = rice_config_path / "keybinds.json"

cache_dir = rice_config_path / "cache"
window_cache_icon_dir = cache_dir / "icons"

wait_icon = assets_dir / "default_app_icon.png"
