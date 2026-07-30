from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class RunwayStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    all = "all"


class RunwayCreate(BaseModel):
    """Schema para criar uma nova pista"""
    identifier: str = Field(..., min_length=1, description="Identificador único da pista")
    length: float = Field(..., gt=0, description="Comprimento da pista (deve ser maior que zero)")
    surface_type: str = Field(..., min_length=1, description="Tipo de superfície da pista")


class RunwayUpdate(BaseModel):
    """Schema para atualizar dados de uma pista"""
    length: Optional[float] = Field(None, gt=0, description="Comprimento da pista")
    surface_type: Optional[str] = Field(None, min_length=1, description="Tipo de superfície da pista")


class RunwayResponse(BaseModel):
    """Schema para retornar dados completos de uma pista"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    identifier: str
    length: float
    surface_type: str
    active: bool
    occupied: bool
    operation_in_progress: bool
    operation_scheduled: bool
    usage_history: Optional[str]
    created_at: datetime
    updated_at: datetime


class RunwayListResponse(BaseModel):
    """Schema para retornar dados resumidos de uma pista"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    identifier: str
    length: float
    surface_type: str
    active: bool
    occupied: bool
    operation_in_progress: bool
    operation_scheduled: bool
