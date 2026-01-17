"""Auth resource (response schemas and ORM mapping)."""
from pydantic import BaseModel
from datetime import datetime
from app.features.auth.schemas import SignupRequestSchema, LoginRequestSchema

# Re-export request schemas for backward compatibility
SignupRequest = SignupRequestSchema
LoginRequest = LoginRequestSchema


class UserResponse(BaseModel):
    """Response schema for user."""
    
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Response schema for login."""
    
    access_token: str
    user: UserResponse
