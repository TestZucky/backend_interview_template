"""Clinics request/response schemas (Pydantic models)."""
from pydantic import BaseModel, Field
from typing import Optional


class CreateClinicRequestSchema(BaseModel):
    """Request schema for creating clinic."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Clinic name")
    address: str = Field(..., min_length=1, max_length=500, description="Full address")


class UpdateClinicRequestSchema(BaseModel):
    """Request schema for updating clinic."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Updated clinic name")
    address: Optional[str] = Field(None, min_length=1, max_length=500, description="Updated address")
    is_active: Optional[bool] = Field(None, description="Active status")
