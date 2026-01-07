from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class QuoteStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class QuoteRequest(BaseModel):
    name: str = Field(..., min_length=2)
    phone: str = Field(..., min_length=1)
    address: str = Field(..., min_length=5)
    service_type: str = Field(..., alias="serviceType")
    description: Optional[str] = None

    class Config:
        populate_by_name = True


class QuoteResponse(BaseModel):
    id: str
    message: str


class QuoteDTO(BaseModel):
    id: str
    name: str
    phone: str
    address: str
    service_type: str = Field(..., alias="serviceType")
    status: Optional[QuoteStatus] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    description: Optional[str] = None

    class Config:
        populate_by_name = True


def serialize_quote(document: dict) -> QuoteDTO:
    """Normalize MongoDB document into a QuoteDTO."""
    document = document.copy()
    document["id"] = str(document.get("_id"))
    document.pop("_id", None)
    return QuoteDTO.model_validate(document)
