"""
Extensible Ruleset Models for multi-domain reasoning.
"""

from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, validator
from sqlmodel import SQLModel, Field as SQLField
from datetime import datetime


class RuleType(str, Enum):
    """Types of rules that can be defined."""
    PROLOG = "prolog"
    PYTHON = "python"
    REGEX = "regex"
    KEYWORD = "keyword"
    MATH = "math"
    LOGIC = "logic"


class RuleSeverity(str, Enum):
    """Severity levels for rule violations."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class RuleCondition(BaseModel):
    """Condition for when a rule should be applied."""
    field: str = Field(..., description="Field to check (e.g., 'question', 'hypothesis', 'domain')")
    operator: str = Field(..., description="Comparison operator (e.g., 'contains', 'equals', 'regex')")
    value: Any = Field(..., description="Value to compare against")
    case_sensitive: bool = Field(default=False, description="Whether comparison is case sensitive")


class RuleDefinition(BaseModel):
    """Definition of a single rule."""
    id: str = Field(..., description="Unique rule identifier")
    name: str = Field(..., description="Human-readable rule name")
    description: str = Field(..., description="Rule description")
    type: RuleType = Field(..., description="Type of rule")
    severity: RuleSeverity = Field(default=RuleSeverity.WARNING, description="Severity level")
    
    # Rule content
    content: str = Field(..., description="Rule content (Prolog code, Python function, regex pattern, etc.)")
    
    # Conditions for when to apply this rule
    conditions: Optional[List[RuleCondition]] = Field(default=None, description="Conditions for rule application")
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    version: str = Field(default="1.0.0", description="Rule version")
    author: Optional[str] = Field(default=None, description="Rule author")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    
    # Validation
    enabled: bool = Field(default=True, description="Whether rule is enabled")
    weight: float = Field(default=1.0, ge=0.0, le=10.0, description="Rule weight for confidence calculation")


class RulesetDefinition(BaseModel):
    """Definition of a complete ruleset."""
    id: str = Field(..., description="Unique ruleset identifier")
    name: str = Field(..., description="Human-readable ruleset name")
    description: str = Field(..., description="Ruleset description")
    domain: str = Field(..., description="Domain this ruleset applies to (e.g., 'healthcare', 'finance', 'legal')")
    version: str = Field(default="1.0.0", description="Ruleset version")
    
    # Rules in this ruleset
    rules: List[RuleDefinition] = Field(..., description="List of rules in this ruleset")
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    author: Optional[str] = Field(default=None, description="Ruleset author")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    # Configuration
    enabled: bool = Field(default=True, description="Whether ruleset is enabled")
    priority: int = Field(default=0, description="Priority for ruleset selection (higher = more important)")
    
    # Validation
    @validator('rules')
    def validate_rules(cls, v):
        if not v:
            raise ValueError("Ruleset must contain at least one rule")
        return v


# Database Models
class RulesetDB(SQLModel, table=True):
    """Database model for storing rulesets."""
    __tablename__ = "rulesets"
    
    id: str = SQLField(primary_key=True, index=True)
    name: str = SQLField(index=True)
    description: str
    domain: str = SQLField(index=True)
    version: str
    content: str = SQLField(description="JSON serialized ruleset definition")
    tags: str = SQLField(description="Comma-separated tags")
    author: Optional[str] = None
    enabled: bool = SQLField(default=True, index=True)
    priority: int = SQLField(default=0, index=True)
    created_at: datetime = SQLField(default_factory=datetime.utcnow)
    updated_at: datetime = SQLField(default_factory=datetime.utcnow)
    
    # Tenant isolation (for multi-tenant support)
    tenant_id: Optional[str] = SQLField(default=None, index=True)


class RuleExecutionLog(SQLModel, table=True):
    """Database model for logging rule executions."""
    __tablename__ = "rule_execution_logs"
    
    id: Optional[int] = SQLField(default=None, primary_key=True)
    ruleset_id: str = SQLField(foreign_key="rulesets.id", index=True)
    rule_id: str = SQLField(index=True)
    reasoning_session_id: str = SQLField(index=True)
    
    # Execution details
    input_data: str = SQLField(description="JSON serialized input data")
    output_data: str = SQLField(description="JSON serialized output data")
    execution_time_ms: float = SQLField(description="Execution time in milliseconds")
    success: bool = SQLField(index=True)
    error_message: Optional[str] = None
    
    # Metadata
    created_at: datetime = SQLField(default_factory=datetime.utcnow, index=True)
    tenant_id: Optional[str] = SQLField(default=None, index=True)


# Response Models
class RuleExecutionResult(BaseModel):
    """Result of executing a single rule."""
    rule_id: str
    rule_name: str
    passed: bool
    confidence: float = Field(ge=0.0, le=1.0)
    output: Dict[str, Any]
    execution_time_ms: float
    error_message: Optional[str] = None


class RulesetExecutionResult(BaseModel):
    """Result of executing a complete ruleset."""
    ruleset_id: str
    ruleset_name: str
    domain: str
    total_rules: int
    passed_rules: int
    failed_rules: int
    overall_confidence: float = Field(ge=0.0, le=1.0)
    rule_results: List[RuleExecutionResult]
    execution_time_ms: float
    errors: List[str] = Field(default_factory=list)


class RulesetValidationResult(BaseModel):
    """Result of validating a ruleset definition."""
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    rule_count: int
    estimated_complexity: str = Field(description="Estimated computational complexity")
