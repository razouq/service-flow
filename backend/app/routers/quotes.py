from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

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
async def get_quotes(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
) -> dict:
    """Retrieve paginated quote requests sorted by creation date (desc)."""
    try:
        skip = (page - 1) * limit
        
        # Get total count for pagination metadata
        total_count = await db.quotes.count_documents({})
        
        # Fetch paginated quotes
        quotes = []
        cursor = db.quotes.find().sort("createdAt", -1).skip(skip).limit(limit)
        async for document in cursor:
            quotes.append(serialize_quote(document).model_dump(by_alias=True))

        total_pages = (total_count + limit - 1) // limit  # Ceiling division

        return {
            "quotes": quotes,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "totalPages": total_pages,
                "hasNext": page < total_pages,
                "hasPrev": page > 1,
            },
        }
    except Exception as exc:  # pragma: no cover - defensive barrier
        raise HTTPException(status_code=500, detail=f"Failed to fetch quotes: {exc}")
