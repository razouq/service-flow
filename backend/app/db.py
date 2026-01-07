from motor.motor_asyncio import AsyncIOMotorClient

from .config import get_settings


settings = get_settings()
client = AsyncIOMotorClient(settings.mongo_url)
db = client[settings.mongo_db]


async def ping() -> None:
    """Ping MongoDB to confirm connectivity."""
    await db.command("ping")
