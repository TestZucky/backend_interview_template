"""Auth request/response schemas (Pydantic models)."""
from pydantic import BaseModel, EmailStr, Field


class SignupRequestSchema(BaseModel):
    """Request schema for signup."""
    
    name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    email: EmailStr = Field(..., description="Valid email address (must be unique)")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")
    role: str = Field(default="member", pattern="^(admin|member)$", description="User role: 'admin' or 'member'")


class LoginRequestSchema(BaseModel):
    """Request schema for login."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
