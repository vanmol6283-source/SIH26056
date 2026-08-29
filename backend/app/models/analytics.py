"""
index_values table — stores calculated AFPI results.
Owned by Prantik (DBMS Lead) — written to by Guntaas's analytics engine.

A row can represent a route-level index, an airline-level index, or both
together (route + airline combined), depending on which of route_id /
airline_id is populated. At least one of the two must be set — enforced at
the application layer by Guntaas's calculate_route_index() /
calculate_airline_index() functions, since a DB-level XOR constraint would
block the combined route+airline case.
"""
from datetime import date, datetime

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class IndexValue(Base):
    __tablename__ = "index_values"

    id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int | None] = mapped_column(
        ForeignKey("routes.id", name="fk_index_values_route"), nullable=True, index=True
    )
    airline_id: Mapped[int | None] = mapped_column(
        ForeignKey("airlines.id", name="fk_index_values_airline"), nullable=True, index=True
    )
    calculated_at: Mapped[datetime] = mapped_column(nullable=False, index=True)
    travel_date: Mapped[date] = mapped_column(nullable=False)
    index_value: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    baseline_value: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    current_average_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    baseline_average_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    route: Mapped["Route"] = relationship(back_populates="index_values")
    airline: Mapped["Airline"] = relationship(back_populates="index_values")

    def __repr__(self) -> str:
        return f"<IndexValue route={self.route_id} airline={self.airline_id} value={self.index_value}>"
