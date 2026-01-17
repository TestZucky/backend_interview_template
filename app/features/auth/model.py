"""Auth models."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum

from app.db import Base
from app.core.permissions import Role


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLEnum(Role), default=Role.MEMBER, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
