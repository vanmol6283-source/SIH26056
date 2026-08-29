"""
Flights and price_observations tables.
Owned by Prantik (DBMS Lead) — populated by Abhay's ingestion pipeline.
"""
from datetime import date, datetime, time

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Flight(Base):
    __tablename__ = "flights"
    __table_args__ = (
        UniqueConstraint(
            "route_id", "airline_id", "flight_number", "departure_time",
            name="uq_flight_identity",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(
        ForeignKey("routes.id", name="fk_flights_route"), nullable=False, index=True
    )
    airline_id: Mapped[int] = mapped_column(
        ForeignKey("airlines.id", name="fk_flights_airline"), nullable=False, index=True
    )
    flight_number: Mapped[str] = mapped_column(String(10), nullable=False)
    departure_time: Mapped[time] = mapped_column(nullable=False)
    arrival_time: Mapped[time] = mapped_column(nullable=False)
    cabin_class: Mapped[str] = mapped_column(String(20), nullable=False, default="economy")
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # provider name, e.g. "amadeus"

    route: Mapped["Route"] = relationship(back_populates="flights")
    airline: Mapped["Airline"] = relationship(back_populates="flights")
    price_observations: Mapped[list["PriceObservation"]] = relationship(back_populates="flight")

    def __repr__(self) -> str:
        return f"<Flight {self.flight_number}>"


class PriceObservation(Base):
    __tablename__ = "price_observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_id: Mapped[int] = mapped_column(
        ForeignKey("flights.id", name="fk_price_observations_flight"), nullable=False, index=True
    )
    observed_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    travel_date: Mapped[date] = mapped_column(nullable=False, index=True)
    base_fare: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    taxes: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total_fare: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="valid")
    # status values e.g. "valid" | "duplicate" | "flagged" — used by Abhay's
    # duplicate-detection / validation step before Guntaas's analytics reads it

    flight: Mapped["Flight"] = relationship(back_populates="price_observations")

    def __repr__(self) -> str:
        return f"<PriceObservation flight={self.flight_id} total={self.total_fare}>"
