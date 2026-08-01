from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from app.dependencies import get_current_user

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/profile", status_code=status.HTTP_200_OK)
def get_profile(current_user: dict = Depends(get_current_user)) -> JSONResponse:
    """
    GET /protected/profile

    Protected route using reusable get_current_user dependency.
    Returns user id, email, and created_at.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "id": current_user["id"],
            "email": current_user["email"],
            "created_at": current_user["created_at"]
        }
    )


@router.get("/dashboard", status_code=status.HTTP_200_OK)
def get_dashboard(current_user: dict = Depends(get_current_user)) -> JSONResponse:
    """
    GET /protected/dashboard

    Second protected route using the exact same get_current_user dependency.
    Returns dashboard welcome message for the authenticated user.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Welcome to your dashboard, {current_user['email']}!",
            "user_id": current_user["id"]
        }
    )


