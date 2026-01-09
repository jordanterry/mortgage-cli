"""Analyze command for single property analysis."""

from typing import Annotated, Optional

import typer
from rich.console import Console

from mortgage_cli.config.manager import ConfigManager, ProfileNotFoundError
from mortgage_cli.core.analyzer import InvestmentAnalyzer
from mortgage_cli.models.property import PropertyInput
from mortgage_cli.output import get_formatter
from mortgage_cli.utils.percentage import parse_percentage

console = Console()


def analyze(
    price: Annotated[
        float,
        typer.Option("--price", "-p", help="Property purchase price"),
    ],
    rent: Annotated[
        float,
        typer.Option("--rent", "-r", help="Expected monthly rental income"),
    ],
    down: Annotated[
        Optional[str],
        typer.Option(
            "--down",
            "-d",
            help="Down payment percentage (e.g., '20%' or '0.20')",
        ),
    ] = None,
    profile: Annotated[
        str,
        typer.Option("--profile", help="Profile name to use"),
    ] = "default",
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="Output format: table, json"),
    ] = "table",
) -> None:
    """Analyze a single property investment.

    Calculate break-even rent, cash-on-cash return, and investment viability
    for a property at a given price and expected rent.

    Examples:
        mortgage-cli analyze --price 150000 --rent 900
        mortgage-cli analyze -p 200000 -r 1200 --down 25%
        mortgage-cli analyze --price 150000 --rent 900 --output json
    """
    # Load profile
    config_manager = ConfigManager()
    try:
        profile_data = config_manager.load_profile(profile)
    except ProfileNotFoundError:
        console.print(f"[red]Error: Profile '{profile}' not found[/red]")
        raise typer.Exit(1)

    # Parse down payment if provided
    down_pct: float | None = None
    if down is not None:
        try:
            down_pct = parse_percentage(down)
        except ValueError:
            console.print(f"[red]Error: Invalid down payment '{down}'[/red]")
            raise typer.Exit(1)

    # Create property input
    property_input = PropertyInput(
        price=price,
        expected_rent=rent,
        down_payment_percent=down_pct,
    )

    # Run analysis
    analyzer = InvestmentAnalyzer(profile_data)
    result = analyzer.analyze(property_input)

    # Output result
    try:
        formatter = get_formatter(output)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

    if output == "json":
        console.print(formatter.format_analysis(result, profile_data))
    else:
        formatter.format_analysis(result, profile_data)
