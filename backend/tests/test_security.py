import pytest
from datetime import timedelta

from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
    TokenData,
)


class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_hash_password(self):
        """Hashing should produce a non-empty bcrypt hash."""
        password = "mysecretpassword"
        hashed = hash_password(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 20  # bcrypt hashes are long

    def test_verify_password_correct(self):
        """Correct password should verify successfully."""
        password = "correctpassword"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Incorrect password should fail verification."""
        password = "correctpassword"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_hash_consistency(self):
        """Same password hashed twice produces different hashes (due to salt)."""
        password = "testpassword"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)


class TestTokenManagement:
    """Test JWT token creation and decoding."""

    def test_create_access_token(self):
        """Token creation should return a valid JWT string."""
        data = {"email": "test@example.com", "user_id": "12345"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 20  # JWT tokens are longer

    def test_decode_valid_token(self):
        """Valid token should decode correctly."""
        data = {"email": "test@example.com", "user_id": "12345"}
        token = create_access_token(data)
        decoded = decode_token(token)
        
        assert decoded is not None
        assert decoded.email == "test@example.com"
        assert decoded.user_id == "12345"

    def test_decode_invalid_token(self):
        """Invalid token should return None."""
        invalid_token = "invalid.token.here"
        decoded = decode_token(invalid_token)
        
        assert decoded is None

    def test_decode_malformed_token(self):
        """Malformed token should return None."""
        malformed = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"  # Incomplete JWT
        decoded = decode_token(malformed)
        
        assert decoded is None

    def test_token_with_custom_expiry(self):
        """Token with custom expiry should work."""
        data = {"email": "test@example.com"}
        custom_expiry = timedelta(hours=24)
        token = create_access_token(data, expires_delta=custom_expiry)
        decoded = decode_token(token)
        
        assert decoded is not None
        assert decoded.email == "test@example.com"

    def test_token_data_model(self):
        """TokenData should be created with optional fields."""
        token_data = TokenData(email="test@example.com", user_id="12345")
        assert token_data.email == "test@example.com"
        assert token_data.user_id == "12345"

        token_data_minimal = TokenData()
        assert token_data_minimal.email is None
        assert token_data_minimal.user_id is None
