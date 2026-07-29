from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/profile", status_code=status.HTTP_200_OK)
def get_profile(request: Request) -> JSONResponse:
    """
    GET /protected/profile

    Stage 2: Checks that the Authorization header is present and has Bearer format.
    Returns 401 if the header is missing or malformed.

    NOTE: Token is extracted here but NOT cryptographically verified yet.
          Full verification with Supabase will be added in Stage 3.
    """
    auth_header = request.headers.get("Authorization")

    # Check if Authorization header exists and has correct format
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Access token required"}
        )

    # Extract the token from "Bearer <token>"
    token = auth_header.split(" ", 1)[1]

    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Access token required"}
        )

    # Stage 2: Token present but not verified — verification added in Stage 3
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Token received. Verification coming in Stage 3."}
    )
