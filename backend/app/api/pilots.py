"""
API endpoints for XReason pilots (Legal and Scientific).
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.pilots.legal_compliance import legal_pilot, LegalDomain, LegalAnalysis
from app.pilots.scientific_validation import scientific_pilot, ScientificDomain, ScientificAnalysis
from app.pilots.healthcare_compliance import healthcare_pilot, HealthcareDomain, HealthcareAnalysis
from app.pilots.finance_compliance import finance_pilot, FinanceDomain, FinanceAnalysis
from app.pilots.manufacturing_compliance import manufacturing_pilot, ManufacturingDomain, ManufacturingAnalysis
from app.pilots.cybersecurity_compliance import cybersecurity_pilot, CybersecurityDomain, CybersecurityAnalysis
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


class HealthcareAnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze for healthcare compliance")
    domains: Optional[List[str]] = Field(
        default=["hipaa", "fda", "clinical_trials"],
        description="Healthcare domains to analyze"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for analysis"
    )


class HealthcareAnalysisResponse(BaseModel):
    domain: str
    is_compliant: bool
    confidence: float
    violations: List[Dict[str, Any]]
    recommendations: List[str]
    risk_score: float
    analysis_timestamp: str
    metadata: Dict[str, Any]


class FinanceAnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze for finance compliance")
    domains: Optional[List[str]] = Field(
        default=["banking", "investment", "aml_kyc"],
        description="Finance domains to analyze"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for analysis"
    )


class FinanceAnalysisResponse(BaseModel):
    domain: str
    is_compliant: bool
    confidence: float
    violations: List[Dict[str, Any]]
    recommendations: List[str]
    risk_score: float
    analysis_timestamp: str
    metadata: Dict[str, Any]


class ManufacturingAnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze for manufacturing compliance")
    domains: Optional[List[str]] = Field(
        default=["quality_control", "safety_standards", "environmental"],
        description="Manufacturing domains to analyze"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for analysis"
    )


class ManufacturingAnalysisResponse(BaseModel):
    domain: str
    is_compliant: bool
    confidence: float
    violations: List[Dict[str, Any]]
    recommendations: List[str]
    risk_score: float
    analysis_timestamp: str
    metadata: Dict[str, Any]


class CybersecurityAnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze for cybersecurity compliance")
    domains: Optional[List[str]] = Field(
        default=["security_frameworks", "threat_detection", "incident_response"],
        description="Cybersecurity domains to analyze"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context for analysis"
    )


class CybersecurityAnalysisResponse(BaseModel):
    domain: str
    is_compliant: bool
    confidence: float
    violations: List[Dict[str, Any]]
    recommendations: List[str]
    risk_score: float
    analysis_timestamp: str
    metadata: Dict[str, Any]


class PilotSummaryResponse(BaseModel):
    legal_analyses: Dict[str, LegalAnalysisResponse]
    scientific_analyses: Dict[str, ScientificAnalysisResponse]
    healthcare_analyses: Dict[str, HealthcareAnalysisResponse]
    finance_analyses: Dict[str, FinanceAnalysisResponse]
    manufacturing_analyses: Dict[str, ManufacturingAnalysisResponse]
    cybersecurity_analyses: Dict[str, CybersecurityAnalysisResponse]
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


# Healthcare Compliance Endpoints
@router.post("/healthcare/hipaa", response_model=HealthcareAnalysisResponse)
async def analyze_hipaa_compliance(request: HealthcareAnalysisRequest):
    """Analyze HIPAA compliance of given text."""
    try:
        analysis = await healthcare_pilot.analyze_hipaa_compliance(request.text, request.context)
        
        return HealthcareAnalysisResponse(
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
                    "regulation_reference": v.regulation_reference,
                    "penalty_info": v.penalty_info,
                    "risk_level": v.risk_level
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


@router.post("/healthcare/fda", response_model=HealthcareAnalysisResponse)
async def analyze_fda_compliance(request: HealthcareAnalysisRequest):
    """Analyze FDA compliance of given text."""
    try:
        analysis = await healthcare_pilot.analyze_fda_compliance(request.text, request.context)
        
        return HealthcareAnalysisResponse(
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
                    "regulation_reference": v.regulation_reference,
                    "penalty_info": v.penalty_info,
                    "risk_level": v.risk_level
                }
                for v in analysis.violations
            ],
            recommendations=analysis.recommendations,
            risk_score=analysis.risk_score,
            analysis_timestamp=analysis.analysis_timestamp.isoformat(),
            metadata=analysis.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"FDA analysis failed: {str(e)}")


@router.post("/healthcare/comprehensive", response_model=Dict[str, HealthcareAnalysisResponse])
async def analyze_comprehensive_healthcare(request: HealthcareAnalysisRequest):
    """Analyze comprehensive healthcare compliance."""
    try:
        analyses = await healthcare_pilot.analyze_comprehensive_healthcare(request.text, request.context)
        
        responses = {}
        for domain_name, analysis in analyses.items():
            responses[domain_name] = HealthcareAnalysisResponse(
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
                        "regulation_reference": v.regulation_reference,
                        "penalty_info": v.penalty_info,
                        "risk_level": v.risk_level
                    }
                    for v in analysis.violations
                ],
                recommendations=analysis.recommendations,
                risk_score=analysis.risk_score,
                analysis_timestamp=analysis.analysis_timestamp.isoformat(),
                metadata=analysis.metadata
            )
        
        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Healthcare analysis failed: {str(e)}")


# Finance Compliance Endpoints
@router.post("/finance/banking", response_model=FinanceAnalysisResponse)
async def analyze_banking_compliance(request: FinanceAnalysisRequest):
    """Analyze banking compliance of given text."""
    try:
        analysis = await finance_pilot.analyze_banking_compliance(request.text, request.context)
        
        return FinanceAnalysisResponse(
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
                    "regulation_reference": v.regulation_reference,
                    "penalty_info": v.penalty_info,
                    "risk_level": v.risk_level
                }
                for v in analysis.violations
            ],
            recommendations=analysis.recommendations,
            risk_score=analysis.risk_score,
            analysis_timestamp=analysis.analysis_timestamp.isoformat(),
            metadata=analysis.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Banking analysis failed: {str(e)}")


@router.post("/finance/comprehensive", response_model=Dict[str, FinanceAnalysisResponse])
async def analyze_comprehensive_finance(request: FinanceAnalysisRequest):
    """Analyze comprehensive finance compliance."""
    try:
        analyses = await finance_pilot.analyze_comprehensive_finance(request.text, request.context)
        
        responses = {}
        for domain_name, analysis in analyses.items():
            responses[domain_name] = FinanceAnalysisResponse(
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
                        "regulation_reference": v.regulation_reference,
                        "penalty_info": v.penalty_info,
                        "risk_level": v.risk_level
                    }
                    for v in analysis.violations
                ],
                recommendations=analysis.recommendations,
                risk_score=analysis.risk_score,
                analysis_timestamp=analysis.analysis_timestamp.isoformat(),
                metadata=analysis.metadata
            )
        
        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Finance analysis failed: {str(e)}")


# Manufacturing Compliance Endpoints
@router.post("/manufacturing/quality-control", response_model=ManufacturingAnalysisResponse)
async def analyze_quality_control(request: ManufacturingAnalysisRequest):
    """Analyze quality control compliance of given text."""
    try:
        analysis = await manufacturing_pilot.analyze_quality_control(request.text, request.context)
        
        return ManufacturingAnalysisResponse(
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
                    "standard_reference": v.standard_reference,
                    "penalty_info": v.penalty_info,
                    "risk_level": v.risk_level
                }
                for v in analysis.violations
            ],
            recommendations=analysis.recommendations,
            risk_score=analysis.risk_score,
            analysis_timestamp=analysis.analysis_timestamp.isoformat(),
            metadata=analysis.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quality control analysis failed: {str(e)}")


@router.post("/manufacturing/comprehensive", response_model=Dict[str, ManufacturingAnalysisResponse])
async def analyze_comprehensive_manufacturing(request: ManufacturingAnalysisRequest):
    """Analyze comprehensive manufacturing compliance."""
    try:
        analyses = await manufacturing_pilot.analyze_comprehensive_manufacturing(request.text, request.context)
        
        responses = {}
        for domain_name, analysis in analyses.items():
            responses[domain_name] = ManufacturingAnalysisResponse(
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
                        "standard_reference": v.standard_reference,
                        "penalty_info": v.penalty_info,
                        "risk_level": v.risk_level
                    }
                    for v in analysis.violations
                ],
                recommendations=analysis.recommendations,
                risk_score=analysis.risk_score,
                analysis_timestamp=analysis.analysis_timestamp.isoformat(),
                metadata=analysis.metadata
            )
        
        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Manufacturing analysis failed: {str(e)}")


# Cybersecurity Compliance Endpoints
@router.post("/cybersecurity/security-frameworks", response_model=CybersecurityAnalysisResponse)
async def analyze_security_frameworks(request: CybersecurityAnalysisRequest):
    """Analyze security frameworks compliance of given text."""
    try:
        analysis = await cybersecurity_pilot.analyze_security_frameworks(request.text, request.context)
        
        return CybersecurityAnalysisResponse(
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
                    "framework_reference": v.framework_reference,
                    "penalty_info": v.penalty_info,
                    "risk_level": v.risk_level
                }
                for v in analysis.violations
            ],
            recommendations=analysis.recommendations,
            risk_score=analysis.risk_score,
            analysis_timestamp=analysis.analysis_timestamp.isoformat(),
            metadata=analysis.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Security frameworks analysis failed: {str(e)}")


@router.post("/cybersecurity/comprehensive", response_model=Dict[str, CybersecurityAnalysisResponse])
async def analyze_comprehensive_cybersecurity(request: CybersecurityAnalysisRequest):
    """Analyze comprehensive cybersecurity compliance."""
    try:
        analyses = await cybersecurity_pilot.analyze_comprehensive_cybersecurity(request.text, request.context)
        
        responses = {}
        for domain_name, analysis in analyses.items():
            responses[domain_name] = CybersecurityAnalysisResponse(
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
                        "framework_reference": v.framework_reference,
                        "penalty_info": v.penalty_info,
                        "risk_level": v.risk_level
                    }
                    for v in analysis.violations
                ],
                recommendations=analysis.recommendations,
                risk_score=analysis.risk_score,
                analysis_timestamp=analysis.analysis_timestamp.isoformat(),
                metadata=analysis.metadata
            )
        
        return responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cybersecurity analysis failed: {str(e)}")


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
