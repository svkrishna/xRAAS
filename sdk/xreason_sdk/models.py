"""
XReason SDK Models
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ReasoningTrace(BaseModel):
    """Represents a step in the reasoning process."""
    stage: str = Field(..., description="Stage of reasoning")
    output: str = Field(..., description="Output from this stage")
    confidence: Optional[float] = Field(None, description="Confidence score for this stage")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ReasoningRequest(BaseModel):
    """Request model for reasoning API."""
    question: str = Field(..., description="The question to reason about")
    context: Optional[str] = Field(None, description="Additional context for reasoning")
    domain: Optional[str] = Field(None, description="Domain for reasoning")
    ruleset_id: Optional[str] = Field(None, description="Specific ruleset to use")


class ReasoningResponse(BaseModel):
    """Response model for reasoning API."""
    answer: str = Field(..., description="The reasoned answer")
    confidence: float = Field(..., description="Overall confidence score")
    reasoning_trace: List[ReasoningTrace] = Field(..., description="Step-by-step reasoning trace")
    session_id: str = Field(..., description="Session identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


# Legal Analysis Models
class LegalAnalysisRequest(BaseModel):
    """Request model for legal analysis."""
    text: str = Field(..., description="Text to analyze for legal compliance")
    domains: Optional[List[str]] = Field(
        default=["gdpr", "hipaa", "contract"],
        description="Legal domains to analyze"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for analysis"
    )


class LegalViolation(BaseModel):
    """Represents a legal violation found in analysis."""
    rule_id: str = Field(..., description="Rule identifier")
    rule_name: str = Field(..., description="Human-readable rule name")
    severity: str = Field(..., description="Severity level")
    description: str = Field(..., description="Violation description")
    evidence: str = Field(..., description="Evidence of violation")
    recommendation: str = Field(..., description="Recommendation to fix")
    article_reference: Optional[str] = Field(None, description="Legal article reference")
    penalty_info: Optional[str] = Field(None, description="Penalty information")


class LegalAnalysisResponse(BaseModel):
    """Response model for legal analysis."""
    domain: str = Field(..., description="Legal domain analyzed")
    is_compliant: bool = Field(..., description="Whether the text is compliant")
    confidence: float = Field(..., description="Analysis confidence score")
    violations: List[LegalViolation] = Field(..., description="List of violations found")
    recommendations: List[str] = Field(..., description="List of recommendations")
    risk_score: float = Field(..., description="Overall risk score")
    analysis_timestamp: str = Field(..., description="Analysis timestamp")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata")


# Scientific Analysis Models
class ScientificAnalysisRequest(BaseModel):
    """Request model for scientific analysis."""
    text: str = Field(..., description="Text to analyze for scientific validity")
    domains: Optional[List[str]] = Field(
        default=["mathematics", "statistics", "methodology"],
        description="Scientific domains to analyze"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for analysis"
    )


class ScientificIssue(BaseModel):
    """Represents a scientific issue found in analysis."""
    issue_id: str = Field(..., description="Issue identifier")
    issue_type: str = Field(..., description="Type of issue")
    severity: str = Field(..., description="Severity level")
    description: str = Field(..., description="Issue description")
    evidence: str = Field(..., description="Evidence of issue")
    recommendation: str = Field(..., description="Recommendation to fix")
    formula_reference: Optional[str] = Field(None, description="Formula reference")
    statistical_test: Optional[str] = Field(None, description="Statistical test reference")


class ScientificAnalysisResponse(BaseModel):
    """Response model for scientific analysis."""
    domain: str = Field(..., description="Scientific domain analyzed")
    is_valid: bool = Field(..., description="Whether the text is scientifically valid")
    confidence: float = Field(..., description="Analysis confidence score")
    issues: List[ScientificIssue] = Field(..., description="List of issues found")
    recommendations: List[str] = Field(..., description="List of recommendations")
    validity_score: float = Field(..., description="Overall validity score")
    analysis_timestamp: str = Field(..., description="Analysis timestamp")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata")


# Combined Analysis Models
class PilotSummaryResponse(BaseModel):
    """Response model for comprehensive pilot analysis."""
    legal_analyses: Dict[str, LegalAnalysisResponse] = Field(..., description="Legal analysis results")
    scientific_analyses: Dict[str, ScientificAnalysisResponse] = Field(..., description="Scientific analysis results")
    overall_compliance_score: float = Field(..., description="Overall compliance score")
    overall_validity_score: float = Field(..., description="Overall validity score")
    total_issues: int = Field(..., description="Total number of issues found")
    total_violations: int = Field(..., description="Total number of violations found")
