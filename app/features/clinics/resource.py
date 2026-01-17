"""Clinics resource (response schemas and ORM mapping)."""
from pydantic import BaseModel
from datetime import datetime
from app.features.clinics.schemas import CreateClinicRequestSchema, UpdateClinicRequestSchema

# Re-export request schemas for backward compatibility
CreateClinicRequest = CreateClinicRequestSchema
UpdateClinicRequest = UpdateClinicRequestSchema


class ClinicResponse(BaseModel):
    """Response schema for clinic."""
    
    id: int
    name: str
    address: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
