"""Profile configuration schema."""

from typing import Literal

from pydantic import BaseModel, Field


class MortgageTerms(BaseModel):
    """Mortgage loan parameters."""

    interest_rate: float = Field(
        ge=0, le=1, description="Annual interest rate as decimal (e.g., 0.04 for 4%)"
    )
    insurance_rate: float = Field(
        ge=0, le=1, default=0.001, description="Annual mortgage insurance rate"
    )
    duration_years: int = Field(ge=1, le=50, default=20, description="Loan term in years")
    default_down_payment: float = Field(
        ge=0, le=1, default=0.20, description="Default down payment percentage"
    )


class Budget(BaseModel):
    """Budget constraints."""

    total_available: float = Field(ge=0, description="Total available capital for investment")
    target_rent: float = Field(ge=0, description="Target monthly rental income")


class CostItem(BaseModel):
    """Single cost item, either fixed or percentage-based."""

    type: Literal["percentage", "fixed"]
    value: float = Field(ge=0)

    def calculate(self, base_amount: float) -> float:
        """Calculate the actual cost given a base amount (purchase price)."""
        if self.type == "percentage":
            return base_amount * self.value
        return self.value


class MonthlyCosts(BaseModel):
    """Fixed monthly property costs."""

    property_tax: float = Field(ge=0, default=0, description="Monthly property tax")
    insurance: float = Field(ge=0, default=0, description="Monthly property insurance")
    maintenance: float = Field(ge=0, default=0, description="Monthly maintenance reserve")
    management: float = Field(ge=0, default=0, description="Property management fee")

    @property
    def total(self) -> float:
        """Total monthly fixed costs."""
        return self.property_tax + self.insurance + self.maintenance + self.management


class PurchaseCosts(BaseModel):
    """One-time purchase costs (itemized)."""

    notary_legal: CostItem = Field(description="Notary and legal fees")
    bank_arrangement: CostItem = Field(description="Bank arrangement/origination fee")
    survey_valuation: CostItem = Field(description="Property survey/valuation fee")
    mortgage_broker: CostItem = Field(
        default_factory=lambda: CostItem(type="fixed", value=0),
        description="Mortgage broker fee",
    )
    other: CostItem = Field(
        default_factory=lambda: CostItem(type="fixed", value=0),
        description="Other purchase costs",
    )

    def calculate_total(self, purchase_price: float) -> float:
        """Calculate total purchase costs for a given price."""
        return (
            self.notary_legal.calculate(purchase_price)
            + self.bank_arrangement.calculate(purchase_price)
            + self.survey_valuation.calculate(purchase_price)
            + self.mortgage_broker.calculate(purchase_price)
            + self.other.calculate(purchase_price)
        )


class Thresholds(BaseModel):
    """Color coding thresholds for viability assessment."""

    green_below: float = Field(
        ge=0, le=1, default=0.80, description="Green if break-even < this % of target rent"
    )
    yellow_below: float = Field(
        ge=0, le=1, default=1.00, description="Yellow if break-even < this % of target rent"
    )


class Profile(BaseModel):
    """Complete investment profile configuration."""

    name: str = Field(description="Profile name")
    description: str = Field(default="", description="Profile description")
    mortgage: MortgageTerms
    budget: Budget
    monthly_costs: MonthlyCosts
    purchase_costs: PurchaseCosts
    thresholds: Thresholds = Field(default_factory=Thresholds)
