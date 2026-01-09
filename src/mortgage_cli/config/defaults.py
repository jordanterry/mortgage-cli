"""Built-in default profile and configuration."""

from mortgage_cli.models.profile import (
    Budget,
    CostItem,
    MonthlyCosts,
    MortgageTerms,
    Profile,
    PurchaseCosts,
    Thresholds,
)

# Default profile based on the original spreadsheet configuration
DEFAULT_PROFILE = Profile(
    name="default",
    description="Standard investment parameters",
    mortgage=MortgageTerms(
        interest_rate=0.04,  # 4% annual interest
        insurance_rate=0.001,  # 0.1% mortgage insurance
        duration_years=20,
        default_down_payment=0.20,  # 20%
    ),
    budget=Budget(
        total_available=80000,  # €80K available capital
        target_rent=1000,  # €1000/month target
    ),
    monthly_costs=MonthlyCosts(
        property_tax=50,
        insurance=50,
        maintenance=100,
        management=50,
        # Total: €250/month
    ),
    purchase_costs=PurchaseCosts(
        notary_legal=CostItem(type="percentage", value=0.03),  # 3%
        bank_arrangement=CostItem(type="percentage", value=0.01),  # 1%
        survey_valuation=CostItem(type="fixed", value=400),  # €400
    ),
    thresholds=Thresholds(
        green_below=0.80,  # Green if < 80% of target
        yellow_below=1.00,  # Yellow if < 100% of target
    ),
)
