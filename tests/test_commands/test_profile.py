"""Integration tests for profile commands."""

import json
import os

from typer.testing import CliRunner

from mortgage_cli.main import app

runner = CliRunner()


class TestProfileListCommand:
    """Tests for profile list command."""

    def test_profile_list_basic(self):
        """Profile list shows default profile."""
        result = runner.invoke(app, ["profile", "list"])

        assert result.exit_code == 0
        assert "default" in result.stdout

    def test_profile_list_json(self):
        """Profile list JSON output is valid."""
        result = runner.invoke(app, ["profile", "list", "--output", "json"])

        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert "profiles" in data
        assert any(p["name"] == "default" for p in data["profiles"])


class TestProfileShowCommand:
    """Tests for profile show command."""

    def test_profile_show_default(self):
        """Profile show displays default profile."""
        result = runner.invoke(app, ["profile", "show", "default"])

        assert result.exit_code == 0
        assert "Profile: default" in result.stdout
        assert "Interest Rate" in result.stdout
        assert "4.0%" in result.stdout

    def test_profile_show_nonexistent(self):
        """Profile show handles missing profile."""
        result = runner.invoke(app, ["profile", "show", "nonexistent"])

        assert result.exit_code == 1
        assert "not found" in result.stdout.lower()


class TestProfileCreateDeleteCommand:
    """Tests for profile create and delete commands."""

    def test_profile_create_and_delete(self, tmp_path, monkeypatch):
        """Profile create and delete work together."""
        # Use temp directory for config
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

        # Create profile
        result = runner.invoke(
            app,
            ["profile", "create", "test-profile", "--description", "Test profile"],
        )
        assert result.exit_code == 0
        assert "Created profile" in result.stdout

        # Verify it exists
        result = runner.invoke(app, ["profile", "list"])
        assert "test-profile" in result.stdout

        # Delete profile
        result = runner.invoke(
            app,
            ["profile", "delete", "test-profile", "--force"],
        )
        assert result.exit_code == 0
        assert "Deleted" in result.stdout

    def test_profile_create_duplicate(self, tmp_path, monkeypatch):
        """Cannot create duplicate profile."""
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

        # Create first
        runner.invoke(app, ["profile", "create", "duplicate"])

        # Try to create again
        result = runner.invoke(app, ["profile", "create", "duplicate"])
        assert result.exit_code == 1
        assert "already exists" in result.stdout.lower()

    def test_profile_delete_default_blocked(self):
        """Cannot delete default profile."""
        result = runner.invoke(app, ["profile", "delete", "default", "--force"])

        assert result.exit_code == 1
        assert "cannot delete" in result.stdout.lower()


class TestProfileCompareCommand:
    """Tests for profile compare command."""

    def test_profile_compare_basic(self):
        """Profile compare works with single profile."""
        result = runner.invoke(
            app,
            [
                "profile", "compare",
                "--price", "150000",
                "--rent", "900",
                "--profiles", "default",
            ],
        )

        assert result.exit_code == 0
        assert "Profile Comparison" in result.stdout
        assert "default" in result.stdout

    def test_profile_compare_json(self):
        """Profile compare JSON output is valid."""
        result = runner.invoke(
            app,
            [
                "profile", "compare",
                "--price", "150000",
                "--rent", "900",
                "--profiles", "default",
                "--output", "json",
            ],
        )

        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert "comparison" in data
        assert len(data["comparison"]) == 1
        assert data["comparison"][0]["profile"] == "default"
