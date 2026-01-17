"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import get_config

config = get_config()

# Create engine
engine = create_engine(
    config.DATABASE_URL,
    echo=config.SQL_ECHO,
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# ============================================================================
# Import all models here to register them with Base.metadata
# This ensures Alembic can detect all tables when generating migrations
# ============================================================================
from app.features.auth.model import User  # noqa: F401, E402
from app.features.clinics.model import Clinic  # noqa: F401, E402

# When adding new features with models, import them here:
# from app.features.yourfeature.model import YourModel  # noqa: F401, E402
# ============================================================================


def get_db():
    """Dependency for getting DB session in routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
