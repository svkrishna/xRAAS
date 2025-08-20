"""
Base models and common functionality.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField


class TimestampMixin:
    """Mixin for timestamp fields."""
    
    created_at: datetime = SQLField(default_factory=datetime.utcnow)
    updated_at: datetime = SQLField(default_factory=datetime.utcnow)


class BaseResponse(BaseModel):
    """Base response model."""
    
    success: bool = True
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None
