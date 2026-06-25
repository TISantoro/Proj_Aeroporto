from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        """Cria um novo usuário no banco"""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        """Busca um usuário pelo ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        """Busca um usuário pelo email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_login(self, login: str) -> User | None:
        """Busca um usuário pelo login"""
        return self.db.query(User).filter(User.login == login).first()

    def get_by_email_excluding_id(self, email: str, user_id: int) -> User | None:
        """Busca um usuário pelo email, excluindo um ID específico (para atualizações)"""
        return self.db.query(User).filter(
            User.email == email, User.id != user_id
        ).first()

    def get_all(self) -> list[User]:
        """Retorna todos os usuários"""
        return self.db.query(User).all()

    def update(self, user: User) -> User:
        """Atualiza um usuário existente"""
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Remove um usuário do banco (soft delete - apenas marca como inativo)"""
        user.active = False
        self.db.commit()

    def hard_delete(self, user: User) -> None:
        """Remove permanentemente um usuário do banco (delete físico)"""
        self.db.delete(user)
        self.db.commit()
