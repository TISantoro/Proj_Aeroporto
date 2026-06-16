from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    US-01: Cadastrar usuário
    
    Cria um novo usuário no sistema com os dados fornecidos.
    """
    # Verifica se o email já existe
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Verifica se o login já existe
    existing_login = db.query(User).filter(User.login == user.login).first()
    if existing_login:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login já cadastrado"
        )
    
    # Cria o novo usuário
    db_user = User(
        name=user.name,
        email=user.email,
        login=user.login,
        password=user.password  # TODO: Hash a senha antes de salvar!
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retorna os dados de um usuário específico"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """US-02: Listar usuários"""
    users = db.query(User).filter(User.active == True).all()
    return users
