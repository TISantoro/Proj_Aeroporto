from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.jwt import create_access_token
from app.auth.security import verify_password
from app.database.db import get_db
from app.repositories.user import UserRepository
from app.schemas.user import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = UserRepository(db).get_by_login(payload.login)
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    if not user.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário inativo")

    access_token = create_access_token({"sub": str(user.id), "login": user.login})
    return {"access_token": access_token, "token_type": "bearer"}
