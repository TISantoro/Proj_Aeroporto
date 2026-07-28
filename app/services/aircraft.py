from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.aircraft import Aircraft
from app.repositories.aircraft import AircraftRepository
from app.schemas.aircraft import AircraftCreate, AircraftUpdate


class AircraftService:
 
    def __init__(self, db: Session):
        self.repository = AircraftRepository(db)

    def create_aircraft(self, aircraft_data: AircraftCreate) -> Aircraft:
        """Validações:
        - Identificador é obrigatório (já garantido pelo schema)
        - Identificador deve ser único
        - Modelo é obrigatório (já garantido pelo schema)
        - Companhia aérea é obrigatória (já garantido pelo schema)
        - Capacidade deve ser maior que zero (já garantido pelo schema)
        - Avião é criado como Ativo por padrão
        """
        # Validação: Identificador já cadastrado
        if self.repository.get_by_identifier(aircraft_data.identifier):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Identificador de avião já cadastrado"
            )

        # Criar avião (active=True por padrão no modelo)
        db_aircraft = Aircraft(
            identifier=aircraft_data.identifier,
            model=aircraft_data.model,
            airline=aircraft_data.airline,
            capacity=aircraft_data.capacity,
            active=True
        )

        return self.repository.create(db_aircraft)

    def get_aircraft_by_id(self, aircraft_id: int) -> Aircraft:
        """US-06: Obtém os detalhes completos de um avião"""
        aircraft = self.repository.get_by_id(aircraft_id)
        if not aircraft:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Avião não encontrado"
            )
        return aircraft

    def list_aircrafts(
        self, 
        active_only: bool = True, 
        identifier_filter: str | None = None
    ) -> list[Aircraft]:
        """Filtros:
        - active_only: Se True, exibe apenas aviões ativos (padrão)
        - identifier_filter: Permite busca pelo identificador
        """
        return self.repository.get_all(active_only=active_only, identifier_filter=identifier_filter)

    def update_aircraft(self, aircraft_id: int, aircraft_update: AircraftUpdate) -> Aircraft:
        """Validações:
        - Não permite alteração do identificador único
        - Permite alteração de modelo, companhia aérea e capacidade
        - TODO: Validar se avião está em operação
        """
        aircraft = self.get_aircraft_by_id(aircraft_id)

        # Não permitir alteração do identificador
        # (o identificador é único e não deve ser alterado)

        if aircraft_update.model is not None:
            aircraft.model = aircraft_update.model

        if aircraft_update.airline is not None:
            aircraft.airline = aircraft_update.airline

        if aircraft_update.capacity is not None:
            if aircraft_update.capacity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Capacidade deve ser maior que zero"
                )
            aircraft.capacity = aircraft_update.capacity

        # Se status foi enviado, permitir alteração apenas se não estiver em operação
        if aircraft_update.active is not None:
            aircraft.active = aircraft_update.active

        return self.repository.update(aircraft)

    def deactivate_aircraft(self, aircraft_id: int) -> Aircraft:
        """Validações:
        - Não permitir inativação se o avião estiver em operação
        - TODO: Validar se avião está em operação
        """
        aircraft = self.get_aircraft_by_id(aircraft_id)

        if not aircraft.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Avião já está inativo"
            )

        return self.repository.deactivate(aircraft)

    def activate_aircraft(self, aircraft_id: int) -> Aircraft:
        """Ativa um avião inativo"""
        aircraft = self.get_aircraft_by_id(aircraft_id)

        if aircraft.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Avião já está ativo"
            )

        aircraft.active = True
        return self.repository.update(aircraft)

    def hard_delete_aircraft(self, aircraft_id: int) -> None:
        """Remove permanentemente um avião do sistema (uso administrativo)"""
        aircraft = self.get_aircraft_by_id(aircraft_id)
        self.repository.hard_delete(aircraft)
