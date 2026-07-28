from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database.db import get_db
from app.models.user import User
from app.schemas.runway import RunwayCreate, RunwayResponse, RunwayUpdate, RunwayListResponse, RunwayStatus
from app.services.runway import RunwayService

router = APIRouter(prefix="/runways", tags=["runways"])


def get_runway_service(db: Session = Depends(get_db)) -> RunwayService:
    """Dependência para injetar o serviço de pistas"""
    return RunwayService(db)


@router.post("/", response_model=RunwayResponse, status_code=status.HTTP_201_CREATED)
def create_runway(
    runway: RunwayCreate,
    service: RunwayService = Depends(get_runway_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_runway(runway)


@router.get("/", response_model=list[RunwayListResponse])
def list_runways(
    status: RunwayStatus = Query(RunwayStatus.active, description="Filtrar por status: active, inactive ou all"),
    service: RunwayService = Depends(get_runway_service),
    current_user: User = Depends(get_current_user),
):
    return service.list_runways(status=status)


@router.get("/{runway_id}", response_model=RunwayResponse)
def get_runway(
    runway_id: int,
    service: RunwayService = Depends(get_runway_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_runway_by_id(runway_id)


@router.put("/{runway_id}", response_model=RunwayResponse)
def update_runway(
    runway_id: int,
    runway_update: RunwayUpdate,
    service: RunwayService = Depends(get_runway_service),
    current_user: User = Depends(get_current_user),
):
    return service.update_runway(runway_id, runway_update)


@router.patch("/{runway_id}/deactivate", response_model=RunwayResponse)
def deactivate_runway(
    runway_id: int,
    service: RunwayService = Depends(get_runway_service),
    current_user: User = Depends(get_current_user),
):
    return service.deactivate_runway(runway_id)


@router.patch("/{runway_id}/activate", response_model=RunwayResponse)
def activate_runway(
    runway_id: int,
    service: RunwayService = Depends(get_runway_service),
    current_user: User = Depends(get_current_user),
):
    return service.activate_runway(runway_id)


@router.delete("/{runway_id}/hard", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete_runway(
    runway_id: int,
    service: RunwayService = Depends(get_runway_service),
    current_user: User = Depends(get_current_user),
):
    service.hard_delete_runway(runway_id)
