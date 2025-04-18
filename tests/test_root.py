"""Root Test Module.

Description:
- This file contains the test for the root endpoint of the FastAPI application.

"""

from fastapi.testclient import TestClient
from httpx import Response

from .conftest import BASE_URL


def test_root(client: TestClient) -> None:
    """Test the root endpoint."""
    result: Response = client.get(f"{BASE_URL}/")

    assert result.status_code == 200
    assert result.json() == {"detail": "Welcome to FastAPI Assessment"}
