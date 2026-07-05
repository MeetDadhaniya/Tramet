# mongodb.py — MongoDB connection manager: initializes Motor async client, provides database/collection accessors, and handles connection lifecycle

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings

logger = logging.getLogger(__name__)

# ── Private module-level state ───────────────────────────────────
_client: AsyncIOMotorClient | None = None
_database: AsyncIOMotorDatabase | None = None


async def connect_mongodb() -> None:
    """
    Open the Motor async client and select the configured database.

    Verifies connectivity with a ``ping`` command and logs success.
    Raises ``ConnectionError`` if the ping fails.
    """
    global _client, _database

    settings = get_settings()

    _client = AsyncIOMotorClient(settings.MONGODB_URI)
    _database = _client[settings.MONGODB_DB_NAME]

    # Verify the connection is alive
    try:
        await _client.admin.command("ping")
        logger.info(
            "MongoDB connected — database: %s", settings.MONGODB_DB_NAME
        )
    except Exception as exc:
        _client.close()
        _client = None
        _database = None
        raise ConnectionError(
            "Failed to connect to MongoDB. Check your MONGODB_URI."
        ) from exc


async def close_mongodb() -> None:
    """
    Gracefully close the Motor client and reset module-level state.

    Safe to call even if no connection was established.
    """
    global _client, _database

    if _client is not None:
        _client.close()
        logger.info("MongoDB connection closed.")

    _client = None
    _database = None


def get_database() -> AsyncIOMotorDatabase:
    """
    Return the active database handle.

    Must be called **after** ``connect_mongodb()`` has completed.

    Raises
    ------
    RuntimeError
        If called before the database connection has been established.
    """
    if _database is None:
        raise RuntimeError(
            "MongoDB is not connected. Call connect_mongodb() first."
        )
    return _database
