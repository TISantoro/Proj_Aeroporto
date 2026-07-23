from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database.db import Base


class Aircraft(Base):
    """Modelo de avião do sistema"""
    __tablename__ = "aircrafts"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True, nullable=False)
    model = Column(String, nullable=False)
    airline = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
