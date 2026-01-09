"""Unit tests for InvestmentAnalyzer."""

import pytest

from mortgage_cli.core.analyzer import InvestmentAnalyzer
from mortgage_cli.models.profile import Profile
from mortgage_cli.models.property import PropertyInput
from mortgage_cli.models.results import Verdict


class TestAnalyzerBasics:
    """Basic analyzer functionality tests."""

    def test_analyze_returns_result(self, default_profile: Profile):
        """Analyze returns an AnalysisResult."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(PropertyInput(price=100000, expected_rent=900))

        assert result is not None
        assert result.property_price == 100000
        assert result.expected_rent == 900

    def test_uses_profile_default_down_payment(self, default_profile: Profile):
        """Uses profile's default down payment when not specified."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(PropertyInput(price=100000, expected_rent=900))

        assert result.down_payment_percent == default_profile.mortgage.default_down_payment

    def test_overrides_down_payment(self, default_profile: Profile):
        """Uses provided down payment over profile default."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(
            PropertyInput(price=100000, expected_rent=900, down_payment_percent=0.30)
        )

        assert result.down_payment_percent == 0.30


class TestUpfrontCosts:
    """Tests for upfront cost calculations."""

    def test_down_payment_calculation(self, default_profile: Profile):
        """Down payment is calculated correctly."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(PropertyInput(price=100000, expected_rent=900))

        # 20% of €100K = €20K
        assert result.upfront_costs.down_payment == 20000

    def test_percentage_costs(self, default_profile: Profile):
        """Percentage-based costs are calculated correctly."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(PropertyInput(price=100000, expected_rent=900))

        # 3% notary = €3000
        assert result.upfront_costs.notary_legal == 3000
        # 1% bank = €1000
        assert result.upfront_costs.bank_arrangement == 1000

    def test_fixed_costs(self, default_profile: Profile):
        """Fixed costs are passed through correctly."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(PropertyInput(price=100000, expected_rent=900))

        # Fixed €400 survey
        assert result.upfront_costs.survey_valuation == 400

    def test_total_upfront_cost(self, default_profile: Profile):
        """Total upfront cost is sum of all components."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(PropertyInput(price=100000, expected_rent=900))

        expected_total = (
            result.upfront_costs.down_payment
            + result.upfront_costs.notary_legal
            + result.upfront_costs.bank_arrangement
            + result.upfront_costs.survey_valuation
            + result.upfront_costs.mortgage_broker
            + result.upfront_costs.other
        )
        assert result.upfront_costs.total == expected_total


class TestMonthlyBreakdown:
    """Tests for monthly cost calculations."""

    def test_monthly_breakdown_components(self, default_profile: Profile):
        """Monthly breakdown has mortgage payment and fixed costs."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(PropertyInput(price=100000, expected_rent=900))

        assert result.monthly.mortgage_payment > 0
        assert result.monthly.fixed_costs == default_profile.monthly_costs.total

    def test_break_even_equals_monthly_total(self, default_profile: Profile):
        """Break-even rent equals sum of monthly costs."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(PropertyInput(price=100000, expected_rent=900))

        assert result.break_even_rent == result.monthly.total


class TestCashOnCashReturn:
    """Tests for cash-on-cash return calculation."""

    def test_positive_cash_flow_positive_return(self, default_profile: Profile):
        """Positive cash flow yields positive return."""
        analyzer = InvestmentAnalyzer(default_profile)
        # High rent should yield positive return
        result = analyzer.analyze(PropertyInput(price=50000, expected_rent=800))

        assert result.monthly_surplus_shortfall > 0
        assert result.cash_on_cash_return > 0

    def test_negative_cash_flow_negative_return(self, default_profile: Profile):
        """Negative cash flow yields negative return."""
        analyzer = InvestmentAnalyzer(default_profile)
        # Low rent should yield negative return
        result = analyzer.analyze(PropertyInput(price=200000, expected_rent=500))

        assert result.monthly_surplus_shortfall < 0
        assert result.cash_on_cash_return < 0


class TestVerdictDetermination:
    """Tests for verdict color coding."""

    def test_green_verdict(self, default_profile: Profile):
        """Low break-even relative to target yields green."""
        analyzer = InvestmentAnalyzer(default_profile)
        # Low price = low break-even = green
        result = analyzer.analyze(PropertyInput(price=50000, expected_rent=800))

        # Break-even should be < 80% of €1000 target
        assert result.break_even_rent < 800
        assert result.verdict == Verdict.GREEN

    def test_yellow_verdict(self, default_profile: Profile):
        """Medium break-even relative to target yields yellow."""
        analyzer = InvestmentAnalyzer(default_profile)
        # Find a price that gives break-even between 80-100% of target (€800-€1000)
        # €130K at 20% down should give ~€885 break-even
        result = analyzer.analyze(PropertyInput(price=130000, expected_rent=900))

        # Should be yellow (between 80-100% of €1000)
        assert 800 <= result.break_even_rent <= 1000
        assert result.verdict == Verdict.YELLOW

    def test_red_verdict(self, default_profile: Profile):
        """High break-even relative to target yields red."""
        analyzer = InvestmentAnalyzer(default_profile)
        # High price = high break-even = red
        result = analyzer.analyze(PropertyInput(price=200000, expected_rent=500))

        # Break-even should be > 100% of €1000 target
        assert result.break_even_rent > 1000
        assert result.verdict == Verdict.RED

    def test_over_budget_verdict(self, default_profile: Profile):
        """Over budget yields over_budget verdict regardless of break-even."""
        analyzer = InvestmentAnalyzer(default_profile)
        # Very high price exceeds €80K budget
        result = analyzer.analyze(PropertyInput(price=500000, expected_rent=2000))

        assert not result.within_budget
        assert result.verdict == Verdict.OVER_BUDGET


class TestWarnings:
    """Tests for warning generation."""

    def test_budget_warning(self, default_profile: Profile):
        """Over budget generates warning."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(PropertyInput(price=500000, expected_rent=2000))

        assert any("exceed" in w.lower() and "budget" in w.lower() for w in result.warnings)

    def test_shortfall_warning(self, default_profile: Profile):
        """Negative cash flow generates warning."""
        analyzer = InvestmentAnalyzer(default_profile)
        result = analyzer.analyze(PropertyInput(price=150000, expected_rent=500))

        assert any("shortfall" in w.lower() for w in result.warnings)

    def test_affordability_warning(self, default_profile: Profile):
        """Very high break-even generates affordability warning."""
        analyzer = InvestmentAnalyzer(default_profile)
        # Break-even > 150% of target (€1500)
        result = analyzer.analyze(PropertyInput(price=300000, expected_rent=500))

        assert result.break_even_rent > 1500
        assert any("unrealistic" in w.lower() for w in result.warnings)

    def test_no_warnings_for_good_investment(self, default_profile: Profile):
        """Good investment has no warnings."""
        analyzer = InvestmentAnalyzer(default_profile)
        # Low price, high rent = no warnings
        result = analyzer.analyze(PropertyInput(price=50000, expected_rent=800))

        assert len(result.warnings) == 0


class TestSpreadsheetIntegration:
    """Validate analyzer against spreadsheet values."""

    @pytest.mark.parametrize(
        "price,down_pct,expected_break_even",
        [
            (100000, 0.10, 800.14),
            (120000, 0.10, 910.16),
            (100000, 0.20, 739.01),
            (100000, 0.30, 677.88),
        ],
    )
    def test_break_even_matches_spreadsheet(
        self,
        spreadsheet_profile: Profile,
        price: float,
        down_pct: float,
        expected_break_even: float,
    ):
        """Analyzer produces same break-even as spreadsheet."""
        analyzer = InvestmentAnalyzer(spreadsheet_profile)
        result = analyzer.analyze(
            PropertyInput(price=price, expected_rent=1000, down_payment_percent=down_pct)
        )

        assert result.break_even_rent == pytest.approx(expected_break_even, rel=0.005)
