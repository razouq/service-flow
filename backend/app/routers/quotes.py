from datetime import datetime

from fastapi import APIRouter, HTTPException

from ..db import db
from ..models.quote import QuoteRequest, QuoteResponse, QuoteStatus, serialize_quote

router = APIRouter(prefix="/api/quotes", tags=["quotes"])


@router.post("", response_model=QuoteResponse)
async def create_quote(quote: QuoteRequest) -> QuoteResponse:
    """Create a new quote request and persist it to MongoDB."""
    try:
        quote_doc = quote.model_dump(by_alias=True)
        quote_doc["createdAt"] = datetime.utcnow()
        quote_doc["status"] = QuoteStatus.PENDING.value

        result = await db.quotes.insert_one(quote_doc)

        return QuoteResponse(
            id=str(result.inserted_id),
            message="Quote request submitted successfully",
        )
    except Exception as exc:  # pragma: no cover - defensive barrier
        raise HTTPException(status_code=500, detail=f"Failed to create quote: {exc}")


@router.get("")
async def get_quotes() -> dict:
    """Retrieve all quote requests sorted by creation date (desc)."""
    try:
        quotes = []
        cursor = db.quotes.find().sort("createdAt", -1)
        async for document in cursor:
            quotes.append(serialize_quote(document).model_dump(by_alias=True))

        return {"quotes": quotes, "count": len(quotes)}
    except Exception as exc:  # pragma: no cover - defensive barrier
        raise HTTPException(status_code=500, detail=f"Failed to fetch quotes: {exc}")
