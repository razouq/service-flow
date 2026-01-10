from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .db import ping
from .routers import auth, quotes, users

settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict:
    return {"message": "FastAPI + MongoDB"}


@app.get("/health")
async def health() -> dict:
    await ping()
    return {"ok": True}


# Routers
app.include_router(auth.router)
app.include_router(quotes.router)
app.include_router(users.router)
