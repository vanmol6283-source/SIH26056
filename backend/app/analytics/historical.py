"""Historical fare aggregation utilities."""

from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime

from .afpi import calculate_average_fare


def aggregate_historical_fares(
    observations: Iterable[Mapping[str, object]],
    *,
    interval: str = "day",
) -> list[dict[str, object]]:
    """Aggregate fare observations into chronological time buckets.

    Each observation must contain ``fare`` and ``observed_at``. ``observed_at``
    may be a datetime or an ISO-8601 string. Supported intervals are ``hour``
    and ``day``. The result contains average/min/max fare and observation count.
    """
    if interval not in {"hour", "day"}:
        raise ValueError("Interval must be 'hour' or 'day'.")

    buckets: dict[datetime, list[float]] = {}
    for observation in observations:
        if "fare" not in observation or "observed_at" not in observation:
            raise ValueError("Each observation requires fare and observed_at.")

        fare = float(observation["fare"])
        if fare < 0:
            raise ValueError("Fare values must not be negative.")

        observed_at = observation["observed_at"]
        if isinstance(observed_at, datetime):
            timestamp = observed_at
        elif isinstance(observed_at, str):
            try:
                timestamp = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError("observed_at must be a valid ISO-8601 timestamp.") from exc
        else:
            raise ValueError("observed_at must be a datetime or ISO-8601 string.")

        if interval == "hour":
            bucket = timestamp.replace(minute=0, second=0, microsecond=0)
        else:
            bucket = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        buckets.setdefault(bucket, []).append(fare)

    result: list[dict[str, object]] = []
    for bucket in sorted(buckets):
        fares = buckets[bucket]
        result.append({
            "observed_at": bucket,
            "average_fare": calculate_average_fare(fares),
            "min_fare": min(fares),
            "max_fare": max(fares),
            "observation_count": len(fares),
        })
    return result


def extract_historical_fares(
    observations: Sequence[Mapping[str, object]],
) -> list[float]:
    """Return historical fares in chronological observation order."""
    parsed: list[tuple[datetime, float]] = []
    for observation in observations:
        if "fare" not in observation or "observed_at" not in observation:
            raise ValueError("Each observation requires fare and observed_at.")
        fare = float(observation["fare"])
        if fare < 0:
            raise ValueError("Fare values must not be negative.")
        timestamp = observation["observed_at"]
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if not isinstance(timestamp, datetime):
            raise ValueError("observed_at must be a datetime or ISO-8601 string.")
        parsed.append((timestamp, fare))
    parsed.sort(key=lambda item: item[0])
    return [fare for _, fare in parsed]
