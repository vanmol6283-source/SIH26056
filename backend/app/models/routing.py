"""
Routes table — a directed origin -> destination pair between two airports.
Owned by Prantik (DBMS Lead).
"""
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Route(Base):
    __tablename__ = "routes"
    __table_args__ = (
        UniqueConstraint("origin_airport_id", "destination_airport_id", name="uq_route_pair"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    origin_airport_id: Mapped[int] = mapped_column(
        ForeignKey("airports.id", name="fk_routes_origin"), nullable=False, index=True
    )
    destination_airport_id: Mapped[int] = mapped_column(
        ForeignKey("airports.id", name="fk_routes_destination"), nullable=False, index=True
    )

    origin_airport: Mapped["Airport"] = relationship(
        back_populates="routes_originating", foreign_keys=[origin_airport_id]
    )
    destination_airport: Mapped["Airport"] = relationship(
        back_populates="routes_arriving", foreign_keys=[destination_airport_id]
    )
    flights: Mapped[list["Flight"]] = relationship(back_populates="route")
    index_values: Mapped[list["IndexValue"]] = relationship(back_populates="route")

    def __repr__(self) -> str:
        return f"<Route {self.origin_airport_id}->{self.destination_airport_id}>"
