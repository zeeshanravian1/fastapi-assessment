"""Test setup file for pytest.

Description:
- This file contains setup for tests.

"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Delete
from sqlmodel import Session, delete

from fastapi_assessment.apps.api_v1.blog.model import Blog
from fastapi_assessment.apps.api_v1.user.model import User
from fastapi_assessment.database.connection import engine
from main import app

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session]:
    """Create a new database session for each test."""
    with Session(engine) as session:
        yield session
        statement: Delete = delete(Blog)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    """Create a test client for the FastAPI app."""
    with TestClient(app) as c:
        yield c
