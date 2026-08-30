def calculate_average_fare(fares: list[float]) -> float:
    """
    Calculate the average fare from a collection of fare values.
    """

    if not fares:
        raise ValueError("Fare list must not be empty.")

    if any(fare < 0 for fare in fares):
        raise ValueError("Fare values must not be negative.")

    return sum(fares) / len(fares)

def calculate_afpi(
    current_average_fare: float,
    base_average_fare: float
) -> float:
    """
    Calculate the Airfare Price Index (AFPI).

    AFPI = (Current Average Fare / Base Average Fare) * 100
    """

    if base_average_fare <= 0:
        raise ValueError("Base average fare must be greater than zero.")

    return (current_average_fare / base_average_fare) * 100

def calculate_price_change(
    current_fare: float,
    previous_fare: float
) -> float:
    """
    Calculate the percentage change in airfare.

    Price Change (%) =
    ((Current Fare - Previous Fare) / Previous Fare) * 100
    """

    if previous_fare <= 0:
        raise ValueError("Previous fare must be greater than zero.")

    return ((current_fare - previous_fare) / previous_fare) * 100

def calculate_volatility(fares: list[float]) -> float:
    """
    Calculate the standard deviation of fare values.

    Uses population standard deviation:
        σ = sqrt((1/N) * Σ(Pi - P̄)^2)
    """

    if not fares:
        raise ValueError("Fare list must not be empty.")

    if any(fare < 0 for fare in fares):
        raise ValueError("Fare values must not be negative.")

    average = sum(fares) / len(fares)

    variance = sum((fare - average) ** 2 for fare in fares) / len(fares)

    return variance ** 0.5

def detect_outliers(fares: list[float]) -> list[float]:
    """
    Detect outlier fare values using the IQR method.

    IQR = Q3 - Q1
    Lower Bound = Q1 - 1.5 * IQR
    Upper Bound = Q3 + 1.5 * IQR

    Returns:
        A list containing fare values identified as outliers.
    """
    if not fares:
        raise ValueError("Fare list must not be empty.")

    if any(fare < 0 for fare in fares):
        raise ValueError("Fare values must not be negative.")

    sorted_fares = sorted(fares)

    def percentile(values: list[float], percentile_value: float) -> float:
        position = (len(values) - 1) * percentile_value
        lower = int(position)
        upper = lower + 1

        if upper >= len(values):
            return float(values[lower])

        fraction = position - lower
        return float(
            values[lower] + (values[upper] - values[lower]) * fraction
        )

    q1 = percentile(sorted_fares, 0.25)
    q3 = percentile(sorted_fares, 0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    return [
        fare
        for fare in fares
        if fare < lower_bound or fare > upper_bound
    ]

def calculate_afpi_trend(afpi_values: list[float]) -> str:
    """
    Determine the overall AFPI trend.

    Returns:
        "increasing" if AFPI is trending upward,
        "decreasing" if AFPI is trending downward,
        "stable" if there is no overall change.
    """
    if not afpi_values:
        raise ValueError("AFPI list must not be empty.")

    if len(afpi_values) == 1:
        return "stable"

    if any(value < 0 for value in afpi_values):
        raise ValueError("AFPI values must not be negative.")

    if afpi_values[-1] > afpi_values[0]:
        return "increasing"

    if afpi_values[-1] < afpi_values[0]:
        return "decreasing"

    return "stable"