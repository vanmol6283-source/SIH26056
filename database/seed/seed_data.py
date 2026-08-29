"""
Seed script — inserts small sample dataset so the team can test without
waiting on a live flight API connection.

Run from the backend/ folder (so app/ is importable) with:
    python ../database/seed/seed_data.py
"""
import os
import sys
from datetime import date, datetime, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "backend", ".env"))

from app.models import Airport, Airline, DataSource, Route, Flight, PriceObservation, IndexValue

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set — copy backend/.env.example to backend/.env first")

engine = create_engine(DATABASE_URL)

with Session(engine) as session:
    # Airports
    del_ = Airport(iata_code="DEL", name="Indira Gandhi International", city="Delhi", country="India")
    bom = Airport(iata_code="BOM", name="Chhatrapati Shivaji Maharaj International", city="Mumbai", country="India")
    session.add_all([del_, bom])
    session.flush()

    # Airlines
    ai = Airline(iata_code="AI", name="Air India")
    six_e = Airline(iata_code="6E", name="IndiGo")
    session.add_all([ai, six_e])
    session.flush()

    # Data source
    mock_source = DataSource(name="mock_provider", provider_type="mock", status="active")
    session.add(mock_source)
    session.flush()

    # Route
    route = Route(origin_airport_id=del_.id, destination_airport_id=bom.id)
    session.add(route)
    session.flush()

    # Flight
    flight = Flight(
        route_id=route.id,
        airline_id=six_e.id,
        flight_number="6E123",
        departure_time=time(6, 30),
        arrival_time=time(8, 45),
        cabin_class="economy",
        source="mock",
    )
    session.add(flight)
    session.flush()

    # Price observations
    obs1 = PriceObservation(
        flight_id=flight.id,
        observed_at=datetime(2026, 8, 20, 9, 0),
        travel_date=date(2026, 9, 15),
        base_fare=4200.00,
        taxes=300.00,
        total_fare=4500.00,
        currency="INR",
        source="mock",
        status="valid",
    )
    obs2 = PriceObservation(
        flight_id=flight.id,
        observed_at=datetime(2026, 8, 21, 9, 0),
        travel_date=date(2026, 9, 15),
        base_fare=5100.00,
        taxes=300.00,
        total_fare=5400.00,
        currency="INR",
        source="mock",
        status="valid",
    )
    session.add_all([obs1, obs2])
    session.flush()

    # Index value (sample AFPI = 120, matching the doc's worked example)
    index_val = IndexValue(
        route_id=route.id,
        airline_id=None,
        calculated_at=datetime(2026, 8, 21, 10, 0),
        travel_date=date(2026, 9, 15),
        index_value=120.00,
        baseline_value=100.00,
        current_average_price=5400.00,
        baseline_average_price=4500.00,
    )
    session.add(index_val)

    session.commit()
    print("Seed data inserted successfully.")
