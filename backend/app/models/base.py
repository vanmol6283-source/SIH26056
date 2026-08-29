"""
Shared SQLAlchemy declarative base.
All model files import Base from here so Alembic can discover every table
through a single metadata object.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
