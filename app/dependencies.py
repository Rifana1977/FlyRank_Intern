from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.supabase_client import supabase


class AuthException(Exception):
    """Custom exception for authentication failures."""
    def __init__(self, status_code: int, error_message: str):
        self.status_code = status_code
        self.error_message = error_message


def get_current_user(request: Request) -> dict:
    """
    Reusable FastAPI dependency to authenticate requests via Supabase JWT.

    1. Checks for Authorization header with 'Bearer <token>'
    2. Verifies token with Supabase (supabase.auth.get_user)
    3. Returns authenticated user payload
    4. Raises AuthException on missing or invalid token
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_message="Access token required"
        )

    token = auth_header.split(" ", 1)[1].strip()

    if not token:
        raise AuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_message="Access token required"
        )

    try:
        response = supabase.auth.get_user(token)

        if response is None or response.user is None:
            raise AuthException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error_message="Invalid or expired token"
            )

        user = response.user
        return {
            "id": str(user.id),
            "email": user.email,
            "created_at": str(user.created_at),
            "token": token
        }

    except AuthException:
        raise
    except Exception:
        raise AuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_message="Invalid or expired token"
        )
