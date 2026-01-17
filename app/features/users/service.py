"""Users service (business logic)."""
from typing import Optional
from sqlalchemy.orm import Session

from app.features.auth.model import User
from app.core.auth import hash_password
from app.core.permissions import Role
from app.shared.exceptions import NotFoundError, ForbiddenError


class UsersService:
    """Users management service."""
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """Get user by ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError(f"User {user_id} not found")
        return user
    
    @staticmethod
    def list_users(db: Session) -> list[User]:
        """List all users (admin only)."""
        return db.query(User).all()
    
    @staticmethod
    def create_user(db: Session, name: str, email: str, password: str, role: str = "member") -> User:
        """Create a new user (admin only)."""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            from app.shared.exceptions import ConflictError
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
    def update_user(db: Session, user_id: int, name: Optional[str] = None, role: Optional[str] = None) -> User:
        """Update user information (admin only)."""
        user = UsersService.get_user(db, user_id)
        
        if name:
            user.name = name
        if role:
            user.role = role
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        """Delete a user (admin only)."""
        user = UsersService.get_user(db, user_id)
        db.delete(user)
        db.commit()
