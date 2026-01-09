"""Integration tests for matrix command."""

import json

from typer.testing import CliRunner

from mortgage_cli.main import app

runner = CliRunner()


class TestMatrixCommand:
    """Tests for the matrix command."""

    def test_matrix_basic(self):
        """Basic matrix command works."""
        result = runner.invoke(
            app,
            [
                "matrix",
                "--price-min", "100000",
                "--price-max", "140000",
                "--price-step", "20000",
                "--down-min", "10%",
                "--down-max", "30%",
                "--down-step", "10%",
            ],
        )

        assert result.exit_code == 0
        assert "Break-Even Rent Matrix" in result.stdout
        assert "€100K" in result.stdout
        assert "€120K" in result.stdout
        assert "€140K" in result.stdout

    def test_matrix_uses_profile_target_rent(self):
        """Matrix uses profile's target rent by default."""
        result = runner.invoke(
            app,
            [
                "matrix",
                "--price-min", "100000",
                "--price-max", "120000",
            ],
        )

        assert result.exit_code == 0
        assert "€1,000" in result.stdout  # Default target rent

    def test_matrix_custom_rent(self):
        """Matrix uses custom rent when specified."""
        result = runner.invoke(
            app,
            [
                "matrix",
                "--price-min", "100000",
                "--price-max", "120000",
                "--rent", "1200",
            ],
        )

        assert result.exit_code == 0
        assert "€1,200" in result.stdout

    def test_matrix_json_output(self):
        """JSON output is valid."""
        result = runner.invoke(
            app,
            [
                "matrix",
                "--price-min", "100000",
                "--price-max", "120000",
                "--price-step", "20000",
                "--down-min", "20%",
                "--down-max", "20%",
                "--output", "json",
            ],
        )

        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert "matrix" in data
        assert "cells" in data["matrix"]
        assert len(data["matrix"]["cells"]) > 0

    def test_matrix_shows_legend(self):
        """Matrix shows color legend."""
        result = runner.invoke(
            app,
            [
                "matrix",
                "--price-min", "100000",
                "--price-max", "120000",
            ],
        )

        assert result.exit_code == 0
        assert "Legend" in result.stdout or "GREEN" in result.stdout
