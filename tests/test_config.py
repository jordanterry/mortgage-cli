"""Tests for configuration management."""

import pytest

from mortgage_cli.config.defaults import DEFAULT_PROFILE
from mortgage_cli.config.manager import (
    ConfigManager,
    ProfileExistsError,
    ProfileNotFoundError,
)
from mortgage_cli.models.profile import Profile


@pytest.fixture
def config_manager(tmp_path):
    """Create a ConfigManager with a temporary profiles directory."""
    profiles_dir = tmp_path / "profiles"
    return ConfigManager(profiles_dir=profiles_dir)


class TestLoadProfile:
    """Tests for profile loading."""

    def test_load_default_builtin(self, config_manager: ConfigManager):
        """Loading 'default' returns built-in profile when no file exists."""
        profile = config_manager.load_profile("default")

        assert profile.name == "default"
        assert profile.mortgage.interest_rate == DEFAULT_PROFILE.mortgage.interest_rate

    def test_load_nonexistent_raises(self, config_manager: ConfigManager):
        """Loading nonexistent profile raises ProfileNotFoundError."""
        with pytest.raises(ProfileNotFoundError) as exc_info:
            config_manager.load_profile("nonexistent")

        assert exc_info.value.name == "nonexistent"

    def test_load_saved_profile(self, config_manager: ConfigManager):
        """Loading saved profile returns correct data."""
        # Save a profile first
        config_manager.save_profile(DEFAULT_PROFILE)

        profile = config_manager.load_profile("default")

        assert profile.name == "default"
        assert profile.mortgage.interest_rate == DEFAULT_PROFILE.mortgage.interest_rate


class TestSaveProfile:
    """Tests for profile saving."""

    def test_save_creates_file(self, config_manager: ConfigManager):
        """Saving profile creates YAML file."""
        config_manager.save_profile(DEFAULT_PROFILE)

        path = config_manager._get_profile_path("default")
        assert path.exists()

    def test_save_creates_directories(self, config_manager: ConfigManager):
        """Saving profile creates parent directories."""
        assert not config_manager.profiles_dir.exists()

        config_manager.save_profile(DEFAULT_PROFILE)

        assert config_manager.profiles_dir.exists()

    def test_save_overwrite_by_default(self, config_manager: ConfigManager):
        """Saving with same name overwrites by default."""
        config_manager.save_profile(DEFAULT_PROFILE)
        config_manager.save_profile(DEFAULT_PROFILE)  # Should not raise

    def test_save_no_overwrite_raises(self, config_manager: ConfigManager):
        """Saving with overwrite=False raises if file exists."""
        config_manager.save_profile(DEFAULT_PROFILE)

        with pytest.raises(ProfileExistsError) as exc_info:
            config_manager.save_profile(DEFAULT_PROFILE, overwrite=False)

        assert exc_info.value.name == "default"

    def test_round_trip(self, config_manager: ConfigManager):
        """Profile saves and loads correctly."""
        original = DEFAULT_PROFILE.model_copy()

        config_manager.save_profile(original)
        loaded = config_manager.load_profile("default")

        assert loaded.name == original.name
        assert loaded.description == original.description
        assert loaded.mortgage.interest_rate == original.mortgage.interest_rate
        assert loaded.budget.total_available == original.budget.total_available
        assert loaded.monthly_costs.total == original.monthly_costs.total


class TestDeleteProfile:
    """Tests for profile deletion."""

    def test_delete_removes_file(self, config_manager: ConfigManager):
        """Deleting profile removes file."""
        config_manager.save_profile(DEFAULT_PROFILE)
        path = config_manager._get_profile_path("default")
        assert path.exists()

        config_manager.delete_profile("default")

        assert not path.exists()

    def test_delete_nonexistent_raises(self, config_manager: ConfigManager):
        """Deleting nonexistent profile raises ProfileNotFoundError."""
        with pytest.raises(ProfileNotFoundError):
            config_manager.delete_profile("nonexistent")


class TestListProfiles:
    """Tests for profile listing."""

    def test_list_includes_builtin_default(self, config_manager: ConfigManager):
        """Listing includes built-in default when no file exists."""
        profiles = config_manager.list_profiles()

        names = [name for name, _ in profiles]
        assert "default" in names

    def test_list_includes_saved_profiles(self, config_manager: ConfigManager):
        """Listing includes saved profiles."""
        # Create a custom profile
        custom = Profile(
            name="custom",
            description="Custom profile",
            mortgage=DEFAULT_PROFILE.mortgage.model_copy(),
            budget=DEFAULT_PROFILE.budget.model_copy(),
            monthly_costs=DEFAULT_PROFILE.monthly_costs.model_copy(),
            purchase_costs=DEFAULT_PROFILE.purchase_costs.model_copy(),
            thresholds=DEFAULT_PROFILE.thresholds.model_copy(),
        )
        config_manager.save_profile(custom)

        profiles = config_manager.list_profiles()

        names = [name for name, _ in profiles]
        assert "custom" in names


class TestProfileExists:
    """Tests for profile existence check."""

    def test_default_always_exists(self, config_manager: ConfigManager):
        """'default' always exists due to built-in fallback."""
        assert config_manager.profile_exists("default")

    def test_nonexistent_returns_false(self, config_manager: ConfigManager):
        """Nonexistent profile returns False."""
        assert not config_manager.profile_exists("nonexistent")

    def test_saved_profile_exists(self, config_manager: ConfigManager):
        """Saved profile returns True."""
        custom = Profile(
            name="custom",
            description="Custom profile",
            mortgage=DEFAULT_PROFILE.mortgage.model_copy(),
            budget=DEFAULT_PROFILE.budget.model_copy(),
            monthly_costs=DEFAULT_PROFILE.monthly_costs.model_copy(),
            purchase_costs=DEFAULT_PROFILE.purchase_costs.model_copy(),
            thresholds=DEFAULT_PROFILE.thresholds.model_copy(),
        )
        config_manager.save_profile(custom)

        assert config_manager.profile_exists("custom")


class TestCreateProfile:
    """Tests for profile creation."""

    def test_create_new_profile(self, config_manager: ConfigManager):
        """Creating profile saves it to disk."""
        profile = config_manager.create_profile("new", description="New profile")

        assert profile.name == "new"
        assert profile.description == "New profile"
        assert config_manager.profile_exists("new")

    def test_create_copies_from_base(self, config_manager: ConfigManager):
        """New profile copies settings from base profile."""
        profile = config_manager.create_profile("new")

        assert profile.mortgage.interest_rate == DEFAULT_PROFILE.mortgage.interest_rate

    def test_create_existing_raises(self, config_manager: ConfigManager):
        """Creating existing profile raises ProfileExistsError."""
        config_manager.create_profile("existing")

        with pytest.raises(ProfileExistsError):
            config_manager.create_profile("existing")
