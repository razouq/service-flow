from fastapi import APIRouter, HTTPException, status

from ..core.security import hash_password
from ..db import db
from ..models.user import UserCreate, UserResponse

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate) -> UserResponse:
    """Create a new user with email and password (hashed)."""
    try:
        # Ensure unique email
        existing = await db.users.find_one({"email": payload.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")

        hashed = hash_password(payload.password)
        result = await db.users.insert_one({
            "email": payload.email,
            "hashed_password": hashed,
        })

        return UserResponse(id=str(result.inserted_id), email=payload.email)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"User creation failed: {exc}")
