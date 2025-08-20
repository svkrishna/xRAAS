"""
Models for the reasoning pipeline.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
from .base import TimestampMixin, SQLModel, SQLField


class ReasoningStage(str, Enum):
    """Stages in the reasoning pipeline."""
    
    LLM_HYPOTHESIS = "LLM Hypothesis"
    RULE_CHECK = "Rule Check"
    KNOWLEDGE_GRAPH = "Knowledge Graph"
    VALIDATION = "Validation"
    FINAL_ANSWER = "Final Answer"


class ConfidenceLevel(str, Enum):
    """Confidence levels for reasoning results."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ReasoningTrace(BaseModel):
    """Individual step in the reasoning trace."""
    
    stage: ReasoningStage
    output: str
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None


class ReasoningRequest(BaseModel):
    """Request model for reasoning endpoint."""
    
    question: str = Field(..., description="The question to reason about")
    context: Optional[str] = Field(None, description="Additional context")
    domain: Optional[str] = Field(None, description="Domain (e.g., 'healthcare', 'finance')")
    confidence_threshold: Optional[float] = Field(0.7, description="Minimum confidence threshold")
    max_steps: Optional[int] = Field(10, description="Maximum reasoning steps")


class ReasoningResponse(BaseModel):
    """Response model for reasoning endpoint."""
    
    answer: str
    reasoning_trace: List[ReasoningTrace]
    confidence: float
    domain: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RuleSet(BaseModel):
    """Model for a rule set."""
    
    name: str
    description: str
    domain: str
    rules: List[Dict[str, Any]]
    version: str = "1.0.0"


class KnowledgeFact(BaseModel):
    """Model for a knowledge fact."""
    
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# Database Models
class ReasoningSession(SQLModel, TimestampMixin, table=True):
    """Database model for reasoning sessions."""
    
    id: Optional[int] = SQLField(default=None, primary_key=True)
    session_id: str = SQLField(unique=True, index=True)
    question: str
    context: Optional[str] = None
    domain: Optional[str] = None
    answer: str
    confidence: float
    reasoning_trace: str  # JSON string
    processing_time: Optional[float] = None
    status: str = "completed"


class RuleSetDB(SQLModel, TimestampMixin, table=True):
    """Database model for rule sets."""
    
    id: Optional[int] = SQLField(default=None, primary_key=True)
    name: str = SQLField(unique=True, index=True)
    description: str
    domain: str
    rules: str  # JSON string
    version: str = "1.0.0"
    is_active: bool = True


class KnowledgeFactDB(SQLModel, TimestampMixin, table=True):
    """Database model for knowledge facts."""
    
    id: Optional[int] = SQLField(default=None, primary_key=True)
    subject: str = SQLField(index=True)
    predicate: str = SQLField(index=True)
    object: str
    confidence: float = 1.0
    source: Optional[str] = None
    metadata: Optional[str] = None  # JSON string
