"""
formatter.py
-----------------------------------
Helper functions for formatting allocation values.
"""


def format_allocation(value):
    """
    Converts numbers into compact Indian format.

    Examples:
    8500 -> 8.5 K
    250000 -> 2.5 L
    10000000 -> 1 Cr
    """

    try:
        value = float(value)
    except (ValueError, TypeError):
        return "-"

    if value >= 10000000:
        return f"{value / 10000000:.2f}".rstrip("0").rstrip(".") + " Cr"

    elif value >= 100000:
        return f"{value / 100000:.2f}".rstrip("0").rstrip(".") + " L"

    elif value >= 1000:
        return f"{value / 1000:.2f}".rstrip("0").rstrip(".") + " K"

    else:
        return str(int(value))