"""Property input schema."""

from pydantic import BaseModel, Field


class PropertyInput(BaseModel):
    """User-provided property details for analysis."""

    price: float = Field(gt=0, description="Property purchase price")
    expected_rent: float = Field(gt=0, description="Expected monthly rental income")
    down_payment_percent: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="Down payment percentage (overrides profile default if provided)",
    )
