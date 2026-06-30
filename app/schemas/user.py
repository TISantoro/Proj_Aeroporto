from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema para criar um novo usuário"""
    name: str
    email: EmailStr
    login: str
    password: str


class UserUpdate(BaseModel):
    """Schema para atualizar um usuário"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    """Schema para retornar dados de um usuário"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    login: str
    active: bool
    created_at: datetime
    updated_at: datetime
    