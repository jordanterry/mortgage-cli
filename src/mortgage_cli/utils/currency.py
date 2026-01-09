"""Currency formatting utilities."""


def format_currency(amount: float, symbol: str = "€", decimals: int = 0) -> str:
    """Format a number as currency.

    Args:
        amount: The amount to format
        symbol: Currency symbol (default: €)
        decimals: Number of decimal places (default: 0)

    Returns:
        Formatted currency string (e.g., "€1,234")

    Examples:
        >>> format_currency(1234.56)
        '€1,235'
        >>> format_currency(1234.56, decimals=2)
        '€1,234.56'
        >>> format_currency(1234.56, symbol='$')
        '$1,235'
    """
    if decimals == 0:
        return f"{symbol}{amount:,.0f}"
    return f"{symbol}{amount:,.{decimals}f}"
