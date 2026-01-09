"""Amortize command for payment schedules."""

from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from mortgage_cli.config.manager import ConfigManager, ProfileNotFoundError
from mortgage_cli.core.amortization import AmortizationGenerator
from mortgage_cli.core.calculator import MortgageCalculator
from mortgage_cli.utils.currency import format_currency
from mortgage_cli.utils.percentage import format_percentage, parse_percentage

console = Console()


def amortize(
    price: Annotated[
        float,
        typer.Option("--price", "-p", help="Property purchase price"),
    ],
    down: Annotated[
        Optional[str],
        typer.Option("--down", "-d", help="Down payment percentage (e.g., '20%')"),
    ] = None,
    years: Annotated[
        Optional[int],
        typer.Option("--years", "-y", help="Show only first N years"),
    ] = None,
    profile: Annotated[
        str,
        typer.Option("--profile", help="Profile name to use"),
    ] = "default",
) -> None:
    """Generate amortization schedule.

    Shows year-by-year breakdown of principal and interest payments,
    remaining balance, and equity buildup.

    Examples:
        mortgage-cli amortize --price 150000
        mortgage-cli amortize --price 150000 --down 25% --years 5
    """
    # Load profile
    config_manager = ConfigManager()
    try:
        profile_data = config_manager.load_profile(profile)
    except ProfileNotFoundError:
        console.print(f"[red]Error: Profile '{profile}' not found[/red]")
        raise typer.Exit(1)

    # Parse down payment
    down_pct = profile_data.mortgage.default_down_payment
    if down is not None:
        try:
            down_pct = parse_percentage(down)
        except ValueError:
            console.print(f"[red]Error: Invalid down payment '{down}'[/red]")
            raise typer.Exit(1)

    # Calculate loan details
    calculator = MortgageCalculator()
    loan_amount = calculator.calculate_loan_amount(price, down_pct)
    effective_rate = calculator.calculate_effective_rate(
        profile_data.mortgage.interest_rate,
        profile_data.mortgage.insurance_rate,
    )
    monthly_payment = calculator.calculate_monthly_payment(
        loan_amount,
        effective_rate,
        profile_data.mortgage.duration_years,
    )

    # Generate schedule
    generator = AmortizationGenerator()
    schedule = generator.generate_schedule(
        principal=loan_amount,
        annual_rate=effective_rate,
        years=profile_data.mortgage.duration_years,
        original_property_value=price,
        limit_years=years,
    )

    # Header
    console.print()
    title = (
        f"Amortization Schedule: {format_currency(loan_amount)} loan "
        f"@ {format_percentage(effective_rate, 1)} over {profile_data.mortgage.duration_years} years"
    )
    console.print(f"[bold]{title}[/bold]")
    console.print(f"Monthly Payment: {format_currency(monthly_payment, decimals=2)}")
    console.print()

    # Table
    table = Table(show_header=True, header_style="bold")
    table.add_column("Year", justify="right")
    table.add_column("Principal", justify="right")
    table.add_column("Interest", justify="right")
    table.add_column("Balance", justify="right")
    table.add_column("Equity", justify="right")

    for entry in schedule:
        table.add_row(
            str(entry.year),
            format_currency(entry.principal_paid),
            format_currency(entry.interest_paid),
            format_currency(entry.remaining_balance),
            format_percentage(entry.equity_percent, 1),
        )

    console.print(table)

    # Summary
    if schedule:
        total_principal = sum(e.principal_paid for e in schedule)
        total_interest = sum(e.interest_paid for e in schedule)
        console.print()
        console.print(f"Total Principal Paid: {format_currency(total_principal)}")
        console.print(f"Total Interest Paid: {format_currency(total_interest)}")

        if years is None or years >= profile_data.mortgage.duration_years:
            total_cost = total_principal + total_interest
            console.print(f"Total Cost of Loan: {format_currency(total_cost)}")

    console.print()
