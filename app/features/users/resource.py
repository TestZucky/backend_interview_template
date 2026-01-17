"""Users resource (response schemas and ORM mapping)."""
from pydantic import BaseModel
from datetime import datetime
from app.features.users.schemas import CreateUserRequestSchema, UpdateUserRequestSchema

# Re-export request schemas for backward compatibility
CreateUserRequest = CreateUserRequestSchema
UpdateUserRequest = UpdateUserRequestSchema


class UserResponse(BaseModel):
    """Response schema for user."""
    
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

