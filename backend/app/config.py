from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field


class Settings(BaseModel):
    mongo_url: str = Field(default="mongodb://localhost:27017", alias="MONGO_URL")
    mongo_db: str = Field(default="fastapi_db", alias="MONGO_DB")
    allowed_origins: List[str] = Field(default_factory=lambda: ["*"])

    class Config:
        populate_by_name = True


@lru_cache
def get_settings() -> Settings:
    """Return cached app settings loaded from environment variables."""
    return Settings()  # Environment variables override defaults
