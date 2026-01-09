"""Main CLI application."""

import typer

from mortgage_cli import __version__
from mortgage_cli.commands.amortize import amortize
from mortgage_cli.commands.analyze import analyze
from mortgage_cli.commands.matrix import matrix
from mortgage_cli.commands.profile import app as profile_app

app = typer.Typer(
    name="mortgage-cli",
    help="CLI tool for analyzing rental property investments.",
    no_args_is_help=True,
)

# Register commands
app.command()(analyze)
app.command()(matrix)
app.command()(amortize)
app.add_typer(profile_app, name="profile")


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        typer.echo(f"mortgage-cli version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """mortgage-cli: Analyze rental property investments."""
    pass


if __name__ == "__main__":
    app()
