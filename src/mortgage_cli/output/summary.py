"""Summary/narrative output formatter."""

from mortgage_cli.models.profile import Profile
from mortgage_cli.models.results import AnalysisResult, MatrixCell, Verdict
from mortgage_cli.utils.currency import format_currency
from mortgage_cli.utils.percentage import format_percentage


class SummaryFormatter:
    """Format analysis results as human-readable narrative."""

    def format_analysis(self, result: AnalysisResult, profile: Profile) -> str:
        """Format single property analysis as narrative summary.

        Args:
            result: Analysis result
            profile: Profile used for analysis

        Returns:
            Human-readable narrative string
        """
        lines = []
        lines.append("INVESTMENT SUMMARY")
        lines.append("=" * 50)
        lines.append("")

        # Main summary
        price = format_currency(result.property_price)
        down_pct = format_percentage(result.down_payment_percent)
        down_amount = format_currency(result.upfront_costs.down_payment)
        break_even = format_currency(result.break_even_rent)
        expected = format_currency(result.expected_rent)

        lines.append(
            f"A {price} property with {down_pct} down ({down_amount}) would require "
            f"{break_even}/month in rent to break even."
        )

        # Cash flow analysis
        if result.monthly_surplus_shortfall >= 0:
            surplus = format_currency(result.monthly_surplus_shortfall)
            lines.append(
                f"At the expected rent of {expected}/month, this represents "
                f"a monthly surplus of {surplus}."
            )
        else:
            shortfall = format_currency(abs(result.monthly_surplus_shortfall))
            lines.append(
                f"At the expected rent of {expected}/month, this represents "
                f"a monthly shortfall of {shortfall}."
            )

        lines.append("")

        # Key metrics
        upfront = format_currency(result.upfront_costs.total)
        budget = format_currency(profile.budget.total_available)
        coc = format_percentage(result.cash_on_cash_return, decimals=1)

        budget_status = "within" if result.within_budget else "exceeds"
        lines.append(f"Total upfront investment: {upfront} ({budget_status} your {budget} budget)")

        coc_desc = "positive" if result.cash_on_cash_return > 0 else "negative"
        if result.cash_on_cash_return < 0:
            lines.append(f"Cash-on-cash return: {coc} ({coc_desc} due to shortfall)")
        else:
            lines.append(f"Cash-on-cash return: {coc}")

        lines.append("")

        # Recommendation
        lines.append("RECOMMENDATION:")
        recommendation = self._get_recommendation(result, profile)
        lines.append(recommendation)

        lines.append("")
        return "\n".join(lines)

    def _get_recommendation(self, result: AnalysisResult, profile: Profile) -> str:
        """Generate recommendation based on analysis."""
        if result.verdict == Verdict.OVER_BUDGET:
            shortfall = format_currency(result.upfront_costs.total - profile.budget.total_available)
            return (
                f"This property exceeds your budget by {shortfall}. Consider a less "
                f"expensive property or increasing your available capital."
            )

        if result.verdict == Verdict.GREEN:
            if result.cash_on_cash_return > 0.05:
                return (
                    "Excellent investment opportunity. Break-even rent is well below "
                    "market expectations with strong cash-on-cash returns."
                )
            return (
                "Good investment opportunity. Break-even rent is comfortably below "
                "your target, providing a margin of safety."
            )

        if result.verdict == Verdict.YELLOW:
            return (
                "Marginally viable investment. Consider negotiating a lower price "
                "or ensuring rental income meets expectations before proceeding."
            )

        # RED
        target = format_currency(profile.budget.target_rent)
        return (
            f"This property requires rent above your {target} target to break even. "
            f"Unless you can command premium rents, consider alternative properties."
        )

    def format_matrix(
        self,
        matrix: list[list[MatrixCell]],
        prices: list[float],
        down_payments: list[float],
        target_rent: float,
        profile: Profile,
    ) -> str:
        """Format sensitivity matrix as narrative summary.

        Args:
            matrix: 2D list of MatrixCell objects
            prices: List of purchase prices (columns)
            down_payments: List of down payment percentages (rows)
            target_rent: Target rent for comparison
            profile: Profile used for analysis

        Returns:
            Narrative summary string
        """
        lines = []
        lines.append("SENSITIVITY ANALYSIS SUMMARY")
        lines.append("=" * 50)
        lines.append("")

        # Count verdicts
        green_count = 0
        yellow_count = 0
        red_count = 0
        over_budget_count = 0

        viable_options = []

        for row in matrix:
            for cell in row:
                if cell.verdict == Verdict.GREEN:
                    green_count += 1
                    viable_options.append(cell)
                elif cell.verdict == Verdict.YELLOW:
                    yellow_count += 1
                    viable_options.append(cell)
                elif cell.verdict == Verdict.RED:
                    red_count += 1
                elif cell.verdict == Verdict.OVER_BUDGET:
                    over_budget_count += 1

        total = len(matrix) * len(matrix[0]) if matrix else 0

        lines.append(f"Analyzed {total} price/down-payment combinations:")
        lines.append(f"  - {green_count} good opportunities (green)")
        lines.append(f"  - {yellow_count} marginal opportunities (yellow)")
        lines.append(f"  - {red_count} poor opportunities (red)")
        if over_budget_count:
            lines.append(f"  - {over_budget_count} over budget")

        lines.append("")

        # Best options
        if viable_options:
            # Sort by break-even rent (lowest first)
            viable_options.sort(key=lambda x: x.break_even_rent)
            best = viable_options[:3]

            lines.append("Top opportunities (lowest break-even rent):")
            for i, cell in enumerate(best, 1):
                price = format_currency(cell.price)
                down = format_percentage(cell.down_payment_percent)
                be = format_currency(cell.break_even_rent)
                lines.append(f"  {i}. {price} with {down} down - break-even: {be}/month")
        else:
            lines.append(
                "No viable opportunities found in this range. Consider adjusting "
                "your price range or increasing your budget."
            )

        lines.append("")
        return "\n".join(lines)

    def format_profile_list(self, profiles: list[tuple[str, str]]) -> str:
        """Format profile list as narrative.

        Args:
            profiles: List of (name, description) tuples

        Returns:
            Narrative string
        """
        lines = []
        lines.append(f"You have {len(profiles)} profile(s) available:")
        lines.append("")
        for name, desc in profiles:
            if desc:
                lines.append(f"  - {name}: {desc}")
            else:
                lines.append(f"  - {name}")
        lines.append("")
        return "\n".join(lines)

    def format_profile_comparison(
        self,
        comparisons: list[tuple[Profile, AnalysisResult]],
        price: float,
        rent: float,
    ) -> str:
        """Format profile comparison as narrative.

        Args:
            comparisons: List of (profile, result) tuples
            price: Property price analyzed
            rent: Expected rent analyzed

        Returns:
            Narrative string
        """
        lines = []
        lines.append("PROFILE COMPARISON")
        lines.append("=" * 50)
        lines.append("")
        lines.append(
            f"Comparing {len(comparisons)} profiles for a "
            f"{format_currency(price)} property at {format_currency(rent)}/month rent:"
        )
        lines.append("")

        # Sort by break-even (lowest first)
        sorted_comparisons = sorted(comparisons, key=lambda x: x[1].break_even_rent)

        for profile, result in sorted_comparisons:
            be = format_currency(result.break_even_rent)
            coc = format_percentage(result.cash_on_cash_return, decimals=1)
            verdict = result.verdict.value.upper()
            lines.append(f"  {profile.name}:")
            lines.append(f"    Break-even: {be}/month [{verdict}]")
            lines.append(f"    Cash-on-cash return: {coc}")
            lines.append("")

        # Recommendation
        best_profile, best_result = sorted_comparisons[0]
        lines.append(
            f"Recommendation: '{best_profile.name}' profile offers the lowest "
            f"break-even rent at {format_currency(best_result.break_even_rent)}/month."
        )
        lines.append("")

        return "\n".join(lines)
