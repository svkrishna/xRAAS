"""
Core configuration settings for the XReason application.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o"
    
    # Database Configuration
    database_url: str = "sqlite:///./xreason.db"
    
    # Application Configuration
    app_name: str = "XReason API"
    app_version: str = "1.0.0"
    debug: bool = True
    log_level: str = "INFO"
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "XReason"
    
    # CORS Configuration
    backend_cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Reasoning Engine Configuration
    default_confidence_threshold: float = 0.7
    max_reasoning_steps: int = 10
    timeout_seconds: int = 30
    
    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
