from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers.users_router import router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@patch("app.routers.users_router.add_user", new_callable=AsyncMock)
def test_create_user(mock_add_user, client):
    mock_add_user.return_value = {
        "id": "123",
        "name": "Test User",
        "email": "test@example.com",
    }

    response = client.post(
        "/users",
        json={"name": "Test User", "email": "test@example.com", "password": "123456"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "123"
    assert data["email"] == "test@example.com"
    mock_add_user.assert_awaited_once()
