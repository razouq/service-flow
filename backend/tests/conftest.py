import pytest
from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Provide a mock database."""
    mock = MagicMock()
    mock.command = AsyncMock()
    return mock


@pytest.fixture
def sample_user():
    """Provide sample user data."""
    return {
        "_id": "507f1f77bcf86cd799439011",
        "email": "test@example.com",
        "hashed_password": hash_password("password123"),
    }


@pytest.fixture
def sample_quote():
    """Provide sample quote data."""
    from datetime import datetime
    return {
        "_id": "507f1f77bcf86cd799439012",
        "name": "John Doe",
        "phone": "555-1234",
        "address": "123 Main St, Springfield",
        "serviceType": "plumbing",
        "status": "PENDING",
        "createdAt": datetime.utcnow(),
        "description": "Need pipe repair",
    }
