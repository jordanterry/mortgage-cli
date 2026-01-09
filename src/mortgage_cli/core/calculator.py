"""Financial calculation utilities."""

import numpy_financial as npf


class MortgageCalculator:
    """Stateless mortgage calculation utilities.

    All methods are static - no instance state is maintained.
    This makes the calculator easy to test and reason about.
    """

    @staticmethod
    def calculate_monthly_payment(
        principal: float,
        annual_rate: float,
        years: int,
    ) -> float:
        """Calculate monthly mortgage payment using PMT formula.

        Args:
            principal: Loan amount (purchase price - down payment)
            annual_rate: Annual interest rate as decimal (e.g., 0.04 for 4%)
            years: Loan term in years

        Returns:
            Monthly payment amount (positive value)

        Example:
            >>> MortgageCalculator.calculate_monthly_payment(100000, 0.04, 20)
            605.98  # approximately
        """
        if principal <= 0:
            return 0.0
        if annual_rate <= 0:
            # No interest - simple division
            return principal / (years * 12)

        monthly_rate = annual_rate / 12
        months = years * 12
        # npf.pmt returns negative (cash outflow), so negate it
        return float(-npf.pmt(monthly_rate, months, principal))

    @staticmethod
    def calculate_loan_amount(
        purchase_price: float,
        down_payment_percent: float,
    ) -> float:
        """Calculate loan amount after down payment.

        Args:
            purchase_price: Total property purchase price
            down_payment_percent: Down payment as decimal (e.g., 0.20 for 20%)

        Returns:
            Loan principal amount
        """
        return purchase_price * (1 - down_payment_percent)

    @staticmethod
    def calculate_down_payment(
        purchase_price: float,
        down_payment_percent: float,
    ) -> float:
        """Calculate down payment amount.

        Args:
            purchase_price: Total property purchase price
            down_payment_percent: Down payment as decimal (e.g., 0.20 for 20%)

        Returns:
            Down payment amount
        """
        return purchase_price * down_payment_percent

    @staticmethod
    def calculate_effective_rate(
        interest_rate: float,
        insurance_rate: float,
    ) -> float:
        """Combine interest and mortgage insurance into effective rate.

        Args:
            interest_rate: Annual interest rate as decimal
            insurance_rate: Annual mortgage insurance rate as decimal

        Returns:
            Combined effective annual rate
        """
        return interest_rate + insurance_rate

    @staticmethod
    def calculate_cash_on_cash_return(
        annual_net_income: float,
        total_cash_invested: float,
    ) -> float:
        """Calculate cash-on-cash return percentage.

        Args:
            annual_net_income: Annual rental income minus all costs
            total_cash_invested: Total upfront cash investment

        Returns:
            Cash-on-cash return as decimal (e.g., 0.05 for 5%)
        """
        if total_cash_invested <= 0:
            return 0.0
        return annual_net_income / total_cash_invested

    @staticmethod
    def calculate_break_even_rent(
        mortgage_payment: float,
        fixed_monthly_costs: float,
    ) -> float:
        """Calculate break-even monthly rent.

        Args:
            mortgage_payment: Monthly mortgage payment (P+I)
            fixed_monthly_costs: Other fixed monthly costs

        Returns:
            Minimum rent needed to cover all costs
        """
        return mortgage_payment + fixed_monthly_costs
