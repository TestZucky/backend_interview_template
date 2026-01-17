"""Clinics model."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.db import Base


class Clinic(Base):
    """Clinic model."""
    
    __tablename__ = "clinics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Clinic(id={self.id}, name={self.name}, is_active={self.is_active})>"
