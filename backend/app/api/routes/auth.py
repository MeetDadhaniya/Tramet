# auth.py — Temporary auth test route for verifying Clerk authentication end-to-end.

from fastapi import APIRouter, Depends
from app.core.auth import require_auth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def get_current_user(user_id: str = Depends(require_auth)):
    """Temporary endpoint to verify Clerk authentication works end-to-end."""
    return {"authenticated": True, "user_id": user_id}
