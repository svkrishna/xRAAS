"""
Financial Schemas
Pydantic schemas for financial analysis operations.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class FinancialMetricType(str, Enum):
    """Types of financial metrics."""
    DEBT_TO_EQUITY = "debt_to_equity"
    CURRENT_RATIO = "current_ratio"
    QUICK_RATIO = "quick_ratio"
    ROE = "roe"
    ROA = "roa"
    ROI = "roi"
    PROFIT_MARGIN = "profit_margin"
    GROSS_MARGIN = "gross_margin"
    OPERATING_MARGIN = "operating_margin"
    EBITDA_MARGIN = "ebitda_margin"


class RiskLevel(str, Enum):
    """Risk levels for financial analysis."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplianceStatus(str, Enum):
    """Compliance status for financial regulations."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    UNKNOWN = "unknown"


class FinancialData(BaseModel):
    """Financial data for analysis."""
    revenue: Optional[float] = Field(None, description="Total revenue")
    costs: Optional[float] = Field(None, description="Total costs")
    assets: Optional[float] = Field(None, description="Total assets")
    liabilities: Optional[float] = Field(None, description="Total liabilities")
    equity: Optional[float] = Field(None, description="Total equity")
    debt: Optional[float] = Field(None, description="Total debt")
    current_assets: Optional[float] = Field(None, description="Current assets")
    current_liabilities: Optional[float] = Field(None, description="Current liabilities")
    net_income: Optional[float] = Field(None, description="Net income")
    operating_income: Optional[float] = Field(None, description="Operating income")
    ebitda: Optional[float] = Field(None, description="EBITDA")
    cash_flow: Optional[float] = Field(None, description="Cash flow")
    period: Optional[str] = Field(None, description="Financial period (e.g., '2023', 'Q1 2024')")
    currency: str = Field("USD", description="Currency for financial data")


class FinancialMetric(BaseModel):
    """A calculated financial metric."""
    metric_type: FinancialMetricType = Field(..., description="Type of financial metric")
    value: float = Field(..., description="Calculated value")
    formula: str = Field(..., description="Formula used for calculation")
    interpretation: str = Field(..., description="Interpretation of the metric")
    risk_level: RiskLevel = Field(..., description="Risk level associated with this metric")
    benchmark: Optional[float] = Field(None, description="Industry benchmark value")
    is_healthy: bool = Field(..., description="Whether this metric indicates healthy financials")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations based on this metric")


class FinancialAnalysisRequest(BaseModel):
    """Request for financial analysis."""
    company_name: str = Field(..., description="Name of the company")
    financial_data: FinancialData = Field(..., description="Financial data for analysis")
    metrics_to_calculate: List[FinancialMetricType] = Field(default_factory=list, description="Specific metrics to calculate")
    include_risk_assessment: bool = Field(True, description="Whether to include risk assessment")
    include_compliance_check: bool = Field(True, description="Whether to include compliance checks")
    industry: Optional[str] = Field(None, description="Industry for benchmarking")
    analysis_period: Optional[str] = Field(None, description="Period for analysis")


class RiskAssessment(BaseModel):
    """Risk assessment for financial analysis."""
    overall_risk_level: RiskLevel = Field(..., description="Overall risk level")
    risk_score: float = Field(..., description="Risk score (0-100)")
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk factors")
    risk_mitigation: List[str] = Field(default_factory=list, description="Risk mitigation strategies")
    stress_test_results: Dict[str, Any] = Field(default_factory=dict, description="Stress test results")


class ComplianceCheck(BaseModel):
    """Compliance check result."""
    regulation: str = Field(..., description="Regulation being checked")
    status: ComplianceStatus = Field(..., description="Compliance status")
    requirements_met: List[str] = Field(default_factory=list, description="Requirements that are met")
    requirements_missing: List[str] = Field(default_factory=list, description="Requirements that are missing")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for compliance")
    risk_level: RiskLevel = Field(..., description="Risk level for non-compliance")


class FinancialAnalysisResult(BaseModel):
    """Result of financial analysis."""
    analysis_id: str = Field(..., description="Unique analysis identifier")
    company_name: str = Field(..., description="Company name")
    analysis_date: datetime = Field(default_factory=datetime.utcnow, description="When analysis was performed")
    financial_data: FinancialData = Field(..., description="Input financial data")
    calculated_metrics: List[FinancialMetric] = Field(default_factory=list, description="Calculated financial metrics")
    risk_assessment: Optional[RiskAssessment] = Field(None, description="Risk assessment results")
    compliance_checks: List[ComplianceCheck] = Field(default_factory=list, description="Compliance check results")
    summary: str = Field(..., description="Summary of analysis")
    key_findings: List[str] = Field(default_factory=list, description="Key findings from analysis")
    recommendations: List[str] = Field(default_factory=list, description="Overall recommendations")
    confidence_score: float = Field(..., description="Confidence in analysis results (0-1)")
    execution_time_ms: float = Field(..., description="Analysis execution time in milliseconds")


class BatchFinancialAnalysisRequest(BaseModel):
    """Request for batch financial analysis."""
    analyses: List[FinancialAnalysisRequest] = Field(..., description="List of financial analysis requests")
    parallel: bool = Field(True, description="Whether to process analyses in parallel")
    timeout_seconds: int = Field(600, description="Timeout for batch processing")


class BatchFinancialAnalysisResult(BaseModel):
    """Result of batch financial analysis."""
    batch_id: str = Field(..., description="Unique batch identifier")
    results: List[FinancialAnalysisResult] = Field(..., description="Individual analysis results")
    total_analyses: int = Field(..., description="Total number of analyses")
    successful_analyses: int = Field(..., description="Number of successful analyses")
    failed_analyses: int = Field(..., description="Number of failed analyses")
    average_confidence: float = Field(..., description="Average confidence across all results")
    total_execution_time_ms: float = Field(..., description="Total execution time in milliseconds")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When batch was completed")


class FinancialReport(BaseModel):
    """Comprehensive financial report."""
    report_id: str = Field(..., description="Unique report identifier")
    company_name: str = Field(..., description="Company name")
    report_date: datetime = Field(default_factory=datetime.utcnow, description="Report date")
    analysis_results: List[FinancialAnalysisResult] = Field(default_factory=list, description="Analysis results")
    executive_summary: str = Field(..., description="Executive summary")
    detailed_analysis: str = Field(..., description="Detailed analysis")
    charts_and_graphs: List[Dict[str, Any]] = Field(default_factory=list, description="Charts and graphs data")
    appendices: List[Dict[str, Any]] = Field(default_factory=list, description="Additional appendices")
    generated_by: str = Field("XReason Financial Analysis", description="System that generated the report")
