"""Users request/response schemas (Pydantic models)."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class CreateUserRequestSchema(BaseModel):
    """Request schema for creating user."""
    
    name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    email: EmailStr = Field(..., description="Valid email address (must be unique)")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")
    role: str = Field(default="member", pattern="^(admin|member)$", description="User role: 'admin' or 'member'")


class UpdateUserRequestSchema(BaseModel):
    """Request schema for updating user."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Updated user name")
    role: Optional[str] = Field(None, pattern="^(admin|member)$", description="Updated user role")
