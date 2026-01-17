"""Clinics service (business logic)."""
from typing import Optional
from sqlalchemy.orm import Session

from app.features.clinics.model import Clinic
from app.shared.exceptions import NotFoundError


class ClinicsService:
    """Clinics management service."""
    
    @staticmethod
    def get_clinic(db: Session, clinic_id: int) -> Clinic:
        """Get clinic by ID."""
        clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
        if not clinic:
            raise NotFoundError(f"Clinic {clinic_id} not found")
        return clinic
    
    @staticmethod
    def list_clinics(db: Session, active_only: bool = False) -> list[Clinic]:
        """List all clinics."""
        query = db.query(Clinic)
        if active_only:
            query = query.filter(Clinic.is_active == True)
        return query.all()
    
    @staticmethod
    def create_clinic(db: Session, name: str, address: str) -> Clinic:
        """Create a new clinic (admin only)."""
        new_clinic = Clinic(name=name, address=address, is_active=True)
        
        db.add(new_clinic)
        db.commit()
        db.refresh(new_clinic)
        
        return new_clinic
    
    @staticmethod
    def update_clinic(
        db: Session,
        clinic_id: int,
        name: Optional[str] = None,
        address: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> Clinic:
        """Update clinic information (admin only)."""
        clinic = ClinicsService.get_clinic(db, clinic_id)
        
        if name:
            clinic.name = name
        if address:
            clinic.address = address
        if is_active is not None:
            clinic.is_active = is_active
        
        db.commit()
        db.refresh(clinic)
        
        return clinic
    
    @staticmethod
    def delete_clinic(db: Session, clinic_id: int) -> None:
        """Delete a clinic (admin only)."""
        clinic = ClinicsService.get_clinic(db, clinic_id)
        db.delete(clinic)
        db.commit()
