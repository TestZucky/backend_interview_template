"""Auth service (business logic)."""
from typing import Optional
from sqlalchemy.orm import Session

from app.features.auth.model import User
from app.core.auth import hash_password, verify_password, create_access_token
from app.core.permissions import Role
from app.shared.exceptions import ValidationError, ConflictError, UnauthorizedError


class AuthService:
    """Authentication service."""
    
    @staticmethod
    def signup(db: Session, name: str, email: str, password: str, role: str = "member") -> User:
        """Register a new user."""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ConflictError(f"User with email {email} already exists")
        
        # Create new user
        hashed_password = hash_password(password)
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def login(db: Session, email: str, password: str) -> tuple[User, str]:
        """Authenticate user and return token."""
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.password):
            raise UnauthorizedError("Invalid email or password")
        
        # Create token
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        )
        
        return user, access_token
