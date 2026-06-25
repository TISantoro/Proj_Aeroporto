from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.user import UserService
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependência para injetar o serviço de usuários"""
    return UserService(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    """Cria um novo usuário no sistema com os dados fornecidos."""
    return service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    """Retorna os dados de um usuário específico"""
    return service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    """Atualiza os dados de um usuário existente"""
    return service.update_user(user_id, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    """Remove um usuário do sistema (soft delete)"""
    service.delete_user(user_id)


@router.get("/", response_model=list[UserResponse])
def list_users(service: UserService = Depends(get_user_service)):
    """Retorna a lista de todos os usuários"""
    return service.list_all_users()
