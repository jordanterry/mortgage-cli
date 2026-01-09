"""Investment analysis orchestration."""

from mortgage_cli.core.calculator import MortgageCalculator
from mortgage_cli.models.profile import Profile
from mortgage_cli.models.property import PropertyInput
from mortgage_cli.models.results import (
    AnalysisResult,
    MonthlyBreakdown,
    UpfrontCosts,
    Verdict,
)


class InvestmentAnalyzer:
    """Orchestrates complete investment analysis.

    Combines the calculator with profile configuration to produce
    a full analysis of a property investment.
    """

    def __init__(self, profile: Profile, calculator: MortgageCalculator | None = None):
        """Initialize analyzer with profile and optional calculator.

        Args:
            profile: Investment profile with mortgage terms and costs
            calculator: MortgageCalculator instance (creates one if not provided)
        """
        self.profile = profile
        self.calculator = calculator or MortgageCalculator()

    def analyze(self, property_input: PropertyInput) -> AnalysisResult:
        """Perform complete investment analysis.

        Args:
            property_input: Property details (price, expected rent, optional down payment)

        Returns:
            Complete analysis result with costs, metrics, and verdict
        """
        # Determine down payment percentage
        down_pct = (
            property_input.down_payment_percent
            if property_input.down_payment_percent is not None
            else self.profile.mortgage.default_down_payment
        )

        # Calculate upfront costs
        upfront_costs = self._calculate_upfront_costs(property_input.price, down_pct)

        # Calculate mortgage payment
        loan_amount = self.calculator.calculate_loan_amount(property_input.price, down_pct)
        effective_rate = self.calculator.calculate_effective_rate(
            self.profile.mortgage.interest_rate,
            self.profile.mortgage.insurance_rate,
        )
        mortgage_payment = self.calculator.calculate_monthly_payment(
            loan_amount,
            effective_rate,
            self.profile.mortgage.duration_years,
        )

        # Calculate break-even rent
        monthly = MonthlyBreakdown(
            mortgage_payment=mortgage_payment,
            fixed_costs=self.profile.monthly_costs.total,
        )
        break_even_rent = monthly.total

        # Calculate returns
        monthly_surplus_shortfall = property_input.expected_rent - break_even_rent
        annual_net_income = monthly_surplus_shortfall * 12
        cash_on_cash_return = self.calculator.calculate_cash_on_cash_return(
            annual_net_income,
            upfront_costs.total,
        )

        # Determine verdict and budget status
        within_budget = upfront_costs.total <= self.profile.budget.total_available
        verdict = self._determine_verdict(break_even_rent, within_budget)

        # Generate warnings
        warnings = self._generate_warnings(
            break_even_rent=break_even_rent,
            expected_rent=property_input.expected_rent,
            upfront_total=upfront_costs.total,
            within_budget=within_budget,
        )

        return AnalysisResult(
            property_price=property_input.price,
            expected_rent=property_input.expected_rent,
            down_payment_percent=down_pct,
            upfront_costs=upfront_costs,
            monthly=monthly,
            break_even_rent=break_even_rent,
            cash_on_cash_return=cash_on_cash_return,
            monthly_surplus_shortfall=monthly_surplus_shortfall,
            verdict=verdict,
            within_budget=within_budget,
            warnings=warnings,
        )

    def _calculate_upfront_costs(self, price: float, down_pct: float) -> UpfrontCosts:
        """Calculate all one-time purchase costs.

        Args:
            price: Property purchase price
            down_pct: Down payment percentage as decimal

        Returns:
            Itemized upfront costs
        """
        down_payment = self.calculator.calculate_down_payment(price, down_pct)
        purchase_costs = self.profile.purchase_costs

        return UpfrontCosts(
            down_payment=down_payment,
            notary_legal=purchase_costs.notary_legal.calculate(price),
            bank_arrangement=purchase_costs.bank_arrangement.calculate(price),
            survey_valuation=purchase_costs.survey_valuation.calculate(price),
            mortgage_broker=purchase_costs.mortgage_broker.calculate(price),
            other=purchase_costs.other.calculate(price),
        )

    def _determine_verdict(self, break_even_rent: float, within_budget: bool) -> Verdict:
        """Determine color-coded verdict based on thresholds.

        Args:
            break_even_rent: Calculated break-even rent
            within_budget: Whether upfront costs are within budget

        Returns:
            Verdict enum value
        """
        if not within_budget:
            return Verdict.OVER_BUDGET

        target_rent = self.profile.budget.target_rent
        if target_rent <= 0:
            return Verdict.RED

        ratio = break_even_rent / target_rent

        if ratio < self.profile.thresholds.green_below:
            return Verdict.GREEN
        elif ratio < self.profile.thresholds.yellow_below:
            return Verdict.YELLOW
        return Verdict.RED

    def _generate_warnings(
        self,
        break_even_rent: float,
        expected_rent: float,
        upfront_total: float,
        within_budget: bool,
    ) -> list[str]:
        """Generate validation warnings.

        Args:
            break_even_rent: Calculated break-even rent
            expected_rent: User's expected rental income
            upfront_total: Total upfront investment
            within_budget: Whether within budget constraint

        Returns:
            List of warning messages
        """
        warnings: list[str] = []

        # Budget warning
        if not within_budget:
            warnings.append(
                f"Total upfront costs ({upfront_total:,.0f}) exceed "
                f"budget of {self.profile.budget.total_available:,.0f}"
            )

        # Cash flow warning
        if break_even_rent > expected_rent:
            shortfall = break_even_rent - expected_rent
            warnings.append(f"Monthly shortfall of {shortfall:,.0f}")

        # Affordability warning
        target_rent = self.profile.budget.target_rent
        if target_rent > 0 and break_even_rent > target_rent * 1.5:
            warnings.append("Break-even rent may be unrealistic for this market")

        return warnings
