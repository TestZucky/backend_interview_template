"""Application configuration."""
import os
from functools import lru_cache


class Config:
    """Base configuration."""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./test.db"
    )
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "False").lower() == "true"

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # App
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENVIRONMENT = "development"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    ENVIRONMENT = "production"


class TestingConfig(Config):
    """Testing configuration."""
    DATABASE_URL = "sqlite:///:memory:"
    DEBUG = True
    ENVIRONMENT = "testing"


@lru_cache()
def get_config() -> Config:
    """Get configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()
