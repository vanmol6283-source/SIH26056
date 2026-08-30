"""Route and airline ranking utilities for the AFPI analytics engine."""

from collections.abc import Mapping, Sequence

from .afpi import calculate_afpi, calculate_average_fare


def _rank_indices(
    current_fares_by_entity: Mapping[str, Sequence[float]],
    baseline_fares_by_entity: Mapping[str, Sequence[float]],
) -> list[dict[str, object]]:
    if not current_fares_by_entity:
        raise ValueError("At least one entity is required.")

    missing = set(current_fares_by_entity) - set(baseline_fares_by_entity)
    if missing:
        raise ValueError(f"Missing baseline fares for: {sorted(missing)}")

    ranked: list[dict[str, object]] = []
    for entity, current_fares in current_fares_by_entity.items():
        baseline_fares = baseline_fares_by_entity[entity]
        current_average = calculate_average_fare(list(current_fares))
        baseline_average = calculate_average_fare(list(baseline_fares))
        afpi = calculate_afpi(current_average, baseline_average)
        ranked.append({
            "entity": entity,
            "afpi": afpi,
            "average_fare": current_average,
        })

    ranked.sort(key=lambda item: (-float(item["afpi"]), str(item["entity"])))
    for rank, item in enumerate(ranked, start=1):
        item["rank"] = rank
    return ranked


def calculate_route_ranking(
    current_fares_by_route: Mapping[str, Sequence[float]],
    baseline_fares_by_route: Mapping[str, Sequence[float]],
) -> list[dict[str, object]]:
    """Rank routes by AFPI, highest AFPI first."""
    return _rank_indices(current_fares_by_route, baseline_fares_by_route)


def calculate_airline_ranking(
    current_fares_by_airline: Mapping[str, Sequence[float]],
    baseline_fares_by_airline: Mapping[str, Sequence[float]],
) -> list[dict[str, object]]:
    """Rank airlines by AFPI, highest AFPI first."""
    return _rank_indices(current_fares_by_airline, baseline_fares_by_airline)
