from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database.db import Base


class User(Base):
    """Modelo de usuário do sistema"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
