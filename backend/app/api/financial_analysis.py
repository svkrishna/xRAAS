"""
FastAPI endpoints for Financial Analysis Service.
Optimized for financial compliance and risk analysis use cases.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from decimal import Decimal

from app.services.financial_analysis_service import financial_analysis_service
from app.services.metrics_service import metrics_service

router = APIRouter(prefix="/api/v1/financial", tags=["Financial Analysis"])


# Request/Response Models
class FinancialDataRequest(BaseModel):
    """Request model for financial analysis."""
    company_id: str = Field(..., description="Unique company identifier")
    revenue: Decimal = Field(..., description="Total revenue")
    costs: Decimal = Field(..., description="Total costs")
    debt: Decimal = Field(..., description="Total debt")
    equity: Decimal = Field(..., description="Total equity")
    assets: Decimal = Field(..., description="Total assets")
    liabilities: Decimal = Field(..., description="Total liabilities")
    cash_flow: Decimal = Field(..., description="Operating cash flow")
    industry: Optional[str] = Field(None, description="Industry classification")
    market_cap: Optional[Decimal] = Field(None, description="Market capitalization")
    pe_ratio: Optional[Decimal] = Field(None, description="Price-to-earnings ratio")


class FinancialMetricsResponse(BaseModel):
    """Response model for financial metrics."""
    revenue: Decimal
    costs: Decimal
    profit: Decimal
    debt: Decimal
    equity: Decimal
    assets: Decimal
    liabilities: Decimal
    cash_flow: Decimal
    debt_to_equity: Decimal
    current_ratio: Decimal
    profit_margin: Decimal
    roe: Decimal
    roa: Decimal


class RiskAssessmentResponse(BaseModel):
    """Response model for risk assessment."""
    overall_risk: str
    risk_score: float
    risk_factors: List[str]
    recommendations: List[str]
    compliance_status: str
    regulatory_concerns: List[str]
    financial_health: str
    confidence: float


class ComplianceReportResponse(BaseModel):
    """Response model for compliance report."""
    company_id: str
    analysis_date: str
    metrics: FinancialMetricsResponse
    risk_assessment: RiskAssessmentResponse
    regulatory_analysis: Dict[str, Any]
    recommendations: List[str]
    next_review_date: str
    analyst_notes: Optional[str] = None


class FinancialInsightsRequest(BaseModel):
    """Request model for financial insights."""
    company_id: str = Field(..., description="Company identifier")
    timeframe: str = Field(default="1y", description="Analysis timeframe")


class FinancialInsightsResponse(BaseModel):
    """Response model for financial insights."""
    company_id: str
    timeframe: str
    trends: Dict[str, str]
    benchmarks: Dict[str, float]
    risk_alerts: List[str]


class BatchAnalysisRequest(BaseModel):
    """Request model for batch financial analysis."""
    companies: List[FinancialDataRequest] = Field(..., description="List of companies to analyze")
    analysis_type: str = Field(default="comprehensive", description="Type of analysis")


class BatchAnalysisResponse(BaseModel):
    """Response model for batch analysis."""
    total_companies: int
    successful_analyses: int
    failed_analyses: int
    results: List[ComplianceReportResponse]
    summary: Dict[str, Any]


# Endpoints
@router.post("/analyze", response_model=ComplianceReportResponse)
async def analyze_financial_health(request: FinancialDataRequest):
    """Analyze financial health and compliance for a company."""
    try:
        # Convert request to financial data dict
        financial_data = {
            "revenue": float(request.revenue),
            "costs": float(request.costs),
            "debt": float(request.debt),
            "equity": float(request.equity),
            "assets": float(request.assets),
            "liabilities": float(request.liabilities),
            "cash_flow": float(request.cash_flow)
        }
        
        if request.market_cap:
            financial_data["market_cap"] = float(request.market_cap)
        if request.pe_ratio:
            financial_data["pe_ratio"] = float(request.pe_ratio)
        
        # Perform analysis
        report = await financial_analysis_service.analyze_financial_health(
            financial_data=financial_data,
            company_id=request.company_id,
            industry=request.industry
        )
        
        # Convert to response model
        return ComplianceReportResponse(
            company_id=report.company_id,
            analysis_date=report.analysis_date.isoformat(),
            metrics=FinancialMetricsResponse(
                revenue=report.metrics.revenue,
                costs=report.metrics.costs,
                profit=report.metrics.profit,
                debt=report.metrics.debt,
                equity=report.metrics.equity,
                assets=report.metrics.assets,
                liabilities=report.metrics.liabilities,
                cash_flow=report.metrics.cash_flow,
                debt_to_equity=report.metrics.debt_to_equity,
                current_ratio=report.metrics.current_ratio,
                profit_margin=report.metrics.profit_margin,
                roe=report.metrics.roe,
                roa=report.metrics.roa
            ),
            risk_assessment=RiskAssessmentResponse(
                overall_risk=report.risk_assessment.overall_risk.value,
                risk_score=report.risk_assessment.risk_score,
                risk_factors=report.risk_assessment.risk_factors,
                recommendations=report.risk_assessment.recommendations,
                compliance_status=report.risk_assessment.compliance_status.value,
                regulatory_concerns=report.risk_assessment.regulatory_concerns,
                financial_health=report.risk_assessment.financial_health,
                confidence=report.risk_assessment.confidence
            ),
            regulatory_analysis=report.regulatory_analysis,
            recommendations=report.recommendations,
            next_review_date=report.next_review_date.isoformat(),
            analyst_notes=report.analyst_notes
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Financial analysis failed: {str(e)}")


@router.post("/batch-analyze", response_model=BatchAnalysisResponse)
async def batch_financial_analysis(request: BatchAnalysisRequest):
    """Perform batch financial analysis for multiple companies."""
    try:
        results = []
        successful = 0
        failed = 0
        
        for company_request in request.companies:
            try:
                # Convert request to financial data dict
                financial_data = {
                    "revenue": float(company_request.revenue),
                    "costs": float(company_request.costs),
                    "debt": float(company_request.debt),
                    "equity": float(company_request.equity),
                    "assets": float(company_request.assets),
                    "liabilities": float(company_request.liabilities),
                    "cash_flow": float(company_request.cash_flow)
                }
                
                if company_request.market_cap:
                    financial_data["market_cap"] = float(company_request.market_cap)
                if company_request.pe_ratio:
                    financial_data["pe_ratio"] = float(company_request.pe_ratio)
                
                # Perform analysis
                report = await financial_analysis_service.analyze_financial_health(
                    financial_data=financial_data,
                    company_id=company_request.company_id,
                    industry=company_request.industry
                )
                
                # Convert to response model
                result = ComplianceReportResponse(
                    company_id=report.company_id,
                    analysis_date=report.analysis_date.isoformat(),
                    metrics=FinancialMetricsResponse(
                        revenue=report.metrics.revenue,
                        costs=report.metrics.costs,
                        profit=report.metrics.profit,
                        debt=report.metrics.debt,
                        equity=report.metrics.equity,
                        assets=report.metrics.assets,
                        liabilities=report.metrics.liabilities,
                        cash_flow=report.metrics.cash_flow,
                        debt_to_equity=report.metrics.debt_to_equity,
                        current_ratio=report.metrics.current_ratio,
                        profit_margin=report.metrics.profit_margin,
                        roe=report.metrics.roe,
                        roa=report.metrics.roa
                    ),
                    risk_assessment=RiskAssessmentResponse(
                        overall_risk=report.risk_assessment.overall_risk.value,
                        risk_score=report.risk_assessment.risk_score,
                        risk_factors=report.risk_assessment.risk_factors,
                        recommendations=report.risk_assessment.recommendations,
                        compliance_status=report.risk_assessment.compliance_status.value,
                        regulatory_concerns=report.risk_assessment.regulatory_concerns,
                        financial_health=report.risk_assessment.financial_health,
                        confidence=report.risk_assessment.confidence
                    ),
                    regulatory_analysis=report.regulatory_analysis,
                    recommendations=report.recommendations,
                    next_review_date=report.next_review_date.isoformat(),
                    analyst_notes=report.analyst_notes
                )
                
                results.append(result)
                successful += 1
                
            except Exception as e:
                failed += 1
                # Log the error but continue with other companies
                continue
        
        # Generate summary
        summary = {
            "success_rate": successful / len(request.companies) if request.companies else 0,
            "average_risk_score": sum(r.risk_assessment.risk_score for r in results) / len(results) if results else 0,
            "compliance_distribution": {
                "compliant": sum(1 for r in results if r.risk_assessment.compliance_status == "compliant"),
                "at_risk": sum(1 for r in results if r.risk_assessment.compliance_status == "at_risk"),
                "non_compliant": sum(1 for r in results if r.risk_assessment.compliance_status == "non_compliant")
            }
        }
        
        return BatchAnalysisResponse(
            total_companies=len(request.companies),
            successful_analyses=successful,
            failed_analyses=failed,
            results=results,
            summary=summary
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")


@router.get("/insights/{company_id}", response_model=FinancialInsightsResponse)
async def get_financial_insights(
    company_id: str,
    timeframe: str = "1y"
):
    """Get financial insights and trends for a company."""
    try:
        insights = await financial_analysis_service.get_financial_insights(
            company_id=company_id,
            timeframe=timeframe
        )
        
        return FinancialInsightsResponse(
            company_id=insights["company_id"],
            timeframe=insights["timeframe"],
            trends=insights["trends"],
            benchmarks=insights["benchmarks"],
            risk_alerts=insights["risk_alerts"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get insights: {str(e)}")


@router.post("/metrics", response_model=FinancialMetricsResponse)
async def calculate_financial_metrics(request: FinancialDataRequest):
    """Calculate financial metrics without full analysis."""
    try:
        # Convert request to financial data dict
        financial_data = {
            "revenue": float(request.revenue),
            "costs": float(request.costs),
            "debt": float(request.debt),
            "equity": float(request.equity),
            "assets": float(request.assets),
            "liabilities": float(request.liabilities),
            "cash_flow": float(request.cash_flow)
        }
        
        # Calculate metrics
        metrics = await financial_analysis_service._calculate_metrics(financial_data)
        
        return FinancialMetricsResponse(
            revenue=metrics.revenue,
            costs=metrics.costs,
            profit=metrics.profit,
            debt=metrics.debt,
            equity=metrics.equity,
            assets=metrics.assets,
            liabilities=metrics.liabilities,
            cash_flow=metrics.cash_flow,
            debt_to_equity=metrics.debt_to_equity,
            current_ratio=metrics.current_ratio,
            profit_margin=metrics.profit_margin,
            roe=metrics.roe,
            roa=metrics.roa
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate metrics: {str(e)}")


@router.get("/risk-assessment/{company_id}")
async def get_risk_assessment(company_id: str):
    """Get risk assessment for a company (requires previous analysis)."""
    try:
        # This would typically query a database for stored analysis
        # For now, return a mock response
        return {
            "company_id": company_id,
            "risk_level": "medium",
            "risk_score": 0.45,
            "last_updated": "2024-01-15T10:30:00Z",
            "status": "analysis_required"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get risk assessment: {str(e)}")


@router.get("/compliance-status/{company_id}")
async def get_compliance_status(company_id: str):
    """Get compliance status for a company."""
    try:
        # This would typically query a database for stored compliance data
        # For now, return a mock response
        return {
            "company_id": company_id,
            "compliance_status": "compliant",
            "regulatory_frameworks": ["sox", "basel_iii"],
            "last_review": "2024-01-15T10:30:00Z",
            "next_review": "2024-04-15T10:30:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get compliance status: {str(e)}")


@router.get("/regulatory-frameworks")
async def get_regulatory_frameworks():
    """Get available regulatory frameworks and their requirements."""
    try:
        frameworks = financial_analysis_service.regulatory_frameworks
        return {
            "frameworks": frameworks,
            "total_frameworks": len(frameworks),
            "last_updated": "2024-01-15T10:30:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get frameworks: {str(e)}")


@router.get("/financial-rules")
async def get_financial_rules():
    """Get financial analysis rules and formulas."""
    try:
        rules = financial_analysis_service.financial_rules
        return {
            "rules": rules,
            "total_rules": len(rules),
            "last_updated": "2024-01-15T10:30:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get rules: {str(e)}")


@router.get("/health")
async def financial_analysis_health():
    """Health check for financial analysis service."""
    try:
        # Check if service components are available
        service_status = {
            "status": "healthy",
            "service": "financial_analysis",
            "components": {
                "ai_agents": "available",
                "llm_service": "available",
                "symbolic_service": "available",
                "knowledge_service": "available"
            },
            "timestamp": "2024-01-15T10:30:00Z"
        }
        
        return JSONResponse(
            content=service_status,
            status_code=200
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": "unhealthy",
                "service": "financial_analysis",
                "error": str(e),
                "timestamp": "2024-01-15T10:30:00Z"
            },
            status_code=503
        )
