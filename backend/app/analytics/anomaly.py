"""Lightweight statistical anomaly detection for airfare observations."""

from collections.abc import Sequence

from .afpi import calculate_volatility, detect_outliers


def detect_anomalies(
    fares: Sequence[float],
    *,
    z_threshold: float = 3.0,
) -> list[float]:
    """Detect unusual fares using a robust IQR-first statistical rule.

    IQR outliers are always considered anomalies. When volatility is non-zero,
    observations with an absolute z-score above ``z_threshold`` are also
    considered anomalies. This keeps anomaly detection dependency-free while
    leaving room for a future ML detector.
    """
    values = list(fares)
    if not values:
        raise ValueError("Fare list must not be empty.")
    if any(value < 0 for value in values):
        raise ValueError("Fare values must not be negative.")
    if z_threshold <= 0:
        raise ValueError("z_threshold must be greater than zero.")

    anomalies = set(detect_outliers(values))
    volatility = calculate_volatility(values)
    if volatility > 0:
        mean = sum(values) / len(values)
        anomalies.update(
            value for value in values
            if abs((value - mean) / volatility) > z_threshold
        )
    return [value for value in values if value in anomalies]


def calculate_anomaly_summary(fares: Sequence[float]) -> dict[str, object]:
    """Return anomaly observations and a concise summary for API consumers."""
    values = list(fares)
    anomalies = detect_anomalies(values)
    return {
        "anomalies": anomalies,
        "anomaly_count": len(anomalies),
        "has_anomalies": bool(anomalies),
        "volatility": calculate_volatility(values),
    }
