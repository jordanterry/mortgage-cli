"""XDG-compliant configuration path resolution."""

import os
from pathlib import Path


def get_config_dir() -> Path:
    """Get XDG-compliant config directory for mortgage-cli.

    Uses $XDG_CONFIG_HOME if set, otherwise ~/.config.

    Returns:
        Path to ~/.config/mortgage-cli (or equivalent)
    """
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        base = Path(xdg_config)
    else:
        base = Path.home() / ".config"
    return base / "mortgage-cli"


def get_profiles_dir() -> Path:
    """Get directory for profile YAML files.

    Returns:
        Path to ~/.config/mortgage-cli/profiles
    """
    return get_config_dir() / "profiles"


def get_global_config_path() -> Path:
    """Get path to global config file.

    Returns:
        Path to ~/.config/mortgage-cli/config.yaml
    """
    return get_config_dir() / "config.yaml"
