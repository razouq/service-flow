from unittest.mock import AsyncMock, patch
import pytest
from datetime import datetime


@pytest.mark.asyncio
class TestQuoteRoutes:
    """Test quote management routes."""

    @patch("app.routers.quotes.db")
    async def test_create_quote_success(self, mock_db, client):
        """Successful quote creation should return quote ID."""
        mock_db.quotes.insert_one = AsyncMock()
        mock_db.quotes.insert_one.return_value.inserted_id = "507f1f77bcf86cd799439012"
        
        response = client.post(
            "/api/quotes",
            json={
                "name": "John Doe",
                "phone": "555-1234",
                "address": "123 Main St",
                "serviceType": "plumbing",
                "description": "Pipe repair",
            },
        )
        
        assert response.status_code == 200
        assert response.json()["id"] == "507f1f77bcf86cd799439012"
        assert response.json()["message"] == "Quote request submitted successfully"

    def test_create_quote_missing_required_field(self, client):
        """Creating quote without required field should fail."""
        response = client.post(
            "/api/quotes",
            json={
                "name": "John Doe",
                "phone": "555-1234",
                # Missing address and serviceType
            },
        )
        
        assert response.status_code == 422

    def test_create_quote_short_name(self, client):
        """Creating quote with name < 2 chars should fail."""
        response = client.post(
            "/api/quotes",
            json={
                "name": "J",
                "phone": "555-1234",
                "address": "123 Main St",
                "serviceType": "plumbing",
            },
        )
        
        assert response.status_code == 422

    def test_create_quote_short_address(self, client):
        """Creating quote with address < 5 chars should fail."""
        response = client.post(
            "/api/quotes",
            json={
                "name": "John Doe",
                "phone": "555-1234",
                "address": "123",
                "serviceType": "plumbing",
            },
        )
        
        assert response.status_code == 422

    @patch("app.routers.quotes.db")
    async def test_get_quotes_default_pagination(self, mock_db, client, sample_quote):
        """Get quotes with default pagination should work."""
        mock_db.quotes.count_documents = AsyncMock(return_value=1)
        mock_db.quotes.find = AsyncMock()
        mock_db.quotes.find.return_value.sort = AsyncMock()
        mock_db.quotes.find.return_value.sort.return_value.skip = AsyncMock()
        mock_db.quotes.find.return_value.sort.return_value.skip.return_value.limit = AsyncMock()
        
        # Mock the async iterator
        async def mock_async_iter(self):
            yield sample_quote
        
        mock_db.quotes.find.return_value.sort.return_value.skip.return_value.limit.return_value.__aiter__ = mock_async_iter
        
        response = client.get("/api/quotes")
        
        assert response.status_code == 200
        data = response.json()
        assert "quotes" in data
        assert "pagination" in data
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["limit"] == 10

    @patch("app.routers.quotes.db")
    async def test_get_quotes_custom_pagination(self, mock_db, client, sample_quote):
        """Get quotes with custom page and limit should work."""
        mock_db.quotes.count_documents = AsyncMock(return_value=25)
        mock_db.quotes.find = AsyncMock()
        mock_db.quotes.find.return_value.sort = AsyncMock()
        mock_db.quotes.find.return_value.sort.return_value.skip = AsyncMock()
        mock_db.quotes.find.return_value.sort.return_value.skip.return_value.limit = AsyncMock()
        
        async def mock_async_iter(self):
            yield sample_quote
        
        mock_db.quotes.find.return_value.sort.return_value.skip.return_value.limit.return_value.__aiter__ = mock_async_iter
        
        response = client.get("/api/quotes?page=2&limit=5")
        
        assert response.status_code == 200
        data = response.json()
        assert data["pagination"]["page"] == 2
        assert data["pagination"]["limit"] == 5
        assert data["pagination"]["total"] == 25
        assert data["pagination"]["totalPages"] == 5
        assert data["pagination"]["hasNext"] is True
        assert data["pagination"]["hasPrev"] is True

    def test_get_quotes_invalid_page(self, client):
        """Get quotes with invalid page should fail validation."""
        response = client.get("/api/quotes?page=0")
        
        assert response.status_code == 422

    def test_get_quotes_invalid_limit(self, client):
        """Get quotes with limit > 100 should fail validation."""
        response = client.get("/api/quotes?limit=200")
        
        assert response.status_code == 422

    @patch("app.routers.quotes.db")
    async def test_create_quote_database_error(self, mock_db, client):
        """Quote creation should handle database errors."""
        mock_db.quotes.insert_one = AsyncMock(side_effect=Exception("DB error"))
        
        response = client.post(
            "/api/quotes",
            json={
                "name": "John Doe",
                "phone": "555-1234",
                "address": "123 Main St",
                "serviceType": "plumbing",
            },
        )
        
        assert response.status_code == 500
        assert "Failed to create quote" in response.json()["detail"]

    @patch("app.routers.quotes.db")
    async def test_get_quotes_database_error(self, mock_db, client):
        """Get quotes should handle database errors."""
        mock_db.quotes.count_documents = AsyncMock(side_effect=Exception("DB error"))
        
        response = client.get("/api/quotes")
        
        assert response.status_code == 500
        assert "Failed to fetch quotes" in response.json()["detail"]
