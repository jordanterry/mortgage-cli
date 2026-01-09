"""Amortization schedule generation."""

import numpy_financial as npf

from mortgage_cli.models.results import AmortizationEntry


class AmortizationGenerator:
    """Generate amortization schedules."""

    def generate_schedule(
        self,
        principal: float,
        annual_rate: float,
        years: int,
        original_property_value: float,
        limit_years: int | None = None,
    ) -> list[AmortizationEntry]:
        """Generate year-by-year amortization schedule.

        Args:
            principal: Loan principal amount
            annual_rate: Annual interest rate as decimal
            years: Total loan term in years
            original_property_value: Original property purchase price (for equity %)
            limit_years: Only return first N years (default: all)

        Returns:
            List of AmortizationEntry objects, one per year
        """
        if principal <= 0 or years <= 0:
            return []

        monthly_rate = annual_rate / 12 if annual_rate > 0 else 0
        total_months = years * 12
        monthly_payment = -npf.pmt(monthly_rate, total_months, principal) if annual_rate > 0 else principal / total_months

        schedule: list[AmortizationEntry] = []
        balance = principal

        num_years = limit_years if limit_years else years

        for year in range(1, num_years + 1):
            year_principal = 0.0
            year_interest = 0.0

            for _ in range(12):
                if balance <= 0:
                    break

                if annual_rate > 0:
                    interest_payment = balance * monthly_rate
                    principal_payment = min(monthly_payment - interest_payment, balance)
                else:
                    interest_payment = 0
                    principal_payment = monthly_payment

                year_interest += interest_payment
                year_principal += principal_payment
                balance = max(0, balance - principal_payment)

            # Calculate equity percentage
            # Equity = (property value - remaining loan) / property value
            equity_value = original_property_value - balance
            equity_percent = equity_value / original_property_value if original_property_value > 0 else 0

            schedule.append(
                AmortizationEntry(
                    year=year,
                    principal_paid=round(year_principal, 2),
                    interest_paid=round(year_interest, 2),
                    remaining_balance=round(balance, 2),
                    equity_percent=round(equity_percent, 4),
                )
            )

            if balance <= 0:
                break

        return schedule
