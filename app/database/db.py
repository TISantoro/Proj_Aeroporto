from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Banco de dados SQLite para começar (simples)
DATABASE_URL = "sqlite:///./aeroporto.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Necessário para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependência para obter a sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
