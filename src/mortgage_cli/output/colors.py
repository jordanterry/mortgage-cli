"""Color coding for verdicts and thresholds."""

from mortgage_cli.models.results import Verdict

# Rich style names for each verdict
VERDICT_COLORS: dict[Verdict, str] = {
    Verdict.GREEN: "green",
    Verdict.YELLOW: "yellow",
    Verdict.RED: "red",
    Verdict.OVER_BUDGET: "dim",
}

# Rich styles with formatting
VERDICT_STYLES: dict[Verdict, str] = {
    Verdict.GREEN: "bold green",
    Verdict.YELLOW: "bold yellow",
    Verdict.RED: "bold red",
    Verdict.OVER_BUDGET: "dim strike",
}

# Human-readable verdict labels
VERDICT_LABELS: dict[Verdict, str] = {
    Verdict.GREEN: "GOOD",
    Verdict.YELLOW: "MARGINAL",
    Verdict.RED: "POOR",
    Verdict.OVER_BUDGET: "OVER BUDGET",
}


def verdict_to_color(verdict: Verdict) -> str:
    """Get Rich color name for a verdict.

    Args:
        verdict: Verdict enum value

    Returns:
        Rich color name (e.g., "green", "yellow")
    """
    return VERDICT_COLORS.get(verdict, "white")


def verdict_to_style(verdict: Verdict) -> str:
    """Get Rich style string for a verdict.

    Args:
        verdict: Verdict enum value

    Returns:
        Rich style string (e.g., "bold green")
    """
    return VERDICT_STYLES.get(verdict, "white")


def verdict_to_label(verdict: Verdict) -> str:
    """Get human-readable label for a verdict.

    Args:
        verdict: Verdict enum value

    Returns:
        Human-readable label (e.g., "GOOD", "MARGINAL")
    """
    return VERDICT_LABELS.get(verdict, "UNKNOWN")
