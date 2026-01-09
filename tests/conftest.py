"""Pytest fixtures and configuration."""

import pytest

from mortgage_cli.core.calculator import MortgageCalculator
from mortgage_cli.models.profile import (
    Budget,
    CostItem,
    MonthlyCosts,
    MortgageTerms,
    Profile,
    PurchaseCosts,
    Thresholds,
)


@pytest.fixture
def calculator() -> MortgageCalculator:
    """Provide a MortgageCalculator instance."""
    return MortgageCalculator()


@pytest.fixture
def default_profile() -> Profile:
    """Provide a default profile matching the spreadsheet values."""
    return Profile(
        name="default",
        description="Standard investment parameters",
        mortgage=MortgageTerms(
            interest_rate=0.04,  # 4%
            insurance_rate=0.001,  # 0.1%
            duration_years=20,
            default_down_payment=0.20,
        ),
        budget=Budget(
            total_available=80000,
            target_rent=1000,
        ),
        monthly_costs=MonthlyCosts(
            property_tax=50,
            insurance=50,
            maintenance=100,
            management=50,
        ),
        purchase_costs=PurchaseCosts(
            notary_legal=CostItem(type="percentage", value=0.03),
            bank_arrangement=CostItem(type="percentage", value=0.01),
            survey_valuation=CostItem(type="fixed", value=400),
        ),
        thresholds=Thresholds(
            green_below=0.80,
            yellow_below=1.00,
        ),
    )


@pytest.fixture
def spreadsheet_profile() -> Profile:
    """Profile matching the exact spreadsheet configuration.

    From the spreadsheet:
    - Interest rate: 4% (J26)
    - Insurance rate: 0.1% (J27)
    - Duration: 20 years (J28)
    - Fixed costs: €250/month (C26)
    - Fixed purchase costs: €11,200 (C27 = 8200 + 3000)
    - The spreadsheet uses 8% of purchase price for variable purchase costs
    """
    return Profile(
        name="spreadsheet",
        description="Exact spreadsheet configuration",
        mortgage=MortgageTerms(
            interest_rate=0.04,
            insurance_rate=0.001,
            duration_years=20,
            default_down_payment=0.20,
        ),
        budget=Budget(
            total_available=80000,
            target_rent=1000,
        ),
        monthly_costs=MonthlyCosts(
            # Total fixed costs = €250/month
            property_tax=62.5,
            insurance=62.5,
            maintenance=62.5,
            management=62.5,
        ),
        purchase_costs=PurchaseCosts(
            # Spreadsheet uses 8% of price + €11,200 fixed
            notary_legal=CostItem(type="percentage", value=0.08),
            bank_arrangement=CostItem(type="fixed", value=0),
            survey_valuation=CostItem(type="fixed", value=11200),
        ),
        thresholds=Thresholds(
            green_below=0.75,  # €750 / €1000
            yellow_below=1.00,
        ),
    )
