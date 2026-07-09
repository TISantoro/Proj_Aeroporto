from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user, get_current_user_optional
from app.database.db import get_db
from app.models.user import User
from app.services.user import UserService
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependência para injetar o serviço de usuários"""
    return UserService(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user_optional),
):
    """Cria um novo usuário no sistema com os dados fornecidos."""
    if not service.can_register_without_auth() and current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária para cadastrar novos usuários",
        )
    return service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    """Retorna os dados de um usuário específico"""
    return service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    """Atualiza os dados de um usuário existente"""
    return service.update_user(user_id, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    """Remove um usuário do sistema (soft delete)"""
    service.delete_user(user_id)


@router.delete("/{user_id}/hard", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    """Remove permanentemente um usuário do sistema."""
    service.hard_delete_user(user_id)


@router.get("/", response_model=list[UserResponse])
def list_users(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    """Retorna a lista de todos os usuários"""
    return service.list_all_users()
