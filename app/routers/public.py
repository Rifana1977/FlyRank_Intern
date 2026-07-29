from fastapi import APIRouter, status

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/info", status_code=status.HTTP_200_OK)
def public_info() -> dict:
    """
    GET /public/info

    Public endpoint — no authentication required.
    Returns a welcome message accessible to anyone.
    """
    return {"message": "Welcome stranger! This info is public."}
