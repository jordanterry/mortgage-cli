"""Analysis result schemas."""

from enum import Enum

from pydantic import BaseModel, Field, computed_field


class Verdict(str, Enum):
    """Investment viability verdict (for color coding)."""

    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    OVER_BUDGET = "over_budget"


class UpfrontCosts(BaseModel):
    """Itemized one-time purchase costs."""

    down_payment: float = Field(ge=0)
    notary_legal: float = Field(ge=0)
    bank_arrangement: float = Field(ge=0)
    survey_valuation: float = Field(ge=0)
    mortgage_broker: float = Field(ge=0, default=0)
    other: float = Field(ge=0, default=0)

    @computed_field
    @property
    def total(self) -> float:
        """Total upfront investment required."""
        return (
            self.down_payment
            + self.notary_legal
            + self.bank_arrangement
            + self.survey_valuation
            + self.mortgage_broker
            + self.other
        )


class MonthlyBreakdown(BaseModel):
    """Monthly payment components."""

    mortgage_payment: float = Field(ge=0, description="Monthly mortgage P+I payment")
    fixed_costs: float = Field(ge=0, description="Fixed monthly property costs")

    @computed_field
    @property
    def total(self) -> float:
        """Total monthly cost (break-even rent)."""
        return self.mortgage_payment + self.fixed_costs


class AnalysisResult(BaseModel):
    """Complete investment analysis output."""

    # Input echo
    property_price: float
    expected_rent: float
    down_payment_percent: float

    # Calculated costs
    upfront_costs: UpfrontCosts
    monthly: MonthlyBreakdown

    # Key metrics
    break_even_rent: float
    cash_on_cash_return: float
    monthly_surplus_shortfall: float

    # Assessment
    verdict: Verdict
    within_budget: bool
    warnings: list[str] = Field(default_factory=list)


class MatrixCell(BaseModel):
    """Single cell in sensitivity matrix."""

    price: float
    down_payment_percent: float
    break_even_rent: float
    verdict: Verdict
    within_budget: bool


class AmortizationEntry(BaseModel):
    """Single year in amortization schedule."""

    year: int
    principal_paid: float
    interest_paid: float
    remaining_balance: float
    equity_percent: float
