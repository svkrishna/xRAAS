"""
API endpoints for XReason pilots (Legal and Scientific).
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.pilots.legal_compliance import legal_pilot, LegalDomain, LegalAnalysis
from app.pilots.scientific_validation import scientific_pilot, ScientificDomain, ScientificAnalysis
from app.services.metrics_service import metrics_service

router = APIRouter(prefix="/pilots", tags=["pilots"])


# Request/Response Models
class LegalAnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze for legal compliance")
    domains: Optional[List[str]] = Field(
        default=["gdpr", "hipaa", "contract"],
        description="Legal domains to analyze"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for analysis"
    )


class LegalAnalysisResponse(BaseModel):
    domain: str
    is_compliant: bool
    confidence: float
    violations: List[Dict[str, Any]]
    recommendations: List[str]
    risk_score: float
    analysis_timestamp: str
    metadata: Dict[str, Any]


class ScientificAnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze for scientific validity")
    domains: Optional[List[str]] = Field(
        default=["mathematics", "statistics", "methodology"],
        description="Scientific domains to analyze"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for analysis"
    )


class ScientificAnalysisResponse(BaseModel):
    domain: str
    is_valid: bool
    confidence: float
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    validity_score: float
    analysis_timestamp: str
    metadata: Dict[str, Any]


class PilotSummaryResponse(BaseModel):
    legal_analyses: Dict[str, LegalAnalysisResponse]
    scientific_analyses: Dict[str, ScientificAnalysisResponse]
    overall_compliance_score: float
    overall_validity_score: float
    total_issues: int
    total_violations: int


# Legal Compliance Endpoints
@router.post("/legal/gdpr", response_model=LegalAnalysisResponse)
async def analyze_gdpr_compliance(request: LegalAnalysisRequest):
    """Analyze GDPR compliance of given text."""
    try:
        analysis = await legal_pilot.analyze_gdpr_compliance(request.text, request.context)
        
        return LegalAnalysisResponse(
            domain=analysis.domain.value,
            is_compliant=analysis.is_compliant,
            confidence=analysis.confidence,
            violations=[
                {
                    "rule_id": v.rule_id,
                    "rule_name": v.rule_name,
                    "severity": v.severity,
                    "description": v.description,
                    "evidence": v.evidence,
                    "recommendation": v.recommendation,
                    "article_reference": v.article_reference,
                    "penalty_info": v.penalty_info
                }
                for v in analysis.violations
            ],
            recommendations=analysis.recommendations,
            risk_score=analysis.risk_score,
            analysis_timestamp=analysis.analysis_timestamp.isoformat(),
            metadata=analysis.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GDPR analysis failed: {str(e)}")


@router.post("/legal/hipaa", response_model=LegalAnalysisResponse)
async def analyze_hipaa_compliance(request: LegalAnalysisRequest):
    """Analyze HIPAA compliance of given text."""
    try:
        analysis = await legal_pilot.analyze_hipaa_compliance(request.text, request.context)
        
        return LegalAnalysisResponse(
            domain=analysis.domain.value,
            is_compliant=analysis.is_compliant,
            confidence=analysis.confidence,
            violations=[
                {
                    "rule_id": v.rule_id,
                    "rule_name": v.rule_name,
                    "severity": v.severity,
                    "description": v.description,
                    "evidence": v.evidence,
                    "recommendation": v.recommendation,
                    "article_reference": v.article_reference,
                    "penalty_info": v.penalty_info
                }
                for v in analysis.violations
            ],
            recommendations=analysis.recommendations,
            risk_score=analysis.risk_score,
            analysis_timestamp=analysis.analysis_timestamp.isoformat(),
            metadata=analysis.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HIPAA analysis failed: {str(e)}")


@router.post("/legal/contract", response_model=LegalAnalysisResponse)
async def analyze_contract(request: LegalAnalysisRequest):
    """Analyze contract for key provisions and risks."""
    try:
        analysis = await legal_pilot.analyze_contract(request.text, request.context)
        
        return LegalAnalysisResponse(
            domain=analysis.domain.value,
            is_compliant=analysis.is_compliant,
            confidence=analysis.confidence,
            violations=[
                {
                    "rule_id": v.rule_id,
                    "rule_name": v.rule_name,
                    "severity": v.severity,
                    "description": v.description,
                    "evidence": v.evidence,
                    "recommendation": v.recommendation,
                    "article_reference": v.article_reference,
                    "penalty_info": v.penalty_info
                }
                for v in analysis.violations
            ],
            recommendations=analysis.recommendations,
            risk_score=analysis.risk_score,
            analysis_timestamp=analysis.analysis_timestamp.isoformat(),
            metadata=analysis.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Contract analysis failed: {str(e)}")


@router.post("/legal/comprehensive", response_model=Dict[str, LegalAnalysisResponse])
async def analyze_legal_compliance(request: LegalAnalysisRequest):
    """Analyze legal compliance across multiple domains."""
    try:
        # Convert domain strings to enum values
        domain_enums = []
        for domain_str in request.domains:
            try:
                domain_enums.append(LegalDomain(domain_str.lower()))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid legal domain: {domain_str}")
        
        analyses = await legal_pilot.analyze_legal_compliance(request.text, domain_enums)
        
        result = {}
        for domain_name, analysis in analyses.items():
            result[domain_name] = LegalAnalysisResponse(
                domain=analysis.domain.value,
                is_compliant=analysis.is_compliant,
                confidence=analysis.confidence,
                violations=[
                    {
                        "rule_id": v.rule_id,
                        "rule_name": v.rule_name,
                        "severity": v.severity,
                        "description": v.description,
                        "evidence": v.evidence,
                        "recommendation": v.recommendation,
                        "article_reference": v.article_reference,
                        "penalty_info": v.penalty_info
                    }
                    for v in analysis.violations
                ],
                recommendations=analysis.recommendations,
                risk_score=analysis.risk_score,
                analysis_timestamp=analysis.analysis_timestamp.isoformat(),
                metadata=analysis.metadata
            )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Legal analysis failed: {str(e)}")


# Scientific Validation Endpoints
@router.post("/scientific/mathematics", response_model=ScientificAnalysisResponse)
async def analyze_mathematical_consistency(request: ScientificAnalysisRequest):
    """Analyze mathematical consistency in given text."""
    try:
        analysis = await scientific_pilot.analyze_mathematical_consistency(request.text, request.context)
        
        return ScientificAnalysisResponse(
            domain=analysis.domain.value,
            is_valid=analysis.is_valid,
            confidence=analysis.confidence,
            issues=[
                {
                    "issue_id": i.issue_id,
                    "issue_type": i.issue_type,
                    "severity": i.severity,
                    "description": i.description,
                    "evidence": i.evidence,
                    "recommendation": i.recommendation,
                    "formula_reference": i.formula_reference,
                    "statistical_test": i.statistical_test
                }
                for i in analysis.issues
            ],
            recommendations=analysis.recommendations,
            validity_score=analysis.validity_score,
            analysis_timestamp=analysis.analysis_timestamp.isoformat(),
            metadata=analysis.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mathematical analysis failed: {str(e)}")


@router.post("/scientific/statistics", response_model=ScientificAnalysisResponse)
async def analyze_statistical_validity(request: ScientificAnalysisRequest):
    """Analyze statistical validity in given text."""
    try:
        analysis = await scientific_pilot.analyze_statistical_validity(request.text, request.context)
        
        return ScientificAnalysisResponse(
            domain=analysis.domain.value,
            is_valid=analysis.is_valid,
            confidence=analysis.confidence,
            issues=[
                {
                    "issue_id": i.issue_id,
                    "issue_type": i.issue_type,
                    "severity": i.severity,
                    "description": i.description,
                    "evidence": i.evidence,
                    "recommendation": i.recommendation,
                    "formula_reference": i.formula_reference,
                    "statistical_test": i.statistical_test
                }
                for i in analysis.issues
            ],
            recommendations=analysis.recommendations,
            validity_score=analysis.validity_score,
            analysis_timestamp=analysis.analysis_timestamp.isoformat(),
            metadata=analysis.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistical analysis failed: {str(e)}")


@router.post("/scientific/methodology", response_model=ScientificAnalysisResponse)
async def analyze_research_methodology(request: ScientificAnalysisRequest):
    """Analyze research methodology in given text."""
    try:
        analysis = await scientific_pilot.analyze_research_methodology(request.text, request.context)
        
        return ScientificAnalysisResponse(
            domain=analysis.domain.value,
            is_valid=analysis.is_valid,
            confidence=analysis.confidence,
            issues=[
                {
                    "issue_id": i.issue_id,
                    "issue_type": i.issue_type,
                    "severity": i.severity,
                    "description": i.description,
                    "evidence": i.evidence,
                    "recommendation": i.recommendation,
                    "formula_reference": i.formula_reference,
                    "statistical_test": i.statistical_test
                }
                for i in analysis.issues
            ],
            recommendations=analysis.recommendations,
            validity_score=analysis.validity_score,
            analysis_timestamp=analysis.analysis_timestamp.isoformat(),
            metadata=analysis.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Methodology analysis failed: {str(e)}")


@router.post("/scientific/comprehensive", response_model=Dict[str, ScientificAnalysisResponse])
async def analyze_scientific_validity(request: ScientificAnalysisRequest):
    """Analyze scientific validity across multiple domains."""
    try:
        # Convert domain strings to enum values
        domain_enums = []
        for domain_str in request.domains:
            try:
                domain_enums.append(ScientificDomain(domain_str.lower()))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid scientific domain: {domain_str}")
        
        analyses = await scientific_pilot.analyze_scientific_validity(request.text, domain_enums)
        
        result = {}
        for domain_name, analysis in analyses.items():
            result[domain_name] = ScientificAnalysisResponse(
                domain=analysis.domain.value,
                is_valid=analysis.is_valid,
                confidence=analysis.confidence,
                issues=[
                    {
                        "issue_id": i.issue_id,
                        "issue_type": i.issue_type,
                        "severity": i.severity,
                        "description": i.description,
                        "evidence": i.evidence,
                        "recommendation": i.recommendation,
                        "formula_reference": i.formula_reference,
                        "statistical_test": i.statistical_test
                    }
                    for i in analysis.issues
                ],
                recommendations=analysis.recommendations,
                validity_score=analysis.validity_score,
                analysis_timestamp=analysis.analysis_timestamp.isoformat(),
                metadata=analysis.metadata
            )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scientific analysis failed: {str(e)}")


# Combined Analysis Endpoint
@router.post("/comprehensive", response_model=PilotSummaryResponse)
async def comprehensive_analysis(
    legal_request: LegalAnalysisRequest,
    scientific_request: ScientificAnalysisRequest
):
    """Perform comprehensive legal and scientific analysis."""
    try:
        # Perform legal analysis
        legal_domains = [LegalDomain(d.lower()) for d in legal_request.domains]
        legal_analyses = await legal_pilot.analyze_legal_compliance(legal_request.text, legal_domains)
        
        # Perform scientific analysis
        scientific_domains = [ScientificDomain(d.lower()) for d in scientific_request.domains]
        scientific_analyses = await scientific_pilot.analyze_scientific_validity(scientific_request.text, scientific_domains)
        
        # Calculate summary metrics
        total_violations = sum(len(analysis.violations) for analysis in legal_analyses.values())
        total_issues = sum(len(analysis.issues) for analysis in scientific_analyses.values())
        
        overall_compliance_score = 1.0 - (total_violations / (len(legal_analyses) * 5))  # Assume max 5 violations per domain
        overall_validity_score = 1.0 - (total_issues / (len(scientific_analyses) * 5))  # Assume max 5 issues per domain
        
        # Convert to response format
        legal_responses = {}
        for domain_name, analysis in legal_analyses.items():
            legal_responses[domain_name] = LegalAnalysisResponse(
                domain=analysis.domain.value,
                is_compliant=analysis.is_compliant,
                confidence=analysis.confidence,
                violations=[
                    {
                        "rule_id": v.rule_id,
                        "rule_name": v.rule_name,
                        "severity": v.severity,
                        "description": v.description,
                        "evidence": v.evidence,
                        "recommendation": v.recommendation,
                        "article_reference": v.article_reference,
                        "penalty_info": v.penalty_info
                    }
                    for v in analysis.violations
                ],
                recommendations=analysis.recommendations,
                risk_score=analysis.risk_score,
                analysis_timestamp=analysis.analysis_timestamp.isoformat(),
                metadata=analysis.metadata
            )
        
        scientific_responses = {}
        for domain_name, analysis in scientific_analyses.items():
            scientific_responses[domain_name] = ScientificAnalysisResponse(
                domain=analysis.domain.value,
                is_valid=analysis.is_valid,
                confidence=analysis.confidence,
                issues=[
                    {
                        "issue_id": i.issue_id,
                        "issue_type": i.issue_type,
                        "severity": i.severity,
                        "description": i.description,
                        "evidence": i.evidence,
                        "recommendation": i.recommendation,
                        "formula_reference": i.formula_reference,
                        "statistical_test": i.statistical_test
                    }
                    for i in analysis.issues
                ],
                recommendations=analysis.recommendations,
                validity_score=analysis.validity_score,
                analysis_timestamp=analysis.analysis_timestamp.isoformat(),
                metadata=analysis.metadata
            )
        
        return PilotSummaryResponse(
            legal_analyses=legal_responses,
            scientific_analyses=scientific_responses,
            overall_compliance_score=max(0.0, overall_compliance_score),
            overall_validity_score=max(0.0, overall_validity_score),
            total_issues=total_issues,
            total_violations=total_violations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comprehensive analysis failed: {str(e)}")


# Information Endpoints
@router.get("/legal/domains")
async def get_legal_domains():
    """Get available legal analysis domains."""
    return {
        "domains": [
            {"value": domain.value, "name": domain.name}
            for domain in LegalDomain
        ]
    }


@router.get("/scientific/domains")
async def get_scientific_domains():
    """Get available scientific analysis domains."""
    return {
        "domains": [
            {"value": domain.value, "name": domain.name}
            for domain in ScientificDomain
        ]
    }


@router.get("/legal/rules")
async def get_legal_rules():
    """Get information about legal compliance rules."""
    return {
        "gdpr_rules": legal_pilot.gdpr_rules,
        "hipaa_rules": legal_pilot.hipaa_rules,
        "contract_rules": legal_pilot.contract_rules,
        "privacy_rules": legal_pilot.privacy_rules
    }


@router.get("/scientific/rules")
async def get_scientific_rules():
    """Get information about scientific validation rules."""
    return {
        "math_rules": scientific_pilot.math_rules,
        "statistical_rules": scientific_pilot.statistical_rules,
        "research_rules": scientific_pilot.research_rules,
        "methodology_rules": scientific_pilot.methodology_rules
    }
