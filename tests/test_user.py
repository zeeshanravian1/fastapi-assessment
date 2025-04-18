"""User Test Module.

Description:
- This file contains the test for the user endpoint of the FastAPI application.

"""

from fastapi.testclient import TestClient
from httpx import Response

from fastapi_assessment.apps.api_v1.user.model import UserCreate
from fastapi_assessment.core.config import settings

from .conftest import BASE_URL


def test_create_user(client: TestClient) -> None:
    """Test Create User."""
    user_in = UserCreate(
        first_name="John",
        last_name="Doe",
        username="johndoe",
        email="johndoe@example.com",
        password="Password@123",
    )

    result: Response = client.post(
        f"{BASE_URL}/{settings.API_V1_STR}/user/",
        json=user_in.model_dump(),
    )

    assert result.status_code == 201
    created_user = result.json()["data"]

    assert created_user["first_name"] == user_in.first_name
    assert created_user["last_name"] == user_in.last_name
    assert created_user["username"] == user_in.username
    assert created_user["email"] == user_in.email
    assert created_user["is_active"] is True


def test_create_user_with_existing_username(client: TestClient) -> None:
    """Test Create User with Existing Username."""
    user_in = UserCreate(
        first_name="Jane",
        last_name="Doe",
        username="johndoe",  # Same username as before
        email="johndoe@example.com",
        password="Password@123",
    )

    result: Response = client.post(
        f"{BASE_URL}/{settings.API_V1_STR}/user/",
        json=user_in.model_dump(),
    )

    assert result.status_code == 409
