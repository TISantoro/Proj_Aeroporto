from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class AircraftCreate(BaseModel):
    """Schema para criar um novo avião"""
    identifier: str = Field(..., min_length=1, description="Identificador único do avião")
    model: str = Field(..., min_length=1, description="Modelo da aeronave")
    airline: str = Field(..., min_length=1, description="Companhia aérea")
    capacity: int = Field(..., gt=0, description="Capacidade de passageiros (deve ser maior que zero)")


class AircraftUpdate(BaseModel):
    """Schema para atualizar dados de um avião (exceto identificador)"""
    model: Optional[str] = Field(None, min_length=1, description="Modelo da aeronave")
    airline: Optional[str] = Field(None, min_length=1, description="Companhia aérea")
    capacity: Optional[int] = Field(None, gt=0, description="Capacidade de passageiros")
    active: Optional[bool] = Field(None, description="Status do avião")


class AircraftResponse(BaseModel):
    """Schema para retornar dados de um avião"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    identifier: str
    model: str
    airline: str
    capacity: int
    active: bool
    created_at: datetime
    updated_at: datetime


class AircraftListResponse(BaseModel):
    """Schema para retornar dados resumidos de um avião em listagem"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    identifier: str
    model: str
    airline: str
    capacity: int
    active: bool
