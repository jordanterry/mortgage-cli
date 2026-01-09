"""Configuration management for mortgage-cli."""

from mortgage_cli.config.defaults import DEFAULT_PROFILE
from mortgage_cli.config.manager import ConfigManager
from mortgage_cli.config.paths import get_config_dir, get_global_config_path, get_profiles_dir

__all__ = [
    "ConfigManager",
    "DEFAULT_PROFILE",
    "get_config_dir",
    "get_profiles_dir",
    "get_global_config_path",
]
