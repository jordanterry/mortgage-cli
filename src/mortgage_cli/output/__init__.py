"""Output formatting for mortgage-cli."""

from typing import Literal

from mortgage_cli.output.colors import verdict_to_color, verdict_to_style
from mortgage_cli.output.json_fmt import JsonFormatter
from mortgage_cli.output.table import TableFormatter

OutputFormat = Literal["table", "json", "csv", "summary"]


def get_formatter(format_name: str) -> TableFormatter | JsonFormatter:
    """Get the appropriate formatter for the specified format.

    Args:
        format_name: Output format name

    Returns:
        Formatter instance

    Raises:
        ValueError: If format is not supported
    """
    formatters = {
        "table": TableFormatter,
        "json": JsonFormatter,
    }

    if format_name not in formatters:
        supported = ", ".join(formatters.keys())
        raise ValueError(f"Unknown format '{format_name}'. Supported: {supported}")

    return formatters[format_name]()


__all__ = [
    "TableFormatter",
    "JsonFormatter",
    "get_formatter",
    "verdict_to_color",
    "verdict_to_style",
]
