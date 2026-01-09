"""Integration tests for analyze command."""

import json

import pytest
from typer.testing import CliRunner

from mortgage_cli.main import app

runner = CliRunner()


class TestAnalyzeCommand:
    """Tests for the analyze command."""

    def test_analyze_basic(self):
        """Basic analyze command works."""
        result = runner.invoke(app, ["analyze", "--price", "150000", "--rent", "900"])

        assert result.exit_code == 0
        assert "Property Analysis" in result.stdout
        assert "€150,000" in result.stdout
        assert "Break-Even Rent" in result.stdout

    def test_analyze_with_down_payment(self):
        """Analyze with custom down payment."""
        result = runner.invoke(
            app,
            ["analyze", "--price", "150000", "--rent", "900", "--down", "30%"],
        )

        assert result.exit_code == 0
        assert "30%" in result.stdout

    def test_analyze_json_output(self):
        """JSON output is valid."""
        result = runner.invoke(
            app,
            ["analyze", "--price", "150000", "--rent", "900", "--output", "json"],
        )

        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert "property" in data
        assert "analysis" in data
        assert data["property"]["price"] == 150000.0
        assert data["analysis"]["verdict"] in ["green", "yellow", "red", "over_budget"]

    def test_analyze_json_structure(self):
        """JSON output has complete structure."""
        result = runner.invoke(
            app,
            ["analyze", "--price", "150000", "--rent", "900", "--output", "json"],
        )

        data = json.loads(result.stdout)

        # Check all expected keys
        assert "upfront_costs" in data
        assert "monthly" in data
        assert "warnings" in data
        assert "profile" in data

        # Check upfront costs breakdown
        assert "down_payment" in data["upfront_costs"]
        assert "total" in data["upfront_costs"]

        # Check monthly breakdown
        assert "mortgage_payment" in data["monthly"]
        assert "fixed_costs" in data["monthly"]

    def test_analyze_shows_warnings(self):
        """Warnings appear when break-even exceeds rent."""
        result = runner.invoke(
            app,
            ["analyze", "--price", "200000", "--rent", "800"],
        )

        assert result.exit_code == 0
        assert "shortfall" in result.stdout.lower() or "WARNING" in result.stdout

    def test_analyze_invalid_profile(self):
        """Invalid profile name shows error."""
        result = runner.invoke(
            app,
            ["analyze", "--price", "150000", "--rent", "900", "--profile", "nonexistent"],
        )

        assert result.exit_code == 1
        assert "not found" in result.stdout.lower()

    def test_analyze_invalid_output_format(self):
        """Invalid output format shows error."""
        result = runner.invoke(
            app,
            ["analyze", "--price", "150000", "--rent", "900", "--output", "invalid"],
        )

        assert result.exit_code == 1
        assert "unknown format" in result.stdout.lower()

    def test_analyze_shows_verdict_color(self):
        """Verdict label appears in output."""
        result = runner.invoke(
            app,
            ["analyze", "--price", "150000", "--rent", "900"],
        )

        assert result.exit_code == 0
        # Should have one of the verdict labels
        assert any(
            label in result.stdout
            for label in ["GOOD", "MARGINAL", "POOR", "OVER BUDGET"]
        )


class TestAnalyzeSpreadsheetValidation:
    """Validate analyze command against spreadsheet values."""

    @pytest.mark.parametrize(
        "price,down,expected_break_even",
        [
            (100000, "10%", 800),
            (120000, "10%", 910),
            (100000, "20%", 739),
        ],
    )
    def test_break_even_matches_spreadsheet(self, price, down, expected_break_even):
        """Break-even rent matches spreadsheet values."""
        result = runner.invoke(
            app,
            [
                "analyze",
                "--price",
                str(price),
                "--rent",
                "1000",
                "--down",
                down,
                "--output",
                "json",
            ],
        )

        assert result.exit_code == 0
        data = json.loads(result.stdout)
        actual = data["analysis"]["break_even_rent"]

        # Allow 1% tolerance
        assert abs(actual - expected_break_even) / expected_break_even < 0.01
