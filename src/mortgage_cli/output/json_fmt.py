"""JSON output formatter."""

import json
from typing import Any

from mortgage_cli.models.profile import Profile
from mortgage_cli.models.results import AnalysisResult, MatrixCell


class JsonFormatter:
    """Format analysis results as JSON."""

    def format_analysis(self, result: AnalysisResult, profile: Profile) -> str:
        """Format single property analysis as JSON.

        Args:
            result: Analysis result
            profile: Profile used for analysis

        Returns:
            JSON string
        """
        output = {
            "property": {
                "price": result.property_price,
                "expected_rent": result.expected_rent,
                "down_payment_percent": result.down_payment_percent,
            },
            "analysis": {
                "break_even_rent": round(result.break_even_rent, 2),
                "cash_on_cash_return": round(result.cash_on_cash_return, 4),
                "monthly_surplus_shortfall": round(result.monthly_surplus_shortfall, 2),
                "verdict": result.verdict.value,
                "within_budget": result.within_budget,
            },
            "upfront_costs": {
                "down_payment": round(result.upfront_costs.down_payment, 2),
                "notary_legal": round(result.upfront_costs.notary_legal, 2),
                "bank_arrangement": round(result.upfront_costs.bank_arrangement, 2),
                "survey_valuation": round(result.upfront_costs.survey_valuation, 2),
                "mortgage_broker": round(result.upfront_costs.mortgage_broker, 2),
                "other": round(result.upfront_costs.other, 2),
                "total": round(result.upfront_costs.total, 2),
            },
            "monthly": {
                "mortgage_payment": round(result.monthly.mortgage_payment, 2),
                "fixed_costs": round(result.monthly.fixed_costs, 2),
                "total": round(result.monthly.total, 2),
            },
            "warnings": result.warnings,
            "profile": {
                "name": profile.name,
                "interest_rate": profile.mortgage.interest_rate,
                "duration_years": profile.mortgage.duration_years,
                "target_rent": profile.budget.target_rent,
                "budget": profile.budget.total_available,
            },
        }

        return json.dumps(output, indent=2)

    def format_matrix(
        self,
        matrix: list[list[MatrixCell]],
        prices: list[float],
        down_payments: list[float],
        target_rent: float,
        profile: Profile,
    ) -> str:
        """Format sensitivity matrix as JSON.

        Args:
            matrix: 2D list of MatrixCell objects
            prices: List of purchase prices (columns)
            down_payments: List of down payment percentages (rows)
            target_rent: Target rent for comparison
            profile: Profile used for analysis

        Returns:
            JSON string
        """
        cells: list[dict[str, Any]] = []

        for row_idx, row in enumerate(matrix):
            for col_idx, cell in enumerate(row):
                cells.append(
                    {
                        "price": prices[col_idx],
                        "down_payment_percent": down_payments[row_idx],
                        "break_even_rent": round(cell.break_even_rent, 2),
                        "verdict": cell.verdict.value,
                        "within_budget": cell.within_budget,
                    }
                )

        output = {
            "matrix": {
                "prices": prices,
                "down_payments": down_payments,
                "target_rent": target_rent,
                "cells": cells,
            },
            "profile": {
                "name": profile.name,
                "interest_rate": profile.mortgage.interest_rate,
                "duration_years": profile.mortgage.duration_years,
                "budget": profile.budget.total_available,
            },
        }

        return json.dumps(output, indent=2)

    def format_profile_list(self, profiles: list[tuple[str, str]]) -> str:
        """Format profile list as JSON.

        Args:
            profiles: List of (name, description) tuples

        Returns:
            JSON string
        """
        output = {
            "profiles": [
                {"name": name, "description": desc} for name, desc in profiles
            ]
        }
        return json.dumps(output, indent=2)

    def format_profile_comparison(
        self,
        comparisons: list[tuple[Profile, AnalysisResult]],
        price: float,
        rent: float,
    ) -> str:
        """Format profile comparison as JSON.

        Args:
            comparisons: List of (profile, result) tuples
            price: Property price analyzed
            rent: Expected rent analyzed

        Returns:
            JSON string
        """
        results = []
        for profile, result in comparisons:
            results.append(
                {
                    "profile": profile.name,
                    "interest_rate": profile.mortgage.interest_rate,
                    "duration_years": profile.mortgage.duration_years,
                    "down_payment_percent": result.down_payment_percent,
                    "break_even_rent": round(result.break_even_rent, 2),
                    "cash_on_cash_return": round(result.cash_on_cash_return, 4),
                    "upfront_cost": round(result.upfront_costs.total, 2),
                    "verdict": result.verdict.value,
                }
            )

        output = {
            "property": {
                "price": price,
                "expected_rent": rent,
            },
            "comparison": results,
        }

        return json.dumps(output, indent=2)
