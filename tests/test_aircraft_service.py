import pytest
from unittest.mock import Mock

from fastapi import HTTPException

from app.models.aircraft import Aircraft
from app.schemas.aircraft import AircraftCreate, AircraftUpdate
from app.services.aircraft import AircraftService


@pytest.fixture
def service():
    service = AircraftService(db=object())
    service.repository = Mock()
    return service


def test_create_plane_should_raise_when_registration_exists(service):
    """Deve lançar exceção quando identificador de avião já existe"""
    service.repository.get_by_identifier.return_value = object()

    aircraft_data = AircraftCreate(
        identifier="PT-ABC",
        model="Boeing 737",
        airline="LATAM",
        capacity=180,
    )

    with pytest.raises(HTTPException) as context:
        service.create_aircraft(aircraft_data)

    assert context.value.status_code == 400
    assert context.value.detail == "Identificador de avião já cadastrado"
    service.repository.create.assert_not_called()


def test_create_plane_should_create_plane(service):
    """Deve criar um novo avião com dados válidos"""
    service.repository.get_by_identifier.return_value = None

    created_aircraft = Aircraft(
        id=1,
        identifier="PT-XYZ",
        model="Airbus A320",
        airline="Gol",
        capacity=190,
        active=True,
    )
    service.repository.create.return_value = created_aircraft

    aircraft_data = AircraftCreate(
        identifier="PT-XYZ",
        model="Airbus A320",
        airline="Gol",
        capacity=190,
    )

    result = service.create_aircraft(aircraft_data)

    assert result == created_aircraft
    assert result.identifier == "PT-XYZ"
    assert result.model == "Airbus A320"
    assert result.airline == "Gol"
    assert result.capacity == 190
    assert result.active is True
    service.repository.create.assert_called_once()

    created_object = service.repository.create.call_args.args[0]
    assert created_object.identifier == "PT-XYZ"
    assert created_object.model == "Airbus A320"
    assert created_object.airline == "Gol"
    assert created_object.capacity == 190
    assert created_object.active is True


def test_get_plane_by_id_should_raise(service):
    """Deve lançar exceção quando avião não é encontrado"""
    service.repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as context:
        service.get_aircraft_by_id(999)

    assert context.value.status_code == 404
    assert context.value.detail == "Avião não encontrado"


def test_get_plane_by_id_should_return_aircraft(service):
    """Deve retornar avião quando ID é válido"""
    aircraft = Aircraft(
        id=1,
        identifier="PT-ABC",
        model="Boeing 737",
        airline="LATAM",
        capacity=180,
        active=True,
    )
    service.repository.get_by_id.return_value = aircraft

    result = service.get_aircraft_by_id(1)

    assert result == aircraft
    assert result.identifier == "PT-ABC"
    service.repository.get_by_id.assert_called_once_with(1)


def test_update_plane(service):
    """Deve atualizar dados de um avião existente"""
    existing_aircraft = Aircraft(
        id=1,
        identifier="PT-ABC",
        model="Boeing 737",
        airline="LATAM",
        capacity=180,
        active=True,
    )
    service.repository.get_by_id.return_value = existing_aircraft
    service.repository.update.return_value = existing_aircraft

    aircraft_update = AircraftUpdate(
        model="Boeing 777",
        capacity=350,
    )

    result = service.update_aircraft(1, aircraft_update)

    assert result == existing_aircraft
    assert existing_aircraft.model == "Boeing 777"
    assert existing_aircraft.capacity == 350
    service.repository.update.assert_called_once()


def test_delete_plane(service):
    """Deve inativar um avião (soft delete)"""
    aircraft = Aircraft(
        id=1,
        identifier="PT-ABC",
        model="Boeing 737",
        airline="LATAM",
        capacity=180,
        active=True,
    )
    service.repository.get_by_id.return_value = aircraft
    service.repository.deactivate.return_value = aircraft

    result = service.deactivate_aircraft(1)

    assert result == aircraft
    service.repository.deactivate.assert_called_once_with(aircraft)


def test_delete_plane_should_raise_when_already_inactive(service):
    """Deve lançar exceção quando avião já está inativo"""
    aircraft = Aircraft(
        id=1,
        identifier="PT-ABC",
        model="Boeing 737",
        airline="LATAM",
        capacity=180,
        active=False,
    )
    service.repository.get_by_id.return_value = aircraft

    with pytest.raises(HTTPException) as context:
        service.deactivate_aircraft(1)

    assert context.value.status_code == 400
    assert context.value.detail == "Avião já está inativo"
    service.repository.deactivate.assert_not_called()


def test_activate_plane(service):
    """Deve ativar um avião inativo"""
    aircraft = Aircraft(
        id=1,
        identifier="PT-ABC",
        model="Boeing 737",
        airline="LATAM",
        capacity=180,
        active=False,
    )
    service.repository.get_by_id.return_value = aircraft
    service.repository.update.return_value = aircraft

    result = service.activate_aircraft(1)

    assert result == aircraft
    assert aircraft.active is True
    service.repository.update.assert_called_once()


def test_activate_plane_should_raise_when_already_active(service):
    """Deve lançar exceção quando avião já está ativo"""
    aircraft = Aircraft(
        id=1,
        identifier="PT-ABC",
        model="Boeing 737",
        airline="LATAM",
        capacity=180,
        active=True,
    )
    service.repository.get_by_id.return_value = aircraft

    with pytest.raises(HTTPException) as context:
        service.activate_aircraft(1)

    assert context.value.status_code == 400
    assert context.value.detail == "Avião já está ativo"
    service.repository.update.assert_not_called()


def test_list_aircrafts_with_active_filter(service):
    """Deve listar apenas aviões ativos por padrão"""
    aircrafts = [
        Aircraft(
            id=1,
            identifier="PT-ABC",
            model="Boeing 737",
            airline="LATAM",
            capacity=180,
            active=True,
        ),
        Aircraft(
            id=2,
            identifier="PT-XYZ",
            model="Airbus A320",
            airline="Gol",
            capacity=190,
            active=True,
        ),
    ]
    service.repository.get_all.return_value = aircrafts

    result = service.list_aircrafts(active_only=True)

    assert len(result) == 2
    assert all(aircraft.active for aircraft in result)
    service.repository.get_all.assert_called_once_with(active_only=True, identifier_filter=None)


def test_list_aircrafts_with_identifier_search(service):
    """Deve buscar avião pelo identificador"""
    aircrafts = [
        Aircraft(
            id=1,
            identifier="PT-ABC",
            model="Boeing 737",
            airline="LATAM",
            capacity=180,
            active=True,
        ),
    ]
    service.repository.get_all.return_value = aircrafts

    result = service.list_aircrafts(active_only=True, identifier_filter="PT-ABC")

    assert len(result) == 1
    assert result[0].identifier == "PT-ABC"
    service.repository.get_all.assert_called_once_with(active_only=True, identifier_filter="PT-ABC")
