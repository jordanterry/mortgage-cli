"""Unit tests for MortgageCalculator."""

import pytest

from mortgage_cli.core.calculator import MortgageCalculator


class TestCalculateMonthlyPayment:
    """Tests for PMT calculation."""

    def test_basic_pmt(self, calculator: MortgageCalculator):
        """Basic PMT calculation matches expected value."""
        # €100,000 loan at 4% for 20 years
        result = calculator.calculate_monthly_payment(100000, 0.04, 20)
        # Expected: ~€605.98 (verified with Excel PMT)
        assert result == pytest.approx(605.98, rel=0.001)

    def test_pmt_with_combined_rate(self, calculator: MortgageCalculator):
        """PMT with interest + insurance rate (4.1% effective)."""
        # €100,000 at 4.1% (4% interest + 0.1% insurance) for 20 years
        effective_rate = 0.04 + 0.001  # 4.1%
        result = calculator.calculate_monthly_payment(100000, effective_rate, 20)
        # Expected: ~€611.26 (verified with Excel PMT(4.1%/12, 240, 100000))
        assert result == pytest.approx(611.26, rel=0.001)

    def test_pmt_zero_principal(self, calculator: MortgageCalculator):
        """Zero principal returns zero payment."""
        result = calculator.calculate_monthly_payment(0, 0.04, 20)
        assert result == 0.0

    def test_pmt_zero_rate(self, calculator: MortgageCalculator):
        """Zero interest rate - simple division."""
        # €120,000 over 20 years = €500/month
        result = calculator.calculate_monthly_payment(120000, 0, 20)
        assert result == pytest.approx(500.0, rel=0.001)

    def test_pmt_various_terms(self, calculator: MortgageCalculator):
        """PMT with different loan terms."""
        principal = 100000
        rate = 0.04

        # Shorter term = higher payment
        pmt_15 = calculator.calculate_monthly_payment(principal, rate, 15)
        pmt_20 = calculator.calculate_monthly_payment(principal, rate, 20)
        pmt_25 = calculator.calculate_monthly_payment(principal, rate, 25)

        assert pmt_15 > pmt_20 > pmt_25


class TestCalculateLoanAmount:
    """Tests for loan amount calculation."""

    def test_basic_loan_amount(self, calculator: MortgageCalculator):
        """20% down payment leaves 80% as loan."""
        result = calculator.calculate_loan_amount(100000, 0.20)
        assert result == 80000

    def test_10_percent_down(self, calculator: MortgageCalculator):
        """10% down payment leaves 90% as loan."""
        result = calculator.calculate_loan_amount(100000, 0.10)
        assert result == 90000

    def test_50_percent_down(self, calculator: MortgageCalculator):
        """50% down payment leaves 50% as loan."""
        result = calculator.calculate_loan_amount(200000, 0.50)
        assert result == 100000


class TestCalculateDownPayment:
    """Tests for down payment calculation."""

    def test_20_percent_down(self, calculator: MortgageCalculator):
        """20% of €100K = €20K."""
        result = calculator.calculate_down_payment(100000, 0.20)
        assert result == 20000

    def test_10_percent_down(self, calculator: MortgageCalculator):
        """10% of €150K = €15K."""
        result = calculator.calculate_down_payment(150000, 0.10)
        assert result == 15000


class TestCalculateEffectiveRate:
    """Tests for effective rate calculation."""

    def test_combine_rates(self, calculator: MortgageCalculator):
        """Interest + insurance = effective rate."""
        result = calculator.calculate_effective_rate(0.04, 0.001)
        assert result == pytest.approx(0.041, rel=0.0001)


class TestCalculateCashOnCashReturn:
    """Tests for cash-on-cash return calculation."""

    def test_positive_return(self, calculator: MortgageCalculator):
        """Positive net income = positive return."""
        # €2400 annual profit on €40000 investment = 6%
        result = calculator.calculate_cash_on_cash_return(2400, 40000)
        assert result == pytest.approx(0.06, rel=0.001)

    def test_negative_return(self, calculator: MortgageCalculator):
        """Negative net income = negative return."""
        # -€1200 annual loss on €40000 investment = -3%
        result = calculator.calculate_cash_on_cash_return(-1200, 40000)
        assert result == pytest.approx(-0.03, rel=0.001)

    def test_zero_investment(self, calculator: MortgageCalculator):
        """Zero investment returns zero (avoid division by zero)."""
        result = calculator.calculate_cash_on_cash_return(1000, 0)
        assert result == 0.0


class TestCalculateBreakEvenRent:
    """Tests for break-even rent calculation."""

    def test_basic_break_even(self, calculator: MortgageCalculator):
        """Mortgage + fixed costs = break-even."""
        result = calculator.calculate_break_even_rent(500, 250)
        assert result == 750


class TestSpreadsheetValidation:
    """Validate calculations against actual spreadsheet values.

    These values are taken directly from the Mortgage Analyzer.xlsx file.
    The spreadsheet formula is:
        -PMT((interest+insurance)/12, duration*12, price*(1-down%)) + fixed_costs

    Where:
        - interest = 4% (0.04)
        - insurance = 0.1% (0.001)
        - duration = 20 years
        - fixed_costs = €250/month
    """

    @pytest.mark.parametrize(
        "price,down_pct,expected_break_even",
        [
            # Row 5: 10% down
            (100000, 0.10, 800.14),
            (120000, 0.10, 910.16),
            (140000, 0.10, 1020.19),
            (160000, 0.10, 1130.22),
            (180000, 0.10, 1240.25),
            # Row 6: 15% down
            (100000, 0.15, 769.57),
            (120000, 0.15, 873.49),
            # Row 7: 20% down
            (100000, 0.20, 739.01),
            (120000, 0.20, 836.81),
            (140000, 0.20, 934.61),
            # Row 8: 25% down
            (100000, 0.25, 708.45),
            (120000, 0.25, 800.14),
            # Row 9: 30% down
            (100000, 0.30, 677.88),
            (180000, 0.30, 1020.19),
        ],
    )
    def test_matches_spreadsheet(
        self,
        calculator: MortgageCalculator,
        price: float,
        down_pct: float,
        expected_break_even: float,
    ):
        """Verify break-even rent matches spreadsheet values."""
        # Spreadsheet parameters
        interest_rate = 0.04
        insurance_rate = 0.001
        duration_years = 20
        fixed_costs = 250.0

        # Calculate
        effective_rate = calculator.calculate_effective_rate(interest_rate, insurance_rate)
        loan_amount = calculator.calculate_loan_amount(price, down_pct)
        mortgage_payment = calculator.calculate_monthly_payment(
            loan_amount, effective_rate, duration_years
        )
        break_even = calculator.calculate_break_even_rent(mortgage_payment, fixed_costs)

        # Verify (allow 0.5% tolerance for floating point)
        assert break_even == pytest.approx(expected_break_even, rel=0.005)
