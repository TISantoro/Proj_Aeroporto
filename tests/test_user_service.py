import pytest
from unittest.mock import Mock

from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user import UserService


@pytest.fixture
def service():
    service = UserService(db=object())
    service.repository = Mock()
    return service


def test_create_user_should_raise_when_email_already_exists(service):
    service.repository.get_by_email.return_value = object()

    user_data = UserCreate(
        name="João",
        email="joao@example.com",
        login="joao",
        password="123456",
    )

    with pytest.raises(HTTPException) as context:
        service.create_user(user_data)

    assert context.value.status_code == 400
    assert context.value.detail == "Email já cadastrado"
    service.repository.create.assert_not_called()


def test_create_user_should_raise_when_login_already_exists(service):
    service.repository.get_by_email.return_value = None
    service.repository.get_by_login.return_value = object()

    user_data = UserCreate(
        name="Maria",
        email="maria@example.com",
        login="maria",
        password="123456",
    )

    with pytest.raises(HTTPException) as context:
        service.create_user(user_data)

    assert context.value.status_code == 400
    assert context.value.detail == "Login já cadastrado"
    service.repository.create.assert_not_called()


def test_create_user_should_create_when_data_is_valid(service):
    service.repository.get_by_email.return_value = None
    service.repository.get_by_login.return_value = None

    created_user = User(
        id=1,
        name="Ana",
        email="ana@example.com",
        login="ana",
        password="123456",
        active=True,
    )
    service.repository.create.return_value = created_user

    user_data = UserCreate(
        name="Ana",
        email="ana@example.com",
        login="ana",
        password="123456",
    )

    result = service.create_user(user_data)

    assert result == created_user
    service.repository.create.assert_called_once()

    created_object = service.repository.create.call_args.args[0]
    assert created_object.name == "Ana"
    assert created_object.email == "ana@example.com"
    assert created_object.login == "ana"


def test_get_user_by_id_should_raise_when_user_not_found(service):
    service.repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as context:
        service.get_user_by_id(999)

    assert context.value.status_code == 404
    assert context.value.detail == "Usuário não encontrado"
