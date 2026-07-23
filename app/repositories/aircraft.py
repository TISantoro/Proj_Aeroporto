from sqlalchemy.orm import Session
from app.models.aircraft import Aircraft


class AircraftRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, aircraft: Aircraft) -> Aircraft:
        """Cria um novo avião no banco"""
        self.db.add(aircraft)
        self.db.commit()
        self.db.refresh(aircraft)
        return aircraft

    def get_by_id(self, aircraft_id: int) -> Aircraft | None:
        """Busca um avião pelo ID"""
        return self.db.query(Aircraft).filter(Aircraft.id == aircraft_id).first()

    def get_by_identifier(self, identifier: str) -> Aircraft | None:
        """Busca um avião pelo identificador único"""
        return self.db.query(Aircraft).filter(Aircraft.identifier == identifier).first()

    def get_by_identifier_excluding_id(self, identifier: str, aircraft_id: int) -> Aircraft | None:
        """Busca um avião pelo identificador, excluindo um ID específico (para atualizações)"""
        return self.db.query(Aircraft).filter(
            Aircraft.identifier == identifier, Aircraft.id != aircraft_id
        ).first()

    def get_all(self, active_only: bool = True, identifier_filter: str | None = None) -> list[Aircraft]:
        """Retorna todos os aviões com opções de filtro
        
        Args:
            active_only: Se True, retorna apenas aviões ativos
            identifier_filter: Filtro opcional por identificador (busca parcial)
        """
        query = self.db.query(Aircraft)
        
        if active_only:
            query = query.filter(Aircraft.active == True)
        
        if identifier_filter:
            query = query.filter(Aircraft.identifier.ilike(f"%{identifier_filter}%"))
        
        return query.all()

    def get_all_no_filters(self) -> list[Aircraft]:
        """Retorna todos os aviões sem filtros"""
        return self.db.query(Aircraft).all()

    def update(self, aircraft: Aircraft) -> Aircraft:
        """Atualiza um avião existente"""
        self.db.commit()
        self.db.refresh(aircraft)
        return aircraft

    def deactivate(self, aircraft: Aircraft) -> Aircraft:
        """Inativa um avião (soft delete)"""
        aircraft.active = False
        self.db.commit()
        self.db.refresh(aircraft)
        return aircraft

    def hard_delete(self, aircraft: Aircraft) -> None:
        """Remove permanentemente um avião do banco (delete físico)"""
        self.db.delete(aircraft)
        self.db.commit()

    def has_any_aircraft(self) -> bool:
        """Retorna True se existe ao menos um avião cadastrado"""
        return self.db.query(Aircraft).first() is not None
