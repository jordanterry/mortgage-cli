"""Profile management commands."""

from typing import Annotated, Optional

import typer
from rich.console import Console

from mortgage_cli.config.manager import (
    ConfigManager,
    ProfileExistsError,
    ProfileNotFoundError,
)
from mortgage_cli.core.analyzer import InvestmentAnalyzer
from mortgage_cli.models.property import PropertyInput
from mortgage_cli.output import get_formatter

console = Console()
app = typer.Typer(help="Manage investment profiles")


@app.command("list")
def list_profiles(
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="Output format: table, json"),
    ] = "table",
) -> None:
    """List all available profiles."""
    config_manager = ConfigManager()
    profiles = config_manager.list_profiles()

    formatter = get_formatter(output)

    if output == "json":
        console.print(formatter.format_profile_list(profiles))
    else:
        formatter.format_profile_list(profiles)


@app.command("show")
def show_profile(
    name: Annotated[str, typer.Argument(help="Profile name to show")],
) -> None:
    """Show details of a profile."""
    config_manager = ConfigManager()

    try:
        profile = config_manager.load_profile(name)
    except ProfileNotFoundError:
        console.print(f"[red]Error: Profile '{name}' not found[/red]")
        raise typer.Exit(1)

    console.print(f"\n[bold]Profile: {profile.name}[/bold]")
    console.print(f"Description: {profile.description or '(none)'}\n")

    console.print("[bold]Mortgage Terms[/bold]")
    console.print(f"  Interest Rate: {profile.mortgage.interest_rate * 100:.1f}%")
    console.print(f"  Insurance Rate: {profile.mortgage.insurance_rate * 100:.2f}%")
    console.print(f"  Duration: {profile.mortgage.duration_years} years")
    console.print(f"  Default Down Payment: {profile.mortgage.default_down_payment * 100:.0f}%")

    console.print("\n[bold]Budget[/bold]")
    console.print(f"  Total Available: €{profile.budget.total_available:,.0f}")
    console.print(f"  Target Rent: €{profile.budget.target_rent:,.0f}/month")

    console.print("\n[bold]Monthly Costs[/bold]")
    console.print(f"  Property Tax: €{profile.monthly_costs.property_tax:,.0f}")
    console.print(f"  Insurance: €{profile.monthly_costs.insurance:,.0f}")
    console.print(f"  Maintenance: €{profile.monthly_costs.maintenance:,.0f}")
    console.print(f"  Management: €{profile.monthly_costs.management:,.0f}")
    console.print(f"  [bold]Total: €{profile.monthly_costs.total:,.0f}/month[/bold]")

    console.print("\n[bold]Purchase Costs[/bold]")
    for cost_name, cost_item in [
        ("Notary/Legal", profile.purchase_costs.notary_legal),
        ("Bank Arrangement", profile.purchase_costs.bank_arrangement),
        ("Survey/Valuation", profile.purchase_costs.survey_valuation),
        ("Mortgage Broker", profile.purchase_costs.mortgage_broker),
        ("Other", profile.purchase_costs.other),
    ]:
        if cost_item.value > 0:
            if cost_item.type == "percentage":
                console.print(f"  {cost_name}: {cost_item.value * 100:.1f}% of price")
            else:
                console.print(f"  {cost_name}: €{cost_item.value:,.0f}")

    console.print("\n[bold]Thresholds[/bold]")
    console.print(f"  Green Below: {profile.thresholds.green_below * 100:.0f}% of target")
    console.print(f"  Yellow Below: {profile.thresholds.yellow_below * 100:.0f}% of target")
    console.print()


@app.command("create")
def create_profile(
    name: Annotated[str, typer.Argument(help="Name for the new profile")],
    description: Annotated[
        str,
        typer.Option("--description", "-d", help="Profile description"),
    ] = "",
    base: Annotated[
        str,
        typer.Option("--base", "-b", help="Profile to copy settings from"),
    ] = "default",
) -> None:
    """Create a new profile.

    Creates a new profile by copying settings from an existing profile
    (default: 'default'). Use 'mortgage-cli profile edit' to customize.
    """
    config_manager = ConfigManager()

    try:
        profile = config_manager.create_profile(name, description, base)
        console.print(f"[green]Created profile '{name}' based on '{base}'[/green]")
        console.print(f"Edit with: [bold]mortgage-cli profile edit {name}[/bold]")
    except ProfileExistsError:
        console.print(f"[red]Error: Profile '{name}' already exists[/red]")
        raise typer.Exit(1)
    except ProfileNotFoundError:
        console.print(f"[red]Error: Base profile '{base}' not found[/red]")
        raise typer.Exit(1)


@app.command("delete")
def delete_profile(
    name: Annotated[str, typer.Argument(help="Profile name to delete")],
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Skip confirmation"),
    ] = False,
) -> None:
    """Delete a profile."""
    if name == "default":
        console.print("[red]Error: Cannot delete the built-in 'default' profile[/red]")
        raise typer.Exit(1)

    config_manager = ConfigManager()

    if not config_manager.profile_exists(name):
        console.print(f"[red]Error: Profile '{name}' not found[/red]")
        raise typer.Exit(1)

    if not force:
        confirm = typer.confirm(f"Delete profile '{name}'?")
        if not confirm:
            console.print("Cancelled")
            raise typer.Exit(0)

    try:
        config_manager.delete_profile(name)
        console.print(f"[green]Deleted profile '{name}'[/green]")
    except ProfileNotFoundError:
        console.print(f"[red]Error: Profile '{name}' not found[/red]")
        raise typer.Exit(1)


@app.command("compare")
def compare_profiles(
    price: Annotated[
        float,
        typer.Option("--price", "-p", help="Property purchase price"),
    ],
    rent: Annotated[
        float,
        typer.Option("--rent", "-r", help="Expected monthly rental income"),
    ],
    profiles: Annotated[
        str,
        typer.Option("--profiles", help="Comma-separated list of profile names"),
    ],
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="Output format: table, json"),
    ] = "table",
) -> None:
    """Compare analysis across multiple profiles.

    Example:
        mortgage-cli profile compare --price 150000 --rent 900 --profiles default,conservative
    """
    config_manager = ConfigManager()
    profile_names = [p.strip() for p in profiles.split(",")]

    # Load profiles and run analysis
    comparisons = []
    for name in profile_names:
        try:
            profile_data = config_manager.load_profile(name)
        except ProfileNotFoundError:
            console.print(f"[red]Error: Profile '{name}' not found[/red]")
            raise typer.Exit(1)

        analyzer = InvestmentAnalyzer(profile_data)
        result = analyzer.analyze(PropertyInput(price=price, expected_rent=rent))
        comparisons.append((profile_data, result))

    # Output
    formatter = get_formatter(output)
    if output == "json":
        console.print(formatter.format_profile_comparison(comparisons, price, rent))
    else:
        formatter.format_profile_comparison(comparisons, price, rent)
