def calculate_price_change_24h(
    current_fare: float,
    historical_fare: float,
) -> float:
    if current_fare < 0:
        raise ValueError("Current fare cannot be negative")

    if historical_fare <= 0:
        raise ValueError("Historical fare must be greater than zero")

    return ((current_fare - historical_fare) / historical_fare) * 100

def calculate_price_change_7d(
    current_fare: float,
    historical_fare: float,
) -> float:
    if current_fare < 0:
        raise ValueError("Current fare cannot be negative")

    if historical_fare <= 0:
        raise ValueError("Historical fare must be greater than zero")

    return ((current_fare - historical_fare) / historical_fare) * 100


def calculate_price_change_30d(
    current_fare: float,
    historical_fare: float,
) -> float:
    if current_fare < 0:
        raise ValueError("Current fare cannot be negative")

    if historical_fare <= 0:
        raise ValueError("Historical fare must be greater than zero")

    return ((current_fare - historical_fare) / historical_fare) * 100

def calculate_price_change(
    current_fare: float,
    historical_fare: float,
    window: str,
) -> float:
    """Calculate fare change for a specified time window."""

    if window == "24h":
        return calculate_price_change_24h(
            current_fare,
            historical_fare,
        )

    if window == "7d":
        return calculate_price_change_7d(
            current_fare,
            historical_fare,
        )

    if window == "30d":
        return calculate_price_change_30d(
            current_fare,
            historical_fare,
        )

    raise ValueError("Unsupported time window")

def calculate_price_changes(
    current_fare: float,
    historical_fare_24h: float,
    historical_fare_7d: float,
    historical_fare_30d: float,
) -> dict[str, float]:
    """Calculate airfare percentage changes across multiple time windows."""

    return {
        "24h": calculate_price_change_24h(
            current_fare,
            historical_fare_24h,
        ),
        "7d": calculate_price_change_7d(
            current_fare,
            historical_fare_7d,
        ),
        "30d": calculate_price_change_30d(
            current_fare,
            historical_fare_30d,
        ),
    }