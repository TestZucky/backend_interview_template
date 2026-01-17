"""Test configuration and fixtures."""
import pytest
from app.main import create_app
from app.db import Base, engine, SessionLocal
from app.core.auth import create_access_token
from app.features.auth.model import User
from app.core.permissions import Role
from app.core.auth import hash_password


@pytest.fixture
def app():
    """Create test application."""
    app = create_app()
    app.config['TESTING'] = True
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    yield app
    
    # Clean up
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def db():
    """Create test database session."""
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    user = User(
        name="Admin User",
        email="admin@example.com",
        password=hash_password("admin123"),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def member_user(db):
    """Create a member user."""
    user = User(
        name="Member User",
        email="member@example.com",
        password=hash_password("member123"),
        role="member",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_token(admin_user):
    """Create admin token."""
    return create_access_token(
        data={"sub": str(admin_user.id), "email": admin_user.email, "role": admin_user.role}
    )


@pytest.fixture
def member_token(member_user):
    """Create member token."""
    return create_access_token(
        data={"sub": str(member_user.id), "email": member_user.email, "role": member_user.role}
    )


@pytest.fixture
def admin_user_id(admin_user):
    """Get admin user ID."""
    return admin_user.id


@pytest.fixture
def member_user_id(member_user):
    """Get member user ID."""
    return member_user.id
