"""
XReason SDK - Python client for XReason Reasoning as a Service
"""

from .client import XReasonClient
from .models import (
    ReasoningRequest, ReasoningResponse, ReasoningTrace,
    LegalAnalysisRequest, LegalAnalysisResponse,
    ScientificAnalysisRequest, ScientificAnalysisResponse,
    PilotSummaryResponse
)
from .exceptions import XReasonError, XReasonAPIError, XReasonValidationError

__version__ = "1.0.0"
__author__ = "XReason Team"
__email__ = "support@xreason.ai"

__all__ = [
    "XReasonClient",
    "ReasoningRequest",
    "ReasoningResponse", 
    "ReasoningTrace",
    "LegalAnalysisRequest",
    "LegalAnalysisResponse",
    "ScientificAnalysisRequest",
    "ScientificAnalysisResponse",
    "PilotSummaryResponse",
    "XReasonError",
    "XReasonAPIError",
    "XReasonValidationError"
]
