"""Clinics routes (endpoints)."""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from app.db import get_db
from app.core.permissions import get_current_user, require_role, require_any_role
from app.features.clinics.service import ClinicsService
from app.features.clinics.resource import CreateClinicRequest, UpdateClinicRequest, ClinicResponse
from app.shared.responses import success_response, error_response
from app.shared.decorators import validate_json
from app.shared.exceptions import AppException

clinics_bp = Blueprint("clinics", __name__, url_prefix="/clinics")


@clinics_bp.route("", methods=["POST"])
@validate_json
@require_role("admin")
def create_clinic():
    """Create a new clinic (admin only)."""
    try:
        data = request.get_json()
        create_request = CreateClinicRequest(**data)
        
        db = next(get_db())
        clinic = ClinicsService.create_clinic(
            db=db,
            name=create_request.name,
            address=create_request.address,
        )
        
        clinic_response = ClinicResponse.from_orm(clinic)
        return success_response(
            data=clinic_response.dict(),
            message="Clinic created successfully",
            status_code=201
        )
    
    except AppException as e:
        return error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            error="INVALID_REQUEST",
            message=str(e),
            status_code=400
        )


@clinics_bp.route("/<int:clinic_id>", methods=["GET"])
@require_any_role(["admin", "member"])
def get_clinic(clinic_id: int):
    """Get clinic by ID."""
    try:
        db = next(get_db())
        clinic = ClinicsService.get_clinic(db, clinic_id)
        
        clinic_response = ClinicResponse.from_orm(clinic)
        return success_response(data=clinic_response.dict())
    
    except AppException as e:
        return error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            error="SERVER_ERROR",
            message=str(e),
            status_code=500
        )


@clinics_bp.route("", methods=["GET"])
@require_any_role(["admin", "member"])
def list_clinics():
    """List all clinics."""
    try:
        current_user = get_current_user()
        db = next(get_db())
        
        # Members can only see active clinics, admins see all
        active_only = current_user.get("role") == "member"
        clinics = ClinicsService.list_clinics(db, active_only=active_only)
        
        clinics_response = [ClinicResponse.from_orm(clinic).dict() for clinic in clinics]
        return success_response(data=clinics_response)
    
    except Exception as e:
        return error_response(
            error="SERVER_ERROR",
            message=str(e),
            status_code=500
        )


@clinics_bp.route("/<int:clinic_id>", methods=["PATCH"])
@validate_json
@require_role("admin")
def update_clinic(clinic_id: int):
    """Update clinic information (admin only)."""
    try:
        data = request.get_json()
        update_request = UpdateClinicRequest(**data)
        
        db = next(get_db())
        clinic = ClinicsService.update_clinic(
            db=db,
            clinic_id=clinic_id,
            name=update_request.name,
            address=update_request.address,
            is_active=update_request.is_active,
        )
        
        clinic_response = ClinicResponse.from_orm(clinic)
        return success_response(data=clinic_response.dict(), message="Clinic updated successfully")
    
    except AppException as e:
        return error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            error="INVALID_REQUEST",
            message=str(e),
            status_code=400
        )


@clinics_bp.route("/<int:clinic_id>", methods=["DELETE"])
@require_role("admin")
def delete_clinic(clinic_id: int):
    """Delete a clinic (admin only)."""
    try:
        db = next(get_db())
        ClinicsService.delete_clinic(db, clinic_id)
        
        return success_response(message="Clinic deleted successfully")
    
    except AppException as e:
        return error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code
        )
    except Exception as e:
        return error_response(
            error="SERVER_ERROR",
            message=str(e),
            status_code=500
        )
