from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.runway import Runway
from app.repositories.runway import RunwayRepository
from app.schemas.runway import RunwayCreate, RunwayUpdate, RunwayStatus


class RunwayService:

    def __init__(self, db: Session):
        self.repository = RunwayRepository(db)

    def create_runway(self, runway_data: RunwayCreate) -> Runway:
        """Validações de criação de pista."""
        if self.repository.get_by_identifier(runway_data.identifier):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Identificador de pista já cadastrado"
            )

        if runway_data.length <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Comprimento da pista deve ser maior que zero"
            )

        runway = Runway(
            identifier=runway_data.identifier,
            length=runway_data.length,
            surface_type=runway_data.surface_type,
            active=True,
            occupied=False,
            operation_in_progress=False,
            operation_scheduled=False,
            usage_history=""
        )

        return self.repository.create(runway)

    def get_runway_by_id(self, runway_id: int) -> Runway:
        runway = self.repository.get_by_id(runway_id)
        if not runway:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pista não encontrada"
            )
        return runway

    def list_runways(self, status: RunwayStatus = RunwayStatus.active) -> list[Runway]:
        return self.repository.get_all(status=status)

    def update_runway(self, runway_id: int, runway_update: RunwayUpdate) -> Runway:
        runway = self.get_runway_by_id(runway_id)

        if runway.operation_in_progress or runway.operation_scheduled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível editar pista com operação em andamento ou agendada"
            )

        if runway_update.length is not None:
            if runway_update.length <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Comprimento da pista deve ser maior que zero"
                )
            runway.length = runway_update.length

        if runway_update.surface_type is not None:
            runway.surface_type = runway_update.surface_type

        return self.repository.update(runway)

    def deactivate_runway(self, runway_id: int) -> Runway:
        runway = self.get_runway_by_id(runway_id)

        if not runway.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pista já está inativa"
            )

        if runway.operation_in_progress or runway.operation_scheduled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível inativar pista com operação em andamento ou agendada"
            )

        return self.repository.deactivate(runway)

    def activate_runway(self, runway_id: int) -> Runway:
        runway = self.get_runway_by_id(runway_id)

        if runway.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pista já está ativa"
            )

        runway.active = True
        return self.repository.update(runway)

    def hard_delete_runway(self, runway_id: int) -> None:
        runway = self.get_runway_by_id(runway_id)
        self.repository.hard_delete(runway)
