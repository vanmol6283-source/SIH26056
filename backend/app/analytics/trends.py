"""Time-window trend analytics."""

from collections.abc import Sequence

from .afpi import calculate_afpi_trend
from .time_based import calculate_price_changes


def _direction(change: float, tolerance: float = 1e-9) -> str:
    if change > tolerance:
        return "increasing"
    if change < -tolerance:
        return "decreasing"
    return "stable"


def calculate_fare_trends(
    current_fare: float,
    historical_fare_24h: float,
    historical_fare_7d: float,
    historical_fare_30d: float,
) -> dict[str, dict[str, float | str]]:
    """Return percentage change and direction for all required windows."""
    changes = calculate_price_changes(
        current_fare,
        historical_fare_24h,
        historical_fare_7d,
        historical_fare_30d,
    )
    return {
        window: {"change_percent": change, "direction": _direction(change)}
        for window, change in changes.items()
    }


def calculate_afpi_trends(
    afpi_values_24h: Sequence[float],
    afpi_values_7d: Sequence[float],
    afpi_values_30d: Sequence[float],
) -> dict[str, str]:
    """Classify AFPI direction independently for each requested window."""
    return {
        "24h": calculate_afpi_trend(list(afpi_values_24h)),
        "7d": calculate_afpi_trend(list(afpi_values_7d)),
        "30d": calculate_afpi_trend(list(afpi_values_30d)),
    }
