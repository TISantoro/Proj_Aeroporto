from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from datetime import datetime
from app.database.db import Base


class Runway(Base):
    """Modelo de pista do sistema"""
    __tablename__ = "runways"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True, nullable=False)
    length = Column(Float, nullable=False)
    surface_type = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    occupied = Column(Boolean, default=False)
    operation_in_progress = Column(Boolean, default=False)
    operation_scheduled = Column(Boolean, default=False)
    usage_history = Column(String, nullable=True, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
