from fastapi import Header, HTTPException, status
from app.core.firebase import verify_token


async def get_current_user(authorization: str = Header(...)) -> dict:
    """Extract and verify the Firebase ID token from the Authorization header."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Use 'Bearer <token>'.",
        )

    token = authorization[7:]
    try:
        decoded = verify_token(token)
        return decoded
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )
