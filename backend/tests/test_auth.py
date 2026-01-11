from unittest.mock import AsyncMock, patch
import pytest

from app.core.security import hash_password


@pytest.mark.asyncio
class TestAuthRoutes:
    """Test authentication routes."""

    @patch("app.routers.auth.db")
    async def test_login_success(self, mock_db, client, sample_user):
        """Successful login should return access token."""
        mock_db.users.find_one = AsyncMock(return_value=sample_user)
        
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    @patch("app.routers.auth.db")
    async def test_login_invalid_email(self, mock_db, client):
        """Login with non-existent email should return 401."""
        mock_db.users.find_one = AsyncMock(return_value=None)
        
        response = client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"},
        )
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    @patch("app.routers.auth.db")
    async def test_login_invalid_password(self, mock_db, client, sample_user):
        """Login with wrong password should return 401."""
        mock_db.users.find_one = AsyncMock(return_value=sample_user)
        
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    def test_login_invalid_email_format(self, client):
        """Login with invalid email format should fail validation."""
        response = client.post(
            "/api/auth/login",
            json={"email": "not-an-email", "password": "password123"},
        )
        
        assert response.status_code == 422
        assert "email" in str(response.json()).lower()

    def test_login_missing_fields(self, client):
        """Login with missing fields should fail validation."""
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com"},
        )
        
        assert response.status_code == 422

    @patch("app.routers.auth.db")
    async def test_login_database_error(self, mock_db, client):
        """Login should handle database errors gracefully."""
        mock_db.users.find_one = AsyncMock(side_effect=Exception("DB error"))
        
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        
        assert response.status_code == 500
