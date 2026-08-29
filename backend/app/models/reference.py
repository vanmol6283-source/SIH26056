"""
Reference / lookup tables: airports, airlines, data_sources.
Owned by Prantik (DBMS Lead).
"""
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Airport(Base):
    __tablename__ = "airports"

    id: Mapped[int] = mapped_column(primary_key=True)
    iata_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

    routes_originating: Mapped[list["Route"]] = relationship(
        back_populates="origin_airport",
        foreign_keys="Route.origin_airport_id",
    )
    routes_arriving: Mapped[list["Route"]] = relationship(
        back_populates="destination_airport",
        foreign_keys="Route.destination_airport_id",
    )

    def __repr__(self) -> str:
        return f"<Airport {self.iata_code}>"


class Airline(Base):
    __tablename__ = "airlines"

    id: Mapped[int] = mapped_column(primary_key=True)
    iata_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    flights: Mapped[list["Flight"]] = relationship(back_populates="airline")
    index_values: Mapped[list["IndexValue"]] = relationship(back_populates="airline")

    def __repr__(self) -> str:
        return f"<Airline {self.iata_code}>"


class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    provider_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. "amadeus", "mock"
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    last_successful_fetch: Mapped[datetime | None] = mapped_column(nullable=True)
    last_failed_fetch: Mapped[datetime | None] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<DataSource {self.name}>"
