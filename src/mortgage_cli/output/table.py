"""Rich terminal table output formatter."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mortgage_cli.models.profile import Profile
from mortgage_cli.models.results import AnalysisResult, MatrixCell, Verdict
from mortgage_cli.output.colors import verdict_to_label, verdict_to_style
from mortgage_cli.utils.currency import format_currency
from mortgage_cli.utils.percentage import format_percentage


class TableFormatter:
    """Format analysis results as Rich terminal tables."""

    def __init__(self, console: Console | None = None):
        """Initialize formatter.

        Args:
            console: Rich Console instance (creates one if not provided)
        """
        self.console = console or Console()

    def format_analysis(self, result: AnalysisResult, profile: Profile) -> None:
        """Render analysis as rich tables with color coding.

        Args:
            result: Analysis result to display
            profile: Profile used for analysis
        """
        # Header
        title = (
            f"Property Analysis: {format_currency(result.property_price)} "
            f"@ {format_currency(result.expected_rent)}/month rent"
        )
        self.console.print()
        self.console.print(Panel(title, style="bold"))

        # Upfront costs table
        self._render_upfront_costs(result)

        # Monthly breakdown table
        self._render_monthly_breakdown(result)

        # Viability summary
        self._render_viability_summary(result, profile)

        # Warnings
        if result.warnings:
            self._render_warnings(result.warnings)

        self.console.print()

    def _render_upfront_costs(self, result: AnalysisResult) -> None:
        """Render upfront costs table."""
        table = Table(title="UPFRONT COSTS", show_header=False, box=None)
        table.add_column("Item", style="dim")
        table.add_column("Amount", justify="right")

        costs = result.upfront_costs
        down_pct = format_percentage(result.down_payment_percent)

        table.add_row(f"Down Payment ({down_pct})", format_currency(costs.down_payment))
        table.add_row("Notary/Legal Fees", format_currency(costs.notary_legal))
        table.add_row("Bank Arrangement Fee", format_currency(costs.bank_arrangement))
        table.add_row("Survey/Valuation", format_currency(costs.survey_valuation))

        if costs.mortgage_broker > 0:
            table.add_row("Mortgage Broker", format_currency(costs.mortgage_broker))
        if costs.other > 0:
            table.add_row("Other", format_currency(costs.other))

        table.add_row("─" * 25, "─" * 10)
        table.add_row("Total Upfront", format_currency(costs.total), style="bold")

        self.console.print(table)
        self.console.print()

    def _render_monthly_breakdown(self, result: AnalysisResult) -> None:
        """Render monthly costs table."""
        table = Table(title="MONTHLY BREAKDOWN", show_header=False, box=None)
        table.add_column("Item", style="dim")
        table.add_column("Amount", justify="right")

        monthly = result.monthly

        table.add_row("Mortgage Payment", format_currency(monthly.mortgage_payment))
        table.add_row("Fixed Costs", format_currency(monthly.fixed_costs))
        table.add_row("─" * 25, "─" * 10)

        # Break-even with verdict color
        style = verdict_to_style(result.verdict)
        verdict_label = f"[{verdict_to_label(result.verdict)}]"
        break_even_text = Text()
        break_even_text.append(format_currency(result.break_even_rent))
        break_even_text.append(f"  {verdict_label}", style=style)

        table.add_row("Break-Even Rent", break_even_text, style="bold")

        self.console.print(table)
        self.console.print()

    def _render_viability_summary(self, result: AnalysisResult, profile: Profile) -> None:
        """Render viability summary."""
        table = Table(title="VIABILITY", show_header=False, box=None)
        table.add_column("Metric", style="dim")
        table.add_column("Value", justify="right")

        # Expected vs Break-even
        table.add_row("Expected Rent", format_currency(result.expected_rent))
        table.add_row("Break-Even Rent", format_currency(result.break_even_rent))

        # Surplus/shortfall
        if result.monthly_surplus_shortfall >= 0:
            table.add_row(
                "Monthly Surplus",
                format_currency(result.monthly_surplus_shortfall),
                style="green",
            )
        else:
            table.add_row(
                "Monthly Shortfall",
                format_currency(abs(result.monthly_surplus_shortfall)),
                style="red",
            )

        table.add_row("─" * 25, "─" * 10)

        # Cash-on-cash return
        coc_pct = format_percentage(result.cash_on_cash_return, decimals=1)
        coc_style = "green" if result.cash_on_cash_return > 0 else "red"
        table.add_row("Cash-on-Cash Return", coc_pct, style=coc_style)

        # Budget status
        budget_text = (
            f"{format_currency(result.upfront_costs.total)} / "
            f"{format_currency(profile.budget.total_available)}"
        )
        budget_status = "[OK]" if result.within_budget else "[OVER]"
        budget_style = "green" if result.within_budget else "red"
        table.add_row("Budget Status", f"{budget_text} {budget_status}", style=budget_style)

        self.console.print(table)

    def _render_warnings(self, warnings: list[str]) -> None:
        """Render warnings."""
        self.console.print()
        self.console.print("[bold yellow]WARNINGS:[/bold yellow]")
        for warning in warnings:
            self.console.print(f"  [yellow]• {warning}[/yellow]")

    def format_matrix(
        self,
        matrix: list[list[MatrixCell]],
        prices: list[float],
        down_payments: list[float],
        target_rent: float,
        profile: Profile,
    ) -> None:
        """Render sensitivity matrix as a colored table.

        Args:
            matrix: 2D list of MatrixCell objects
            prices: List of purchase prices (columns)
            down_payments: List of down payment percentages (rows)
            target_rent: Target rent for comparison
            profile: Profile used for analysis
        """
        # Title
        title = (
            f"Break-Even Rent Matrix (Target: {format_currency(target_rent)}/month, "
            f"Budget: {format_currency(profile.budget.total_available)})"
        )
        self.console.print()
        self.console.print(Panel(title, style="bold"))

        # Create table
        table = Table(show_header=True, header_style="bold")

        # Add down payment column
        table.add_column("Down %", justify="right", style="dim")

        # Add price columns
        for price in prices:
            # Format as K (e.g., €100K)
            price_k = f"€{price / 1000:.0f}K"
            table.add_column(price_k, justify="right")

        # Add rows
        for row_idx, down_pct in enumerate(down_payments):
            row_values = [format_percentage(down_pct)]

            for col_idx, cell in enumerate(matrix[row_idx]):
                style = verdict_to_style(cell.verdict)
                value = format_currency(cell.break_even_rent)
                row_values.append(f"[{style}]{value}[/{style}]")

            table.add_row(*row_values)

        self.console.print(table)

        # Legend
        self.console.print()
        green_threshold = format_currency(target_rent * profile.thresholds.green_below)
        yellow_threshold = format_currency(target_rent * profile.thresholds.yellow_below)
        self.console.print(
            f"Legend: [bold green]GREEN[/bold green] < {green_threshold} | "
            f"[bold yellow]YELLOW[/bold yellow] {green_threshold}-{yellow_threshold} | "
            f"[bold red]RED[/bold red] > {yellow_threshold} | "
            f"[dim]GRAY[/dim] = Over budget"
        )
        self.console.print()

    def format_profile_list(self, profiles: list[tuple[str, str]]) -> None:
        """Render profile list as table.

        Args:
            profiles: List of (name, description) tuples
        """
        table = Table(show_header=True, header_style="bold")
        table.add_column("NAME")
        table.add_column("DESCRIPTION")

        for name, description in profiles:
            table.add_row(name, description)

        self.console.print(table)

    def format_profile_comparison(
        self,
        comparisons: list[tuple[Profile, AnalysisResult]],
        price: float,
        rent: float,
    ) -> None:
        """Render profile comparison as table.

        Args:
            comparisons: List of (profile, result) tuples
            price: Property price analyzed
            rent: Expected rent analyzed
        """
        title = f"Profile Comparison: {format_currency(price)} @ {format_currency(rent)}/month"
        self.console.print()
        self.console.print(Panel(title, style="bold"))

        table = Table(show_header=True, header_style="bold")

        # First column for metric names
        table.add_column("", style="dim")

        # Add a column for each profile
        for profile, _ in comparisons:
            table.add_column(profile.name, justify="right")

        # Add rows for each metric
        metrics = [
            ("Interest Rate", lambda p, r: format_percentage(p.mortgage.interest_rate, 1)),
            ("Duration", lambda p, r: f"{p.mortgage.duration_years} years"),
            ("Down Payment", lambda p, r: format_percentage(r.down_payment_percent)),
            ("─" * 15, lambda p, r: "─" * 10),
            ("Break-Even Rent", lambda p, r: format_currency(r.break_even_rent)),
            ("Cash-on-Cash", lambda p, r: format_percentage(r.cash_on_cash_return, 1)),
            ("Upfront Cost", lambda p, r: format_currency(r.upfront_costs.total)),
            (
                "Verdict",
                lambda p, r: f"[{verdict_to_style(r.verdict)}]{verdict_to_label(r.verdict)}[/{verdict_to_style(r.verdict)}]",
            ),
        ]

        for metric_name, value_fn in metrics:
            row = [metric_name]
            for profile, result in comparisons:
                row.append(value_fn(profile, result))
            table.add_row(*row)

        self.console.print(table)
        self.console.print()
