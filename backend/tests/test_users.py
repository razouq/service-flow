from unittest.mock import AsyncMock, patch
import pytest


@pytest.mark.asyncio
class TestUserRoutes:
    """Test user management routes."""

    @patch("app.routers.users.db")
    async def test_create_user_success(self, mock_db, client):
        """Successful user creation should return user data."""
        mock_db.users.find_one = AsyncMock(return_value=None)
        mock_db.users.insert_one = AsyncMock()
        mock_db.users.insert_one.return_value.inserted_id = "507f1f77bcf86cd799439011"
        
        response = client.post(
            "/api/users",
            json={"email": "newuser@example.com", "password": "strongpass123"},
        )
        
        assert response.status_code == 201
        assert response.json()["id"] == "507f1f77bcf86cd799439011"
        assert response.json()["email"] == "newuser@example.com"
        mock_db.users.insert_one.assert_called_once()

    @patch("app.routers.users.db")
    async def test_create_user_duplicate_email(self, mock_db, client, sample_user):
        """Creating user with existing email should return 400."""
        mock_db.users.find_one = AsyncMock(return_value=sample_user)
        
        response = client.post(
            "/api/users",
            json={"email": "test@example.com", "password": "strongpass123"},
        )
        
        assert response.status_code == 400
        assert "already in use" in response.json()["detail"]

    def test_create_user_invalid_email(self, client):
        """Creating user with invalid email should fail validation."""
        response = client.post(
            "/api/users",
            json={"email": "invalid-email", "password": "strongpass123"},
        )
        
        assert response.status_code == 422

    def test_create_user_short_password(self, client):
        """Creating user with password < 8 chars should fail validation."""
        response = client.post(
            "/api/users",
            json={"email": "valid@example.com", "password": "short"},
        )
        
        assert response.status_code == 422
        assert "password" in str(response.json()).lower()

    def test_create_user_missing_fields(self, client):
        """Creating user with missing fields should fail validation."""
        response = client.post(
            "/api/users",
            json={"email": "valid@example.com"},
        )
        
        assert response.status_code == 422

    @patch("app.routers.users.db")
    async def test_create_user_database_error(self, mock_db, client):
        """User creation should handle database errors."""
        mock_db.users.find_one = AsyncMock(return_value=None)
        mock_db.users.insert_one = AsyncMock(side_effect=Exception("DB error"))
        
        response = client.post(
            "/api/users",
            json={"email": "test@example.com", "password": "strongpass123"},
        )
        
        assert response.status_code == 500
        assert "User creation failed" in response.json()["detail"]
