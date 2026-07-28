import pytest
from unittest.mock import Mock

from fastapi import HTTPException

from app.models.runway import Runway
from app.schemas.runway import RunwayCreate, RunwayUpdate, RunwayStatus
from app.services.runway import RunwayService


@pytest.fixture
def service():
    service = RunwayService(db=object())
    service.repository = Mock()
    return service


def test_create_runway_should_raise_when_identifier_exists(service):
    service.repository.get_by_identifier.return_value = object()

    runway_data = RunwayCreate(
        identifier="RWY-01",
        length=2500.0,
        surface_type="asfalto",
    )

    with pytest.raises(HTTPException) as context:
        service.create_runway(runway_data)

    assert context.value.status_code == 400
    assert context.value.detail == "Identificador de pista já cadastrado"
    service.repository.create.assert_not_called()


def test_create_runway_should_raise_when_length_invalid(service):
    service.repository.get_by_identifier.return_value = None

    runway_data = RunwayCreate(
        identifier="RWY-02",
        length=0.0,
        surface_type="concreto",
    )

    with pytest.raises(HTTPException) as context:
        service.create_runway(runway_data)

    assert context.value.status_code == 400
    assert context.value.detail == "Comprimento da pista deve ser maior que zero"
    service.repository.create.assert_not_called()


def test_create_runway_should_create_runway(service):
    service.repository.get_by_identifier.return_value = None

    created_runway = Runway(
        id=1,
        identifier="RWY-03",
        length=3000.0,
        surface_type="asfalto",
        active=True,
        occupied=False,
        operation_in_progress=False,
        operation_scheduled=False,
        usage_history="",
    )
    service.repository.create.return_value = created_runway

    runway_data = RunwayCreate(
        identifier="RWY-03",
        length=3000.0,
        surface_type="asfalto",
    )

    result = service.create_runway(runway_data)

    assert result == created_runway
    assert result.identifier == "RWY-03"
    assert result.length == 3000.0
    assert result.surface_type == "asfalto"
    assert result.active is True
    service.repository.create.assert_called_once()


def test_get_runway_by_id_should_raise(service):
    service.repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as context:
        service.get_runway_by_id(999)

    assert context.value.status_code == 404
    assert context.value.detail == "Pista não encontrada"


def test_get_runway_by_id_should_return_runway(service):
    runway = Runway(
        id=1,
        identifier="RWY-04",
        length=2500.0,
        surface_type="concreto",
        active=True,
        occupied=False,
        operation_in_progress=False,
        operation_scheduled=False,
        usage_history="",
    )
    service.repository.get_by_id.return_value = runway

    result = service.get_runway_by_id(1)

    assert result == runway
    assert result.identifier == "RWY-04"
    service.repository.get_by_id.assert_called_once_with(1)


def test_list_runways_with_active_filter(service):
    runways = [
        Runway(
            id=1,
            identifier="RWY-05",
            length=2500.0,
            surface_type="asfalto",
            active=True,
            occupied=False,
            operation_in_progress=False,
            operation_scheduled=False,
            usage_history="",
        )
    ]
    service.repository.get_all.return_value = runways

    result = service.list_runways(status=RunwayStatus.active)

    assert result == runways
    service.repository.get_all.assert_called_once_with(status=RunwayStatus.active)


def test_update_runway_should_raise_when_operation_in_progress(service):
    runway = Runway(
        id=1,
        identifier="RWY-06",
        length=2500.0,
        surface_type="asfalto",
        active=True,
        occupied=False,
        operation_in_progress=True,
        operation_scheduled=False,
        usage_history="",
    )
    service.repository.get_by_id.return_value = runway

    with pytest.raises(HTTPException) as context:
        service.update_runway(1, RunwayUpdate(length=2600.0))

    assert context.value.status_code == 400
    assert context.value.detail == "Não é possível editar pista com operação em andamento ou agendada"


def test_update_runway_should_update_length_and_surface(service):
    runway = Runway(
        id=1,
        identifier="RWY-07",
        length=2500.0,
        surface_type="asfalto",
        active=True,
        occupied=False,
        operation_in_progress=False,
        operation_scheduled=False,
        usage_history="",
    )
    service.repository.get_by_id.return_value = runway
    service.repository.update.return_value = runway

    runway_update = RunwayUpdate(length=2600.0, surface_type="concreto")

    result = service.update_runway(1, runway_update)

    assert result == runway
    assert runway.length == 2600.0
    assert runway.surface_type == "concreto"
    service.repository.update.assert_called_once()


def test_deactivate_runway_should_raise_when_already_inactive(service):
    runway = Runway(
        id=1,
        identifier="RWY-08",
        length=2500.0,
        surface_type="asfalto",
        active=False,
        occupied=False,
        operation_in_progress=False,
        operation_scheduled=False,
        usage_history="",
    )
    service.repository.get_by_id.return_value = runway

    with pytest.raises(HTTPException) as context:
        service.deactivate_runway(1)

    assert context.value.status_code == 400
    assert context.value.detail == "Pista já está inativa"


def test_deactivate_runway_should_raise_when_operation_scheduled(service):
    runway = Runway(
        id=1,
        identifier="RWY-09",
        length=2500.0,
        surface_type="concreto",
        active=True,
        occupied=False,
        operation_in_progress=False,
        operation_scheduled=True,
        usage_history="",
    )
    service.repository.get_by_id.return_value = runway

    with pytest.raises(HTTPException) as context:
        service.deactivate_runway(1)

    assert context.value.status_code == 400
    assert context.value.detail == "Não é possível inativar pista com operação em andamento ou agendada"


def test_deactivate_runway_should_deactivate_runway(service):
    runway = Runway(
        id=1,
        identifier="RWY-10",
        length=2500.0,
        surface_type="asfalto",
        active=True,
        occupied=False,
        operation_in_progress=False,
        operation_scheduled=False,
        usage_history="",
    )
    service.repository.get_by_id.return_value = runway
    service.repository.deactivate.return_value = runway

    result = service.deactivate_runway(1)

    assert result == runway
    service.repository.deactivate.assert_called_once_with(runway)


def test_activate_runway_should_raise_when_already_active(service):
    runway = Runway(
        id=1,
        identifier="RWY-11",
        length=2500.0,
        surface_type="asfalto",
        active=True,
        occupied=False,
        operation_in_progress=False,
        operation_scheduled=False,
        usage_history="",
    )
    service.repository.get_by_id.return_value = runway

    with pytest.raises(HTTPException) as context:
        service.activate_runway(1)

    assert context.value.status_code == 400
    assert context.value.detail == "Pista já está ativa"


def test_activate_runway_should_activate_runway(service):
    runway = Runway(
        id=1,
        identifier="RWY-12",
        length=2500.0,
        surface_type="asfalto",
        active=False,
        occupied=False,
        operation_in_progress=False,
        operation_scheduled=False,
        usage_history="",
    )
    service.repository.get_by_id.return_value = runway
    service.repository.update.return_value = runway

    result = service.activate_runway(1)

    assert result == runway
    assert runway.active is True
    service.repository.update.assert_called_once()
