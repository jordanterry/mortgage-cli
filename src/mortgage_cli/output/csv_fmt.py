"""CSV output formatter."""

import csv
from io import StringIO
from typing import Any

from mortgage_cli.models.profile import Profile
from mortgage_cli.models.results import AnalysisResult, MatrixCell


class CsvFormatter:
    """Format analysis results as CSV."""

    def format_analysis(self, result: AnalysisResult, profile: Profile) -> str:
        """Format single property analysis as CSV.

        Args:
            result: Analysis result
            profile: Profile used for analysis

        Returns:
            CSV string with headers and single data row
        """
        output = StringIO()
        writer = csv.writer(output)

        # Headers
        headers = [
            "property_price",
            "expected_rent",
            "down_payment_percent",
            "break_even_rent",
            "cash_on_cash_return",
            "monthly_surplus_shortfall",
            "verdict",
            "within_budget",
            "upfront_total",
            "mortgage_payment",
            "fixed_costs",
            "profile",
        ]
        writer.writerow(headers)

        # Data row
        row = [
            result.property_price,
            result.expected_rent,
            result.down_payment_percent,
            round(result.break_even_rent, 2),
            round(result.cash_on_cash_return, 4),
            round(result.monthly_surplus_shortfall, 2),
            result.verdict.value,
            result.within_budget,
            round(result.upfront_costs.total, 2),
            round(result.monthly.mortgage_payment, 2),
            round(result.monthly.fixed_costs, 2),
            profile.name,
        ]
        writer.writerow(row)

        return output.getvalue()

    def format_matrix(
        self,
        matrix: list[list[MatrixCell]],
        prices: list[float],
        down_payments: list[float],
        target_rent: float,
        profile: Profile,
    ) -> str:
        """Format sensitivity matrix as CSV.

        Args:
            matrix: 2D list of MatrixCell objects
            prices: List of purchase prices (columns)
            down_payments: List of down payment percentages (rows)
            target_rent: Target rent for comparison
            profile: Profile used for analysis

        Returns:
            CSV string with one row per cell
        """
        output = StringIO()
        writer = csv.writer(output)

        # Headers
        headers = [
            "price",
            "down_payment_percent",
            "break_even_rent",
            "verdict",
            "within_budget",
        ]
        writer.writerow(headers)

        # Data rows
        for row_idx, down_pct in enumerate(down_payments):
            for col_idx, cell in enumerate(matrix[row_idx]):
                row = [
                    cell.price,
                    cell.down_payment_percent,
                    round(cell.break_even_rent, 2),
                    cell.verdict.value,
                    cell.within_budget,
                ]
                writer.writerow(row)

        return output.getvalue()

    def format_profile_list(self, profiles: list[tuple[str, str]]) -> str:
        """Format profile list as CSV.

        Args:
            profiles: List of (name, description) tuples

        Returns:
            CSV string
        """
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(["name", "description"])
        for name, description in profiles:
            writer.writerow([name, description])

        return output.getvalue()

    def format_profile_comparison(
        self,
        comparisons: list[tuple[Profile, AnalysisResult]],
        price: float,
        rent: float,
    ) -> str:
        """Format profile comparison as CSV.

        Args:
            comparisons: List of (profile, result) tuples
            price: Property price analyzed
            rent: Expected rent analyzed

        Returns:
            CSV string
        """
        output = StringIO()
        writer = csv.writer(output)

        headers = [
            "profile",
            "interest_rate",
            "duration_years",
            "down_payment_percent",
            "break_even_rent",
            "cash_on_cash_return",
            "upfront_cost",
            "verdict",
        ]
        writer.writerow(headers)

        for profile, result in comparisons:
            row = [
                profile.name,
                profile.mortgage.interest_rate,
                profile.mortgage.duration_years,
                result.down_payment_percent,
                round(result.break_even_rent, 2),
                round(result.cash_on_cash_return, 4),
                round(result.upfront_costs.total, 2),
                result.verdict.value,
            ]
            writer.writerow(row)

        return output.getvalue()
