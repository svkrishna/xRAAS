"""
XReason SDK Client
"""

import httpx
import asyncio
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin

from .models import (
    CybersecurityAnalysisRequest, CybersecurityAnalysisResponse, FinanceAnalysisRequest, FinanceAnalysisResponse, HealthcareAnalysisRequest, HealthcareAnalysisResponse, ManufacturingAnalysisRequest, ManufacturingAnalysisResponse, ReasoningRequest, ReasoningResponse,
    LegalAnalysisRequest, LegalAnalysisResponse,
    ScientificAnalysisRequest, ScientificAnalysisResponse,
    PilotSummaryResponse
)
from .exceptions import XReasonAPIError, XReasonValidationError


class XReasonClient:
    """Client for interacting with XReason API."""
    
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize XReason client.
        
        Args:
            base_url: Base URL of XReason API
            api_key: API key for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_client()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def _ensure_client(self):
        """Ensure HTTP client is initialized."""
        if self._client is None:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers=headers
            )
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to XReason API."""
        await self._ensure_client()
        
        url = urljoin(self.base_url, endpoint)
        
        for attempt in range(self.max_retries):
            try:
                response = await self._client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise XReasonAPIError(f"API request failed: {e.response.text}", e.response.status_code)
            except httpx.RequestError as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise XReasonAPIError(f"Request failed: {str(e)}")
    
    # Core Reasoning API
    async def reason(
        self,
        question: str,
        context: Optional[str] = None,
        domain: Optional[str] = None,
        ruleset_id: Optional[str] = None
    ) -> ReasoningResponse:
        """
        Perform reasoning on a question.
        
        Args:
            question: The question to reason about
            context: Additional context for reasoning
            domain: Domain for reasoning (e.g., 'healthcare', 'finance')
            ruleset_id: Specific ruleset to use
            
        Returns:
            ReasoningResponse with reasoning results
        """
        request_data = ReasoningRequest(
            question=question,
            context=context,
            domain=domain,
            ruleset_id=ruleset_id
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/reason",
            data=request_data
        )
        
        return ReasoningResponse(**response_data)
    
    # Legal Compliance API
    async def analyze_gdpr_compliance(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> LegalAnalysisResponse:
        """
        Analyze GDPR compliance of text.
        
        Args:
            text: Text to analyze for GDPR compliance
            context: Additional context for analysis
            
        Returns:
            LegalAnalysisResponse with GDPR analysis results
        """
        request_data = LegalAnalysisRequest(
            text=text,
            domains=["gdpr"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/legal/gdpr",
            data=request_data
        )
        
        return LegalAnalysisResponse(**response_data)
    
    async def analyze_hipaa_compliance(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> LegalAnalysisResponse:
        """
        Analyze HIPAA compliance of text.
        
        Args:
            text: Text to analyze for HIPAA compliance
            context: Additional context for analysis
            
        Returns:
            LegalAnalysisResponse with HIPAA analysis results
        """
        request_data = LegalAnalysisRequest(
            text=text,
            domains=["hipaa"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/legal/hipaa",
            data=request_data
        )
        
        return LegalAnalysisResponse(**response_data)
    
    async def analyze_contract(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> LegalAnalysisResponse:
        """
        Analyze contract for key provisions and risks.
        
        Args:
            text: Contract text to analyze
            context: Additional context for analysis
            
        Returns:
            LegalAnalysisResponse with contract analysis results
        """
        request_data = LegalAnalysisRequest(
            text=text,
            domains=["contract"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/legal/contract",
            data=request_data
        )
        
        return LegalAnalysisResponse(**response_data)
    
    async def analyze_legal_compliance(
        self,
        text: str,
        domains: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, LegalAnalysisResponse]:
        """
        Analyze legal compliance across multiple domains.
        
        Args:
            text: Text to analyze
            domains: List of legal domains to analyze
            context: Additional context for analysis
            
        Returns:
            Dictionary of LegalAnalysisResponse by domain
        """
        if domains is None:
            domains = ["gdpr", "hipaa", "contract"]
        
        request_data = LegalAnalysisRequest(
            text=text,
            domains=domains,
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/legal/comprehensive",
            data=request_data
        )
        
        return {
            domain: LegalAnalysisResponse(**analysis_data)
            for domain, analysis_data in response_data.items()
        }
    
    # Scientific Validation API
    async def analyze_mathematical_consistency(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ScientificAnalysisResponse:
        """
        Analyze mathematical consistency in text.
        
        Args:
            text: Text containing mathematical expressions
            context: Additional context for analysis
            
        Returns:
            ScientificAnalysisResponse with mathematical analysis results
        """
        request_data = ScientificAnalysisRequest(
            text=text,
            domains=["mathematics"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/scientific/mathematics",
            data=request_data
        )
        
        return ScientificAnalysisResponse(**response_data)
    
    async def analyze_statistical_validity(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ScientificAnalysisResponse:
        """
        Analyze statistical validity in text.
        
        Args:
            text: Text containing statistical analysis
            context: Additional context for analysis
            
        Returns:
            ScientificAnalysisResponse with statistical analysis results
        """
        request_data = ScientificAnalysisRequest(
            text=text,
            domains=["statistics"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/scientific/statistics",
            data=request_data
        )
        
        return ScientificAnalysisResponse(**response_data)
    
    async def analyze_research_methodology(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ScientificAnalysisResponse:
        """
        Analyze research methodology in text.
        
        Args:
            text: Text describing research methodology
            context: Additional context for analysis
            
        Returns:
            ScientificAnalysisResponse with methodology analysis results
        """
        request_data = ScientificAnalysisRequest(
            text=text,
            domains=["methodology"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/scientific/methodology",
            data=request_data
        )
        
        return ScientificAnalysisResponse(**response_data)
    
    async def analyze_scientific_validity(
        self,
        text: str,
        domains: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, ScientificAnalysisResponse]:
        """
        Analyze scientific validity across multiple domains.
        
        Args:
            text: Text to analyze
            domains: List of scientific domains to analyze
            context: Additional context for analysis
            
        Returns:
            Dictionary of ScientificAnalysisResponse by domain
        """
        if domains is None:
            domains = ["mathematics", "statistics", "methodology"]
        
        request_data = ScientificAnalysisRequest(
            text=text,
            domains=domains,
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/scientific/comprehensive",
            data=request_data
        )
        
        return {
            domain: ScientificAnalysisResponse(**analysis_data)
            for domain, analysis_data in response_data.items()
        }

    # Healthcare Compliance Methods
    async def analyze_hipaa_compliance(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> HealthcareAnalysisResponse:
        """
        Analyze HIPAA compliance of given text.
        
        Args:
            text: Text to analyze for HIPAA compliance
            context: Additional context for analysis
            
        Returns:
            HealthcareAnalysisResponse with HIPAA analysis results
        """
        request_data = HealthcareAnalysisRequest(
            text=text,
            domains=["hipaa"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/healthcare/hipaa",
            data=request_data
        )
        
        return HealthcareAnalysisResponse(**response_data)

    async def analyze_fda_compliance(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> HealthcareAnalysisResponse:
        """
        Analyze FDA compliance of given text.
        
        Args:
            text: Text to analyze for FDA compliance
            context: Additional context for analysis
            
        Returns:
            HealthcareAnalysisResponse with FDA analysis results
        """
        request_data = HealthcareAnalysisRequest(
            text=text,
            domains=["fda"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/healthcare/fda",
            data=request_data
        )
        
        return HealthcareAnalysisResponse(**response_data)

    async def analyze_healthcare_compliance(
        self,
        text: str,
        domains: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, HealthcareAnalysisResponse]:
        """
        Analyze healthcare compliance across multiple domains.
        
        Args:
            text: Text to analyze
            domains: List of healthcare domains to analyze
            context: Additional context for analysis
            
        Returns:
            Dictionary of HealthcareAnalysisResponse by domain
        """
        if domains is None:
            domains = ["hipaa", "fda", "clinical_trials"]
        
        request_data = HealthcareAnalysisRequest(
            text=text,
            domains=domains,
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/healthcare/comprehensive",
            data=request_data
        )
        
        return {
            domain: HealthcareAnalysisResponse(**analysis_data)
            for domain, analysis_data in response_data.items()
        }

    # Finance Compliance Methods
    async def analyze_banking_compliance(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> FinanceAnalysisResponse:
        """
        Analyze banking compliance of given text.
        
        Args:
            text: Text to analyze for banking compliance
            context: Additional context for analysis
            
        Returns:
            FinanceAnalysisResponse with banking analysis results
        """
        request_data = FinanceAnalysisRequest(
            text=text,
            domains=["banking"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/finance/banking",
            data=request_data
        )
        
        return FinanceAnalysisResponse(**response_data)

    async def analyze_finance_compliance(
        self,
        text: str,
        domains: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, FinanceAnalysisResponse]:
        """
        Analyze finance compliance across multiple domains.
        
        Args:
            text: Text to analyze
            domains: List of finance domains to analyze
            context: Additional context for analysis
            
        Returns:
            Dictionary of FinanceAnalysisResponse by domain
        """
        if domains is None:
            domains = ["banking", "investment", "aml_kyc"]
        
        request_data = FinanceAnalysisRequest(
            text=text,
            domains=domains,
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/finance/comprehensive",
            data=request_data
        )
        
        return {
            domain: FinanceAnalysisResponse(**analysis_data)
            for domain, analysis_data in response_data.items()
        }

    # Manufacturing Compliance Methods
    async def analyze_quality_control(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ManufacturingAnalysisResponse:
        """
        Analyze quality control compliance of given text.
        
        Args:
            text: Text to analyze for quality control compliance
            context: Additional context for analysis
            
        Returns:
            ManufacturingAnalysisResponse with quality control analysis results
        """
        request_data = ManufacturingAnalysisRequest(
            text=text,
            domains=["quality_control"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/manufacturing/quality-control",
            data=request_data
        )
        
        return ManufacturingAnalysisResponse(**response_data)

    async def analyze_manufacturing_compliance(
        self,
        text: str,
        domains: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, ManufacturingAnalysisResponse]:
        """
        Analyze manufacturing compliance across multiple domains.
        
        Args:
            text: Text to analyze
            domains: List of manufacturing domains to analyze
            context: Additional context for analysis
            
        Returns:
            Dictionary of ManufacturingAnalysisResponse by domain
        """
        if domains is None:
            domains = ["quality_control", "safety_standards", "environmental"]
        
        request_data = ManufacturingAnalysisRequest(
            text=text,
            domains=domains,
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/manufacturing/comprehensive",
            data=request_data
        )
        
        return {
            domain: ManufacturingAnalysisResponse(**analysis_data)
            for domain, analysis_data in response_data.items()
        }

    # Cybersecurity Compliance Methods
    async def analyze_security_frameworks(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> CybersecurityAnalysisResponse:
        """
        Analyze security frameworks compliance of given text.
        
        Args:
            text: Text to analyze for security frameworks compliance
            context: Additional context for analysis
            
        Returns:
            CybersecurityAnalysisResponse with security frameworks analysis results
        """
        request_data = CybersecurityAnalysisRequest(
            text=text,
            domains=["security_frameworks"],
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/cybersecurity/security-frameworks",
            data=request_data
        )
        
        return CybersecurityAnalysisResponse(**response_data)

    async def analyze_cybersecurity_compliance(
        self,
        text: str,
        domains: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, CybersecurityAnalysisResponse]:
        """
        Analyze cybersecurity compliance across multiple domains.
        
        Args:
            text: Text to analyze
            domains: List of cybersecurity domains to analyze
            context: Additional context for analysis
            
        Returns:
            Dictionary of CybersecurityAnalysisResponse by domain
        """
        if domains is None:
            domains = ["security_frameworks", "threat_detection", "incident_response"]
        
        request_data = CybersecurityAnalysisRequest(
            text=text,
            domains=domains,
            context=context
        ).dict(exclude_none=True)
        
        response_data = await self._make_request(
            method="POST",
            endpoint="/api/v1/pilots/cybersecurity/comprehensive",
            data=request_data
        )
        
        return {
            domain: CybersecurityAnalysisResponse(**analysis_data)
            for domain, analysis_data in response_data.items()
        }
    
    # Health Check
    async def health_check(self) -> Dict[str, Any]:
        """
        Check API health status.
        
        Returns:
            Health status information
        """
        return await self._make_request(
            method="GET",
            endpoint="/health/"
        )
    
    # Information Endpoints
    async def get_legal_domains(self) -> Dict[str, Any]:
        """Get available legal analysis domains."""
        return await self._make_request(
            method="GET",
            endpoint="/api/v1/pilots/legal/domains"
        )
    
    async def get_scientific_domains(self) -> Dict[str, Any]:
        """Get available scientific analysis domains."""
        return await self._make_request(
            method="GET",
            endpoint="/api/v1/pilots/scientific/domains"
        )
    
    async def get_legal_rules(self) -> Dict[str, Any]:
        """Get information about legal compliance rules."""
        return await self._make_request(
            method="GET",
            endpoint="/api/v1/pilots/legal/rules"
        )
    
    async def get_scientific_rules(self) -> Dict[str, Any]:
        """Get information about scientific validation rules."""
        return await self._make_request(
            method="GET",
            endpoint="/api/v1/pilots/scientific/rules"
        )
