"""Pydantic data models for mortgage-cli."""

from mortgage_cli.models.profile import (
    Profile,
    MortgageTerms,
    Budget,
    MonthlyCosts,
    PurchaseCosts,
    CostItem,
    Thresholds,
)
from mortgage_cli.models.property import PropertyInput
from mortgage_cli.models.results import (
    AnalysisResult,
    UpfrontCosts,
    MonthlyBreakdown,
    Verdict,
    MatrixCell,
    AmortizationEntry,
)

__all__ = [
    "Profile",
    "MortgageTerms",
    "Budget",
    "MonthlyCosts",
    "PurchaseCosts",
    "CostItem",
    "Thresholds",
    "PropertyInput",
    "AnalysisResult",
    "UpfrontCosts",
    "MonthlyBreakdown",
    "Verdict",
    "MatrixCell",
    "AmortizationEntry",
]
