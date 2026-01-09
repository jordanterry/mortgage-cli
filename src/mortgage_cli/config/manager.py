"""Configuration and profile management."""

from pathlib import Path

import yaml

from mortgage_cli.config.defaults import DEFAULT_PROFILE
from mortgage_cli.config.paths import get_profiles_dir
from mortgage_cli.models.profile import Profile


class ProfileNotFoundError(Exception):
    """Raised when a requested profile does not exist."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Profile '{name}' not found")


class ProfileExistsError(Exception):
    """Raised when trying to create a profile that already exists."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Profile '{name}' already exists")


class ConfigManager:
    """Manage profile and global configuration.

    Handles CRUD operations for profiles stored as YAML files.
    """

    def __init__(self, profiles_dir: Path | None = None):
        """Initialize config manager.

        Args:
            profiles_dir: Custom profiles directory (for testing).
                         Uses default XDG path if not specified.
        """
        self.profiles_dir = profiles_dir or get_profiles_dir()

    def ensure_directories(self) -> None:
        """Create config directories if they don't exist."""
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def _get_profile_path(self, name: str) -> Path:
        """Get the path to a profile file.

        Args:
            name: Profile name

        Returns:
            Path to the profile YAML file
        """
        return self.profiles_dir / f"{name}.yaml"

    def load_profile(self, name: str) -> Profile:
        """Load profile by name.

        Falls back to built-in default if 'default' profile doesn't exist on disk.

        Args:
            name: Profile name

        Returns:
            Profile instance

        Raises:
            ProfileNotFoundError: If profile doesn't exist (except 'default')
        """
        path = self._get_profile_path(name)

        if not path.exists():
            if name == "default":
                return DEFAULT_PROFILE
            raise ProfileNotFoundError(name)

        with open(path) as f:
            data = yaml.safe_load(f)

        return Profile(**data)

    def save_profile(self, profile: Profile, overwrite: bool = True) -> None:
        """Save profile to YAML file.

        Args:
            profile: Profile to save
            overwrite: If False, raises error if profile exists

        Raises:
            ProfileExistsError: If overwrite=False and profile exists
        """
        self.ensure_directories()
        path = self._get_profile_path(profile.name)

        if not overwrite and path.exists():
            raise ProfileExistsError(profile.name)

        with open(path, "w") as f:
            yaml.dump(
                profile.model_dump(mode="json"),
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )

    def delete_profile(self, name: str) -> None:
        """Delete a profile.

        Args:
            name: Profile name to delete

        Raises:
            ProfileNotFoundError: If profile doesn't exist
        """
        path = self._get_profile_path(name)

        if not path.exists():
            raise ProfileNotFoundError(name)

        path.unlink()

    def list_profiles(self) -> list[tuple[str, str]]:
        """List all available profiles.

        Returns:
            List of (name, description) tuples
        """
        profiles: list[tuple[str, str]] = []

        # Always include default
        if not self._get_profile_path("default").exists():
            profiles.append((DEFAULT_PROFILE.name, DEFAULT_PROFILE.description))

        # Add saved profiles
        if self.profiles_dir.exists():
            for path in sorted(self.profiles_dir.glob("*.yaml")):
                name = path.stem
                try:
                    profile = self.load_profile(name)
                    profiles.append((name, profile.description))
                except Exception:
                    # Skip invalid profiles
                    profiles.append((name, "(invalid profile)"))

        return profiles

    def profile_exists(self, name: str) -> bool:
        """Check if a profile exists.

        Args:
            name: Profile name

        Returns:
            True if profile exists (on disk or built-in default)
        """
        if name == "default":
            return True
        return self._get_profile_path(name).exists()

    def create_profile(
        self,
        name: str,
        description: str = "",
        base_profile: str | None = None,
    ) -> Profile:
        """Create a new profile.

        Args:
            name: New profile name
            description: Profile description
            base_profile: Name of profile to copy settings from (default: 'default')

        Returns:
            The created profile

        Raises:
            ProfileExistsError: If profile already exists
            ProfileNotFoundError: If base_profile doesn't exist
        """
        if self.profile_exists(name) and self._get_profile_path(name).exists():
            raise ProfileExistsError(name)

        # Load base profile
        base = self.load_profile(base_profile or "default")

        # Create new profile with same settings
        new_profile = Profile(
            name=name,
            description=description,
            mortgage=base.mortgage.model_copy(),
            budget=base.budget.model_copy(),
            monthly_costs=base.monthly_costs.model_copy(),
            purchase_costs=base.purchase_costs.model_copy(),
            thresholds=base.thresholds.model_copy(),
        )

        self.save_profile(new_profile, overwrite=False)
        return new_profile
