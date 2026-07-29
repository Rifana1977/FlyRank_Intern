from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    """
    Request body for POST /auth/signup.
    Both email and password are required.
    """
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password (min 6 characters recommended)")


class LoginRequest(BaseModel):
    """
    Request body for POST /auth/login.
    """
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    """
    Safe user information returned after signup.
    Sensitive fields like password hash are never included.
    """
    id: str = Field(..., description="Supabase user UUID")
    email: str = Field(..., description="User's email address")
    created_at: str = Field(..., description="Account creation timestamp")


class TokenResponse(BaseModel):
    """
    Token payload returned after successful login.
    """
    access_token: str = Field(..., description="JWT access token for API requests")
    refresh_token: str = Field(..., description="Token used to obtain a new access token")
    token_type: str = Field(default="bearer", description="Token type")
