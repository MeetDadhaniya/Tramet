# config.py — Global configuration: loads environment variables, defines Settings model (DB URIs, API keys, CORS origins, app metadata)

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    All values can be overridden via environment variables at runtime.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App Metadata ─────────────────────────────────────────────
    APP_NAME: str = "Tramet"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development | staging | production

    # ── Server ───────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ── CORS ─────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]  # Vite dev server

    # ── MongoDB (Motor async driver) ─────────────────────────────
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "tramet"

    # ── Neo4j ────────────────────────────────────────────────────
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4j"

    # ── Clerk Authentication ─────────────────────────────────────
    CLERK_SECRET_KEY: str

    # ── LLM / External APIs (optional) ──────────────────────────
    OPENAI_API_KEY: str = ""
    GOOGLE_MAPS_API_KEY: str = ""


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings singleton."""
    return Settings()
