from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]

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
    serviceType: str = Field(..., alias="serviceType")
    description: Optional[str] = None

    class Config:
        populate_by_name = True


class QuoteResponse(BaseModel):
    id: str
    message: str


@app.get("/")
def root():
    return {"message": "FastAPI + MongoDB"}


@app.get("/health")
async def health():
    await db.command("ping")
    return {"ok": True}


@app.post("/api/quotes", response_model=QuoteResponse)
async def create_quote(quote: QuoteRequest):
    """
    Create a new quote request and save it to MongoDB
    """
    try:
        quote_doc = quote.model_dump(by_alias=True)
        quote_doc["createdAt"] = datetime.utcnow()
        quote_doc["status"] = QuoteStatus.PENDING.value
        
        result = await db.quotes.insert_one(quote_doc)
        
        return QuoteResponse(
            id=str(result.inserted_id),
            message="Quote request submitted successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create quote: {str(e)}")


@app.get("/api/quotes")
async def get_quotes():
    """
    Get all quote requests from MongoDB
    """
    try:
        quotes = []
        cursor = db.quotes.find().sort("createdAt", -1)
        async for document in cursor:
            document["id"] = str(document["_id"])
            del document["_id"]
            quotes.append(document)
        return {"quotes": quotes, "count": len(quotes)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch quotes: {str(e)}")

