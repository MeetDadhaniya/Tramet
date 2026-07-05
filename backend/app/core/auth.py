# auth.py — Clerk authentication dependency for FastAPI routes.

from fastapi import Depends, HTTPException, Request, status
from clerk_backend_api import authenticate_request_async
from clerk_backend_api.security.types import AuthenticateRequestOptions

from app.core.config import Settings, get_settings


async def require_auth(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> str:
    """
    FastAPI dependency that verifies the Clerk session token
    from the Authorization header and returns the authenticated user ID.

    Usage:
        @app.get("/protected")
        async def protected_route(user_id: str = Depends(require_auth)):
            ...

    Raises:
        HTTPException 401 if the token is missing, malformed, or invalid.
    """
    options = AuthenticateRequestOptions(secret_key=settings.CLERK_SECRET_KEY)
    state = await authenticate_request_async(request, options)

    if not state.is_signed_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=state.message or "Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # The 'sub' claim in a Clerk session token is the user ID (e.g. "user_abc123")
    user_id: str | None = state.payload.get("sub") if state.payload else None
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id
