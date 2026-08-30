from typing import List

from .afpi import calculate_average_fare, calculate_afpi


def calculate_route_index(
    current_fares: List[float],
    baseline_fares: List[float],
) -> float:
    """
    Calculate the route-level Airfare Price Index (AFPI).

    Route AFPI = (Current Average Fare / Base Average Fare) * 100

    Args:
        current_fares: Valid current fare observations for the route.
        baseline_fares: Valid baseline fare observations for the route.

    Returns:
        Route-level AFPI as a percentage.

    Raises:
        ValueError: If either fare list is empty or contains
                    invalid negative values.
    """

    current_average = calculate_average_fare(current_fares)
    baseline_average = calculate_average_fare(baseline_fares)

    return calculate_afpi(
        current_average,
        baseline_average,
    )