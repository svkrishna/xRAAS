"""
XReason Pilots
Domain-specific reasoning pilots for different industries.
"""

from .cybersecurity_compliance import CybersecurityCompliancePilot
from .finance_compliance import FinanceCompliancePilot
from .healthcare_compliance import HealthcareCompliancePilot
from .legal_compliance import LegalCompliancePilot
from .manufacturing_compliance import ManufacturingCompliancePilot
from .scientific_validation import ScientificValidationPilot

__all__ = [
    "CybersecurityCompliancePilot",
    "FinanceCompliancePilot", 
    "HealthcareCompliancePilot",
    "LegalCompliancePilot",
    "ManufacturingCompliancePilot",
    "ScientificValidationPilot"
]
