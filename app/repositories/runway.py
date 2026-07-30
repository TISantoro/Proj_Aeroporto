from sqlalchemy.orm import Session
from app.models.runway import Runway
from app.schemas.runway import RunwayStatus


class RunwayRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, runway: Runway) -> Runway:
        """Cria uma nova pista no banco"""
        self.db.add(runway)
        self.db.commit()
        self.db.refresh(runway)
        return runway

    def get_by_id(self, runway_id: int) -> Runway | None:
        """Busca uma pista pelo ID"""
        return self.db.query(Runway).filter(Runway.id == runway_id).first()

    def get_by_identifier(self, identifier: str) -> Runway | None:
        """Busca uma pista pelo identificador único"""
        return self.db.query(Runway).filter(Runway.identifier == identifier).first()

    def get_by_identifier_excluding_id(self, identifier: str, runway_id: int) -> Runway | None:
        """Busca uma pista pelo identificador excluindo um ID específico"""
        return self.db.query(Runway).filter(
            Runway.identifier == identifier,
            Runway.id != runway_id
        ).first()

    def get_all(self, status: RunwayStatus = RunwayStatus.active) -> list[Runway]:
        """Retorna todas as pistas com filtro de status."""
        query = self.db.query(Runway)

        if status == RunwayStatus.active:
            query = query.filter(Runway.active == True)
        elif status == RunwayStatus.inactive:
            query = query.filter(Runway.active == False)

        return query.all()

    def update(self, runway: Runway) -> Runway:
        """Atualiza uma pista existente"""
        self.db.commit()
        self.db.refresh(runway)
        return runway

    def deactivate(self, runway: Runway) -> Runway:
        """Inativa uma pista (soft delete)"""
        runway.active = False
        self.db.commit()
        self.db.refresh(runway)
        return runway

    def hard_delete(self, runway: Runway) -> None:
        """Remove permanentemente uma pista do banco"""
        self.db.delete(runway)
        self.db.commit()

    def has_any_runway(self) -> bool:
        """Retorna True se existir ao menos uma pista cadastrada"""
        return self.db.query(Runway).first() is not None
