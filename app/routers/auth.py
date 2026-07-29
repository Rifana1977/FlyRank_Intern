from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.supabase_client import supabase
from app.auth_schemas import SignupRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest) -> JSONResponse:
    """
    POST /auth/signup

    Creates a new user account using Supabase Auth.

    - Requires: email, password
    - Returns 400 if email or password is missing or invalid
    - Returns 201 with safe user information on success
    - Password is never returned in the response
    """
    # Validate that fields are not empty strings
    if not payload.email.strip() or not payload.password.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Email and password are required"}
        )

    try:
        response = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password
        })

        if response.user is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Signup failed. Please try again."}
            )

        user = response.user
        # Return only safe, non-sensitive user fields
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "id": str(user.id),
                "email": user.email,
                "created_at": str(user.created_at)
            }
        )

    except Exception as e:
        error_message = str(e)
        # Email already registered
        if "already registered" in error_message.lower():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Email already registered"}
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": error_message}
        )


@router.post("/login", status_code=status.HTTP_200_OK)
def login(payload: LoginRequest) -> JSONResponse:
    """
    POST /auth/login

    Authenticates a user using Supabase signInWithPassword.

    - Returns 200 with access_token and refresh_token on success
    - Returns 401 for wrong credentials or non-existent user
    """
    try:
        response = supabase.auth.sign_in_with_password({
            "email": payload.email,
            "password": payload.password
        })

        if response.session is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": "Invalid login credentials"}
            )

        session = response.session
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "token_type": "bearer"
            }
        )

    except Exception:
        # Any auth failure (wrong password, user not found, etc.) → 401
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid login credentials"}
        )
