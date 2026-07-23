from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database.db import get_db
from app.models.user import User
from app.services.aircraft import AircraftService
from app.schemas.aircraft import AircraftCreate, AircraftResponse, AircraftUpdate, AircraftListResponse

router = APIRouter(prefix="/aircrafts", tags=["aircrafts"])


def get_aircraft_service(db: Session = Depends(get_db)) -> AircraftService:
    """Dependência para injetar o serviço de aviões"""
    return AircraftService(db)


@router.post("/", response_model=AircraftResponse, status_code=status.HTTP_201_CREATED)
def create_aircraft(
    aircraft: AircraftCreate,
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(get_current_user),
):
    """Apenas usuários autenticados podem cadastrar aviões."""
    return service.create_aircraft(aircraft)


@router.get("/", response_model=list[AircraftListResponse])
def list_aircrafts(
    active_only: bool = Query(True, description="Filtrar apenas aviões ativos (padrão: True)"),
    identifier: str | None = Query(None, description="Buscar por identificador (busca parcial)"),
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(get_current_user),
):
    """
    Filtros disponíveis:
    - active_only: Exibe aviões ativos por padrão (pode ser alterado para False)
    - identifier: Permite busca pelo identificador (busca parcial)
    """
    return service.list_aircrafts(active_only=active_only, identifier_filter=identifier)


@router.get("/{aircraft_id}", response_model=AircraftResponse)
def get_aircraft(
    aircraft_id: int,
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(get_current_user),
):
    """
    Informações exibidas:
    - Todos os campos do cadastro
    - Status atual do avião
    - TODO: Se avião está associado a operação em andamento
    - TODO: Histórico básico de operações
    """
    return service.get_aircraft_by_id(aircraft_id)


@router.put("/{aircraft_id}", response_model=AircraftResponse)
def update_aircraft(
    aircraft_id: int,
    aircraft_update: AircraftUpdate,
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(get_current_user),
):
    """
    Validações:
    - Não permite alteração do identificador único
    - Permite alteração de modelo, companhia aérea e capacidade
    - TODO: Não permite alterações que impactem operação em andamento
    - TODO: Registra a alteração no log de auditoria
    """
    return service.update_aircraft(aircraft_id, aircraft_update)


@router.patch("/{aircraft_id}/deactivate", response_model=AircraftResponse)
def deactivate_aircraft(
    aircraft_id: int,
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(get_current_user),
):
    """
    Validações:
    - Não permite inativação se avião está em operação
    - Aviões inativos não podem ser usados em novas operações
    - Histórico do avião é preservado
    - TODO: Registra a inativação no log de auditoria
    """
    return service.deactivate_aircraft(aircraft_id)


@router.patch("/{aircraft_id}/activate", response_model=AircraftResponse)
def activate_aircraft(
    aircraft_id: int,
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(get_current_user),
):
    """Ativa um avião inativo"""
    return service.activate_aircraft(aircraft_id)


@router.delete("/{aircraft_id}/hard", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete_aircraft(
    aircraft_id: int,
    service: AircraftService = Depends(get_aircraft_service),
    current_user: User = Depends(get_current_user),
):
    """Remove permanentemente um avião do sistema (uso administrativo)"""
    service.hard_delete_aircraft(aircraft_id)
