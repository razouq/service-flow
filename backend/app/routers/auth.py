from fastapi import APIRouter, HTTPException

from ..core.security import create_access_token, hash_password, verify_password
from ..db import db
from ..models.user import Token, UserLogin

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin) -> Token:
    """Authenticate user with email and password, return JWT token."""
    try:
        # Find user by email
        user = await db.users.find_one({"email": credentials.email})
        
        if not user:
            raise HTTPException(
                status_code=401, detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(credentials.password, user.get("hashed_password", "")):
            raise HTTPException(
                status_code=401, detail="Invalid email or password"
            )
        
        # Create JWT token
        access_token = create_access_token(
            data={"email": credentials.email, "user_id": str(user["_id"])}
        )
        
        return Token(access_token=access_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Login failed: {exc}")


@router.post("/register", response_model=Token)
async def register(user_data: UserLogin) -> Token:
    """Register a new user with email and password."""
    try:
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password and create user
        hashed_password = hash_password(user_data.password)
        result = await db.users.insert_one({
            "email": user_data.email,
            "hashed_password": hashed_password,
        })
        
        # Create JWT token
        access_token = create_access_token(
            data={"email": user_data.email, "user_id": str(result.inserted_id)}
        )
        
        return Token(access_token=access_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Registration failed: {exc}")
