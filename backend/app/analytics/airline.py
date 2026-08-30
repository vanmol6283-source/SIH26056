from typing import List

from .afpi import calculate_average_fare, calculate_afpi


def calculate_airline_index(
    current_fares: List[float],
    baseline_fares: List[float],
) -> float:
    """
    Calculate the airline-level Airfare Price Index (AFPI).

    Airline AFPI = (Current Average Fare / Baseline Average Fare) * 100
    """

    current_average = calculate_average_fare(current_fares)
    baseline_average = calculate_average_fare(baseline_fares)

    return calculate_afpi(
        current_average,
        baseline_average,
    )