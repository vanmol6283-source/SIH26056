from collections.abc import Sequence

from .afpi import calculate_average_fare, calculate_volatility, detect_outliers
from .airline import calculate_airline_index
from .anomaly import calculate_anomaly_summary
from .route import calculate_route_index
from .time_based import calculate_price_changes
from .trends import calculate_fare_trends


def calculate_airfare_analysis(
    current_airline_fares: list[float],
    baseline_airline_fares: list[float],
    current_route_fares: list[float],
    baseline_route_fares: list[float],
    current_fare: float,
    historical_fare_24h: float,
    historical_fare_7d: float,
    historical_fare_30d: float,
    historical_fares: Sequence[float] | None = None,
) -> dict[str, object]:
    """Calculate the complete snapshot airfare analytics payload.

    ``historical_fares`` is optional for backwards compatibility. When supplied,
    it adds historical statistics and anomaly analysis without changing the
    existing AFPI/price-change contract.
    """
    airline_afpi = calculate_airline_index(
        current_airline_fares, baseline_airline_fares
    )
    route_afpi = calculate_route_index(current_route_fares, baseline_route_fares)
    price_changes = calculate_price_changes(
        current_fare=current_fare,
        historical_fare_24h=historical_fare_24h,
        historical_fare_7d=historical_fare_7d,
        historical_fare_30d=historical_fare_30d,
    )
    volatility = calculate_volatility(current_airline_fares)
    outliers = detect_outliers(current_airline_fares)

    result: dict[str, object] = {
        "airline_afpi": airline_afpi,
        "route_afpi": route_afpi,
        "price_changes": price_changes,
        "trends": calculate_fare_trends(
            current_fare,
            historical_fare_24h,
            historical_fare_7d,
            historical_fare_30d,
        ),
        "volatility": volatility,
        "outliers": outliers,
        "anomaly_summary": calculate_anomaly_summary(current_airline_fares),
        "average_fare": calculate_average_fare(current_airline_fares),
    }

    if historical_fares is not None:
        historical_values = list(historical_fares)
        if not historical_values:
            raise ValueError("historical_fares must not be empty when provided.")
        historical_average = calculate_average_fare(historical_values)
        result["historical_fare"] = historical_average
        result["historical_volatility"] = calculate_volatility(historical_values)
        result["historical_outliers"] = detect_outliers(historical_values)

    return result
