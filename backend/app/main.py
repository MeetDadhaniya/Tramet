# main.py — FastAPI application entry point: creates the app instance, registers routers, configures CORS middleware, and startup/shutdown events
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.database.mongodb import connect_mongodb, close_mongodb

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    await connect_mongodb()
    try:
        yield
    finally:
        await close_mongodb()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────
from app.api.routes.auth import router as auth_router
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Tramet backend is running"}