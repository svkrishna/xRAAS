"""
Reasoning Schemas
Pydantic schemas for reasoning operations.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class ReasoningType(str, Enum):
    """Types of reasoning operations."""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"


class ConfidenceLevel(str, Enum):
    """Confidence levels for reasoning results."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "uncertain"


class ReasoningRequest(BaseModel):
    """Request for reasoning operation."""
    question: str = Field(..., description="The question to reason about")
    context: Optional[str] = Field(None, description="Additional context")
    reasoning_type: ReasoningType = Field(ReasoningType.DEDUCTIVE, description="Type of reasoning to apply")
    domain: Optional[str] = Field(None, description="Domain-specific context")
    max_steps: int = Field(10, description="Maximum reasoning steps")
    confidence_threshold: float = Field(0.7, description="Minimum confidence threshold")


class ReasoningStep(BaseModel):
    """A single reasoning step."""
    step_id: str = Field(..., description="Unique step identifier")
    step_number: int = Field(..., description="Step number in sequence")
    reasoning_type: ReasoningType = Field(..., description="Type of reasoning used")
    premise: str = Field(..., description="Premise or input for this step")
    conclusion: str = Field(..., description="Conclusion from this step")
    confidence: float = Field(..., description="Confidence in this step (0-1)")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    rules_applied: List[str] = Field(default_factory=list, description="Rules applied in this step")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When this step was executed")


class ReasoningResult(BaseModel):
    """Result of a reasoning operation."""
    request_id: str = Field(..., description="Unique request identifier")
    question: str = Field(..., description="Original question")
    answer: str = Field(..., description="Final answer")
    confidence: float = Field(..., description="Overall confidence (0-1)")
    confidence_level: ConfidenceLevel = Field(..., description="Confidence level category")
    reasoning_steps: List[ReasoningStep] = Field(default_factory=list, description="Detailed reasoning steps")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    rules_applied: List[str] = Field(default_factory=list, description="Rules that were applied")
    execution_time_ms: float = Field(..., description="Total execution time in milliseconds")
    domain: Optional[str] = Field(None, description="Domain context used")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When result was created")


class KnowledgeFact(BaseModel):
    """A knowledge fact for reasoning."""
    fact_id: str = Field(..., description="Unique fact identifier")
    statement: str = Field(..., description="The factual statement")
    source: Optional[str] = Field(None, description="Source of this fact")
    confidence: float = Field(1.0, description="Confidence in this fact (0-1)")
    domain: Optional[str] = Field(None, description="Domain this fact belongs to")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When fact was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="When fact was last updated")


class ValidationResult(BaseModel):
    """Result of a validation operation."""
    validation_id: str = Field(..., description="Unique validation identifier")
    statement: str = Field(..., description="Statement being validated")
    is_valid: bool = Field(..., description="Whether the statement is valid")
    confidence: float = Field(..., description="Confidence in validation (0-1)")
    reasoning: str = Field(..., description="Reasoning for validation result")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    contradictions: List[str] = Field(default_factory=list, description="Contradictions found")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When validation was performed")


class BatchReasoningRequest(BaseModel):
    """Request for batch reasoning operations."""
    requests: List[ReasoningRequest] = Field(..., description="List of reasoning requests")
    parallel: bool = Field(True, description="Whether to process requests in parallel")
    timeout_seconds: int = Field(300, description="Timeout for batch processing")


class BatchReasoningResult(BaseModel):
    """Result of batch reasoning operations."""
    batch_id: str = Field(..., description="Unique batch identifier")
    results: List[ReasoningResult] = Field(..., description="Individual reasoning results")
    total_requests: int = Field(..., description="Total number of requests")
    successful_requests: int = Field(..., description="Number of successful requests")
    failed_requests: int = Field(..., description="Number of failed requests")
    average_confidence: float = Field(..., description="Average confidence across all results")
    total_execution_time_ms: float = Field(..., description="Total execution time in milliseconds")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When batch was completed")
