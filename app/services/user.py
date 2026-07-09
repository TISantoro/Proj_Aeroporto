from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.auth.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
 
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def can_register_without_auth(self) -> bool:
        """Permite cadastro inicial sem autenticação apenas se não existir usuário cadastrado."""
        return not self.repository.has_any_user()

    def create_user(self, user_data: UserCreate) -> User:
        # Validação: Email já cadastrado
        if self.repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )

        # Validação: Login já cadastrado
        if self.repository.get_by_login(user_data.login):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login já cadastrado"
            )

        # Criar usuário (TODO: Hash da senha aqui seria ideal!)
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            login=user_data.login,
            password=hash_password(user_data.password)
        )

        return self.repository.create(db_user)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return user

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.get_user_by_id(user_id)

        # Validação: Email já cadastrado (excluindo o próprio usuário)
        if user_update.email:
            if self.repository.get_by_email_excluding_id(user_update.email, user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado"
                )
            user.email = user_update.email

        if user_update.name:
            user.name = user_update.name

        if user_update.password:
            user.password = hash_password(user_update.password)

        return self.repository.update(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        self.repository.delete(user)

    def hard_delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        self.repository.hard_delete(user)

    def list_all_users(self) -> list[User]:
        return self.repository.get_all()
