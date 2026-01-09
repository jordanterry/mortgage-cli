"""Matrix command for sensitivity analysis."""

from typing import Annotated

import typer
from rich.console import Console

from mortgage_cli.config.manager import ConfigManager, ProfileNotFoundError
from mortgage_cli.core.analyzer import InvestmentAnalyzer
from mortgage_cli.models.property import PropertyInput
from mortgage_cli.models.results import MatrixCell
from mortgage_cli.output import get_formatter
from mortgage_cli.utils.percentage import parse_percentage

console = Console()


def matrix(
    price_min: Annotated[
        float,
        typer.Option("--price-min", help="Minimum property price"),
    ],
    price_max: Annotated[
        float,
        typer.Option("--price-max", help="Maximum property price"),
    ],
    price_step: Annotated[
        float,
        typer.Option("--price-step", help="Price increment"),
    ] = 20000,
    down_min: Annotated[
        str,
        typer.Option("--down-min", help="Minimum down payment % (e.g., '10%')"),
    ] = "10%",
    down_max: Annotated[
        str,
        typer.Option("--down-max", help="Maximum down payment % (e.g., '50%')"),
    ] = "50%",
    down_step: Annotated[
        str,
        typer.Option("--down-step", help="Down payment increment % (e.g., '5%')"),
    ] = "5%",
    rent: Annotated[
        float,
        typer.Option("--rent", "-r", help="Target rent for comparison"),
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
    """Generate a sensitivity matrix for break-even rent analysis.

    Shows break-even rent for combinations of purchase prices and
    down payment percentages, with color coding for viability.

    Examples:
        mortgage-cli matrix --price-min 100000 --price-max 200000
        mortgage-cli matrix --price-min 100000 --price-max 300000 --rent 1200
    """
    # Load profile
    config_manager = ConfigManager()
    try:
        profile_data = config_manager.load_profile(profile)
    except ProfileNotFoundError:
        console.print(f"[red]Error: Profile '{profile}' not found[/red]")
        raise typer.Exit(1)

    # Parse percentages
    try:
        down_min_pct = parse_percentage(down_min)
        down_max_pct = parse_percentage(down_max)
        down_step_pct = parse_percentage(down_step)
    except ValueError as e:
        console.print(f"[red]Error: Invalid percentage: {e}[/red]")
        raise typer.Exit(1)

    # Use profile's target rent if not specified
    target_rent = rent if rent is not None else profile_data.budget.target_rent

    # Generate ranges
    prices = _generate_range(price_min, price_max, price_step)
    down_payments = _generate_range(down_min_pct, down_max_pct, down_step_pct)

    # Calculate matrix
    analyzer = InvestmentAnalyzer(profile_data)
    matrix_data: list[list[MatrixCell]] = []

    for down_pct in down_payments:
        row: list[MatrixCell] = []
        for price in prices:
            result = analyzer.analyze(
                PropertyInput(
                    price=price,
                    expected_rent=target_rent,
                    down_payment_percent=down_pct,
                )
            )
            row.append(
                MatrixCell(
                    price=price,
                    down_payment_percent=down_pct,
                    break_even_rent=result.break_even_rent,
                    verdict=result.verdict,
                    within_budget=result.within_budget,
                )
            )
        matrix_data.append(row)

    # Output
    try:
        formatter = get_formatter(output)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

    if output == "json":
        console.print(
            formatter.format_matrix(
                matrix_data, prices, down_payments, target_rent, profile_data
            )
        )
    else:
        formatter.format_matrix(
            matrix_data, prices, down_payments, target_rent, profile_data
        )


def _generate_range(start: float, end: float, step: float) -> list[float]:
    """Generate a list of values from start to end (inclusive) with step."""
    result = []
    current = start
    while current <= end + step / 2:  # Small tolerance for floating point
        result.append(current)
        current += step
    return result
