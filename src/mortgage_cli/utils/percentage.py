"""Percentage parsing and formatting utilities."""

import re


def parse_percentage(value: str) -> float:
    """Parse a percentage string to a decimal.

    Accepts formats like "20%", "20", "0.20".

    Args:
        value: String to parse

    Returns:
        Decimal value (e.g., 0.20 for "20%")

    Raises:
        ValueError: If value cannot be parsed

    Examples:
        >>> parse_percentage("20%")
        0.2
        >>> parse_percentage("20")
        0.2
        >>> parse_percentage("0.20")
        0.2
    """
    value = value.strip()

    # Handle percentage sign
    if value.endswith("%"):
        value = value[:-1].strip()
        num = float(value)
        return num / 100

    num = float(value)

    # If the value is > 1, assume it's a percentage (e.g., "20" means 20%)
    if num > 1:
        return num / 100

    return num


def format_percentage(value: float, decimals: int = 0) -> str:
    """Format a decimal as a percentage string.

    Args:
        value: Decimal value (e.g., 0.20)
        decimals: Number of decimal places

    Returns:
        Formatted percentage (e.g., "20%")

    Examples:
        >>> format_percentage(0.20)
        '20%'
        >>> format_percentage(0.1234, decimals=1)
        '12.3%'
    """
    pct = value * 100
    if decimals == 0:
        return f"{pct:.0f}%"
    return f"{pct:.{decimals}f}%"
