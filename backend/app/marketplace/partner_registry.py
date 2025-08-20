"""
Partner Registry & Ecosystem Management
Comprehensive partner management with certification, validation, and marketplace integration.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Set
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
import uuid
import json
import statistics

from app.security.audit_logger import audit_logger, AuditEventType, ComplianceFramework
from app.services.ruleset_registry import ruleset_registry, RulesetSource


class PartnerStatus(str, Enum):
    """Partner status levels."""
    APPLICANT = "applicant"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    CERTIFIED = "certified"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class PartnerTier(str, Enum):
    """Partner tier levels."""
    COMMUNITY = "community"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    STRATEGIC = "strategic"


class IntegrationType(str, Enum):
    """Types of partner integrations."""
    RULESET_PROVIDER = "ruleset_provider"
    DATA_SOURCE = "data_source"
    AI_MODEL_PROVIDER = "ai_model_provider"
    COMPLIANCE_AUDITOR = "compliance_auditor"
    SYSTEM_INTEGRATOR = "system_integrator"
    TECHNOLOGY_VENDOR = "technology_vendor"


@dataclass
class PartnerContact:
    """Partner contact information."""
    name: str
    email: str
    phone: Optional[str]
    role: str
    primary: bool = False


@dataclass
class PartnerCapability:
    """Partner capability specification."""
    capability_id: str
    name: str
    description: str
    domains: List[str]
    compliance_frameworks: List[str]
    api_endpoints: List[str]
    sla_commitments: Dict[str, Any]
    pricing_model: str


@dataclass
class Partner:
    """Comprehensive partner profile."""
    partner_id: str
    name: str
    organization: str
    status: PartnerStatus
    tier: PartnerTier
    integration_types: List[IntegrationType]
    
    # Contact information
    contacts: List[PartnerContact]
    website: Optional[str]
    support_email: Optional[str]
    
    # Business details
    founded_date: Optional[datetime]
    headquarters: Optional[str]
    employee_count: Optional[int]
    annual_revenue: Optional[str]
    
    # Technical capabilities
    capabilities: List[PartnerCapability]
    api_documentation: Optional[str]
    sdk_versions: List[str]
    
    # Compliance and security
    certifications: List[str]
    security_clearances: List[str]
    compliance_frameworks: List[str]
    data_residency_requirements: List[str]
    
    # Partnership details
    partnership_start_date: datetime
    contract_end_date: Optional[datetime]
    revenue_share_percentage: float
    minimum_sla_requirements: Dict[str, Any]
    
    # Metrics
    total_rulesets: int = 0
    active_customers: int = 0
    average_rating: float = 0.0
    support_response_time_hours: Optional[float] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: Optional[datetime] = None


class PartnerRegistry:
    """
    Enterprise Partner Registry & Ecosystem Management.
    
    Features:
    - Partner onboarding and lifecycle management
    - Certification and validation workflows
    - Revenue sharing and billing integration
    - SLA monitoring and compliance tracking
    - Marketplace integration
    - Security and compliance verification
    """
    
    def __init__(self):
        self.partners: Dict[str, Partner] = {}
        self.partner_applications: Dict[str, Dict[str, Any]] = {}
        self.certification_requirements = self._load_certification_requirements()
        self.revenue_sharing_rules = self._load_revenue_sharing_rules()
        self._initialize_sample_partners()
    
    def _load_certification_requirements(self) -> Dict[str, Dict[str, Any]]:
        """Load partner certification requirements by tier."""
        return {
            PartnerTier.COMMUNITY.value: {
                "requirements": [
                    "Basic partner agreement signed",
                    "Contact information verified",
                    "At least one working integration"
                ],
                "review_period_days": 7,
                "annual_fee": 0,
                "revenue_share": 0.0,
                "sla_requirements": {
                    "availability": 95.0,
                    "response_time_ms": 10000
                }
            },
            PartnerTier.BRONZE.value: {
                "requirements": [
                    "All community requirements met",
                    "Technical documentation provided",
                    "Basic support processes defined",
                    "At least 5 customer references"
                ],
                "review_period_days": 14,
                "annual_fee": 1000,
                "revenue_share": 10.0,
                "sla_requirements": {
                    "availability": 99.0,
                    "response_time_ms": 5000,
                    "support_response_hours": 48
                }
            },
            PartnerTier.SILVER.value: {
                "requirements": [
                    "All bronze requirements met",
                    "Security audit completed",
                    "SOC2 Type II certification",
                    "24/7 support available",
                    "At least 25 customer references"
                ],
                "review_period_days": 21,
                "annual_fee": 5000,
                "revenue_share": 15.0,
                "sla_requirements": {
                    "availability": 99.5,
                    "response_time_ms": 2000,
                    "support_response_hours": 24
                }
            },
            PartnerTier.GOLD.value: {
                "requirements": [
                    "All silver requirements met",
                    "ISO27001 certification",
                    "Dedicated customer success team",
                    "API rate limiting and monitoring",
                    "At least 100 customer references",
                    "Multi-region deployment"
                ],
                "review_period_days": 30,
                "annual_fee": 15000,
                "revenue_share": 20.0,
                "sla_requirements": {
                    "availability": 99.9,
                    "response_time_ms": 1000,
                    "support_response_hours": 12
                }
            },
            PartnerTier.PLATINUM.value: {
                "requirements": [
                    "All gold requirements met",
                    "FedRAMP authorization (for government)",
                    "White-glove onboarding",
                    "Custom SLA agreements",
                    "At least 500 customer references",
                    "Global deployment with local support"
                ],
                "review_period_days": 45,
                "annual_fee": 50000,
                "revenue_share": 25.0,
                "sla_requirements": {
                    "availability": 99.99,
                    "response_time_ms": 500,
                    "support_response_hours": 4
                }
            },
            PartnerTier.STRATEGIC.value: {
                "requirements": [
                    "All platinum requirements met",
                    "Joint go-to-market strategy",
                    "Dedicated engineering resources",
                    "Co-developed solutions",
                    "Board-level partnership agreement"
                ],
                "review_period_days": 60,
                "annual_fee": 100000,
                "revenue_share": 30.0,
                "sla_requirements": {
                    "availability": 99.995,
                    "response_time_ms": 200,
                    "support_response_hours": 1
                }
            }
        }
    
    def _load_revenue_sharing_rules(self) -> Dict[str, Any]:
        """Load revenue sharing rules and calculations."""
        return {
            "base_calculation": "net_revenue_after_costs",
            "payment_frequency": "monthly",
            "minimum_payout": 100.0,
            "payment_terms_days": 30,
            "currency": "USD",
            "tax_handling": "partner_responsible",
            "dispute_resolution": "arbitration",
            "tier_bonuses": {
                PartnerTier.GOLD.value: 2.0,      # +2% bonus
                PartnerTier.PLATINUM.value: 5.0,   # +5% bonus
                PartnerTier.STRATEGIC.value: 10.0  # +10% bonus
            },
            "volume_bonuses": [
                {"threshold": 10000, "bonus_percentage": 1.0},
                {"threshold": 50000, "bonus_percentage": 2.0},
                {"threshold": 100000, "bonus_percentage": 3.0}
            ]
        }
    
    def _initialize_sample_partners(self):
        """Initialize with sample strategic partners."""
        sample_partners = [
            {
                "name": "HealthTech Solutions",
                "organization": "HealthTech Solutions Inc.",
                "integration_types": [IntegrationType.RULESET_PROVIDER, IntegrationType.COMPLIANCE_AUDITOR],
                "tier": PartnerTier.GOLD,
                "domains": ["healthcare", "medical_devices", "hipaa"],
                "compliance_frameworks": ["HIPAA", "FDA", "SOC2"]
            },
            {
                "name": "FinCompliance Pro",
                "organization": "Financial Compliance Technologies",
                "integration_types": [IntegrationType.RULESET_PROVIDER, IntegrationType.AI_MODEL_PROVIDER],
                "tier": PartnerTier.PLATINUM,
                "domains": ["finance", "banking", "securities"],
                "compliance_frameworks": ["SOX", "Basel III", "PCI DSS"]
            },
            {
                "name": "LegalAI Partners",
                "organization": "LegalTech Innovations LLC",
                "integration_types": [IntegrationType.RULESET_PROVIDER, IntegrationType.DATA_SOURCE],
                "tier": PartnerTier.SILVER,
                "domains": ["legal", "contracts", "litigation"],
                "compliance_frameworks": ["GDPR", "CCPA", "Legal Ethics"]
            }
        ]
        
        for partner_data in sample_partners:
            try:
                self.register_partner(
                    name=partner_data["name"],
                    organization=partner_data["organization"],
                    integration_types=partner_data["integration_types"],
                    target_tier=partner_data["tier"],
                    contact_name="Partner Manager",
                    contact_email=f"contact@{partner_data['name'].lower().replace(' ', '')}.com",
                    capabilities=[
                        PartnerCapability(
                            capability_id=f"{partner_data['name'].lower().replace(' ', '_')}_rules",
                            name=f"{partner_data['name']} Rule Engine",
                            description=f"Specialized rules for {', '.join(partner_data['domains'])}",
                            domains=partner_data["domains"],
                            compliance_frameworks=partner_data["compliance_frameworks"],
                            api_endpoints=["/api/v1/rules", "/api/v1/validate"],
                            sla_commitments={"availability": 99.9, "response_time_ms": 1000},
                            pricing_model="usage_based"
                        )
                    ]
                )
            except Exception:
                # Partner might already exist
                pass
    
    def register_partner(
        self,
        name: str,
        organization: str,
        integration_types: List[IntegrationType],
        target_tier: PartnerTier,
        contact_name: str,
        contact_email: str,
        capabilities: List[PartnerCapability],
        website: Optional[str] = None,
        founded_date: Optional[datetime] = None,
        headquarters: Optional[str] = None,
        employee_count: Optional[int] = None
    ) -> str:
        """
        Register a new partner in the registry.
        
        Args:
            name: Partner name
            organization: Organization name
            integration_types: Types of integration offered
            target_tier: Desired partner tier
            contact_name: Primary contact name
            contact_email: Primary contact email
            capabilities: List of partner capabilities
            website: Partner website
            founded_date: Company founding date
            headquarters: Company headquarters location
            employee_count: Number of employees
            
        Returns:
            str: Partner ID
        """
        partner_id = f"partner_{uuid.uuid4().hex[:8]}"
        
        # Create primary contact
        primary_contact = PartnerContact(
            name=contact_name,
            email=contact_email,
            phone=None,
            role="Primary Contact",
            primary=True
        )
        
        # Determine initial status and tier
        initial_status = PartnerStatus.APPLICANT
        initial_tier = PartnerTier.COMMUNITY  # Start at community level
        
        # Get tier requirements
        tier_requirements = self.certification_requirements.get(target_tier.value, {})
        
        partner = Partner(
            partner_id=partner_id,
            name=name,
            organization=organization,
            status=initial_status,
            tier=initial_tier,
            integration_types=integration_types,
            contacts=[primary_contact],
            website=website,
            support_email=contact_email,
            founded_date=founded_date,
            headquarters=headquarters,
            employee_count=employee_count,
            capabilities=capabilities,
            api_documentation=None,
            sdk_versions=[],
            certifications=[],
            security_clearances=[],
            compliance_frameworks=[],
            data_residency_requirements=[],
            partnership_start_date=datetime.now(timezone.utc),
            contract_end_date=None,
            revenue_share_percentage=tier_requirements.get("revenue_share", 0.0),
            minimum_sla_requirements=tier_requirements.get("sla_requirements", {})
        )
        
        self.partners[partner_id] = partner
        
        # Log partner registration
        audit_logger.log_event(
            event_type=AuditEventType.ADMIN_ACTION,
            action="register_partner",
            result="success",
            details={
                "partner_id": partner_id,
                "name": name,
                "organization": organization,
                "target_tier": target_tier.value,
                "integration_types": [t.value for t in integration_types],
                "capabilities_count": len(capabilities)
            },
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="medium"
        )
        
        # Start approval workflow
        self._initiate_partner_review(partner_id, target_tier)
        
        return partner_id
    
    def _initiate_partner_review(self, partner_id: str, target_tier: PartnerTier):
        """Initiate partner review workflow."""
        if partner_id not in self.partners:
            return
        
        partner = self.partners[partner_id]
        tier_requirements = self.certification_requirements.get(target_tier.value, {})
        
        # Create review application
        application = {
            "application_id": str(uuid.uuid4()),
            "partner_id": partner_id,
            "target_tier": target_tier.value,
            "submitted_at": datetime.now(timezone.utc),
            "requirements": tier_requirements.get("requirements", []),
            "review_deadline": datetime.now(timezone.utc) + timedelta(
                days=tier_requirements.get("review_period_days", 14)
            ),
            "status": "pending_review",
            "reviewer_notes": [],
            "completed_requirements": []
        }
        
        self.partner_applications[partner_id] = application
        
        # Update partner status
        partner.status = PartnerStatus.UNDER_REVIEW
        partner.updated_at = datetime.now(timezone.utc)
    
    def approve_partner(
        self,
        partner_id: str,
        approved_tier: PartnerTier,
        reviewer_id: str,
        notes: str = ""
    ) -> bool:
        """
        Approve partner for specific tier.
        
        Args:
            partner_id: Partner to approve
            approved_tier: Approved tier level
            reviewer_id: ID of reviewer
            notes: Approval notes
            
        Returns:
            bool: True if approved successfully
        """
        if partner_id not in self.partners:
            return False
        
        partner = self.partners[partner_id]
        tier_config = self.certification_requirements.get(approved_tier.value, {})
        
        # Update partner details
        partner.status = PartnerStatus.APPROVED
        partner.tier = approved_tier
        partner.revenue_share_percentage = tier_config.get("revenue_share", 0.0)
        partner.minimum_sla_requirements = tier_config.get("sla_requirements", {})
        partner.updated_at = datetime.now(timezone.utc)
        
        # Update application status
        if partner_id in self.partner_applications:
            application = self.partner_applications[partner_id]
            application["status"] = "approved"
            application["approved_tier"] = approved_tier.value
            application["approved_at"] = datetime.now(timezone.utc)
            application["reviewer_id"] = reviewer_id
            application["reviewer_notes"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "reviewer": reviewer_id,
                "note": notes,
                "action": "approved"
            })
        
        # Log approval
        audit_logger.log_event(
            event_type=AuditEventType.ADMIN_ACTION,
            action="approve_partner",
            result="success",
            details={
                "partner_id": partner_id,
                "approved_tier": approved_tier.value,
                "reviewer_id": reviewer_id,
                "revenue_share": partner.revenue_share_percentage,
                "notes": notes
            },
            user_id=reviewer_id,
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="medium"
        )
        
        return True
    
    def get_partner(self, partner_id: str) -> Optional[Partner]:
        """Get partner by ID."""
        return self.partners.get(partner_id)
    
    def list_partners(
        self,
        status: Optional[PartnerStatus] = None,
        tier: Optional[PartnerTier] = None,
        integration_type: Optional[IntegrationType] = None,
        domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List partners with optional filtering.
        
        Args:
            status: Filter by partner status
            tier: Filter by partner tier
            integration_type: Filter by integration type
            domain: Filter by domain capability
            
        Returns:
            List of partner summaries
        """
        filtered_partners = []
        
        for partner in self.partners.values():
            # Apply filters
            if status and partner.status != status:
                continue
            if tier and partner.tier != tier:
                continue
            if integration_type and integration_type not in partner.integration_types:
                continue
            if domain and not any(domain in cap.domains for cap in partner.capabilities):
                continue
            
            # Create summary
            summary = {
                "partner_id": partner.partner_id,
                "name": partner.name,
                "organization": partner.organization,
                "status": partner.status.value,
                "tier": partner.tier.value,
                "integration_types": [t.value for t in partner.integration_types],
                "capabilities_count": len(partner.capabilities),
                "total_rulesets": partner.total_rulesets,
                "active_customers": partner.active_customers,
                "average_rating": partner.average_rating,
                "partnership_start_date": partner.partnership_start_date.isoformat(),
                "last_activity": partner.last_activity.isoformat() if partner.last_activity else None
            }
            
            filtered_partners.append(summary)
        
        return filtered_partners
    
    def get_partner_metrics(self, partner_id: str) -> Dict[str, Any]:
        """Get comprehensive partner metrics."""
        if partner_id not in self.partners:
            return {}
        
        partner = self.partners[partner_id]
        
        # Get partner rulesets from registry
        partner_rulesets = ruleset_registry.list_rulesets(source=RulesetSource.PARTNER)
        partner_specific_rulesets = [
            r for r in partner_rulesets
            if r.get("organization") == partner.organization
        ]
        
        return {
            "partner_id": partner_id,
            "basic_info": {
                "name": partner.name,
                "organization": partner.organization,
                "status": partner.status.value,
                "tier": partner.tier.value
            },
            "business_metrics": {
                "total_rulesets": len(partner_specific_rulesets),
                "active_customers": partner.active_customers,
                "average_rating": partner.average_rating,
                "revenue_share_percentage": partner.revenue_share_percentage
            },
            "performance_metrics": {
                "support_response_time_hours": partner.support_response_time_hours,
                "sla_compliance": "99.9%",  # Would be calculated from actual metrics
                "availability_percentage": 99.95  # Would be calculated from monitoring
            },
            "ruleset_metrics": {
                "total_rulesets": len(partner_specific_rulesets),
                "domains_covered": len(set().union(*[cap.domains for cap in partner.capabilities])),
                "compliance_frameworks": len(set().union(*[cap.compliance_frameworks for cap in partner.capabilities])),
                "download_count": sum(r.get("download_count", 0) for r in partner_specific_rulesets)
            },
            "partnership_details": {
                "partnership_duration_days": (datetime.now(timezone.utc) - partner.partnership_start_date).days,
                "contract_end_date": partner.contract_end_date.isoformat() if partner.contract_end_date else None,
                "next_review_date": (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
            }
        }
    
    def get_marketplace_dashboard(self) -> Dict[str, Any]:
        """Get marketplace ecosystem dashboard."""
        total_partners = len(self.partners)
        
        # Count by status
        status_counts = {}
        for status in PartnerStatus:
            status_counts[status.value] = sum(
                1 for p in self.partners.values() if p.status == status
            )
        
        # Count by tier
        tier_counts = {}
        for tier in PartnerTier:
            tier_counts[tier.value] = sum(
                1 for p in self.partners.values() if p.tier == tier
            )
        
        # Integration type distribution
        integration_counts = {}
        for integration_type in IntegrationType:
            integration_counts[integration_type.value] = sum(
                1 for p in self.partners.values()
                if integration_type in p.integration_types
            )
        
        # Calculate total ecosystem value
        total_rulesets = sum(p.total_rulesets for p in self.partners.values())
        total_customers = sum(p.active_customers for p in self.partners.values())
        average_partner_rating = statistics.mean([
            p.average_rating for p in self.partners.values()
            if p.average_rating > 0
        ]) if any(p.average_rating > 0 for p in self.partners.values()) else 0
        
        return {
            "ecosystem_overview": {
                "total_partners": total_partners,
                "active_partners": status_counts.get("approved", 0) + status_counts.get("certified", 0),
                "total_rulesets": total_rulesets,
                "total_customers": total_customers,
                "average_partner_rating": round(average_partner_rating, 2)
            },
            "partner_distribution": {
                "by_status": status_counts,
                "by_tier": tier_counts,
                "by_integration_type": integration_counts
            },
            "business_metrics": {
                "total_revenue_potential": sum(
                    p.revenue_share_percentage * 1000  # Mock calculation
                    for p in self.partners.values()
                ),
                "average_revenue_share": statistics.mean([
                    p.revenue_share_percentage for p in self.partners.values()
                ]) if self.partners else 0,
                "tier_distribution_value": tier_counts
            },
            "growth_metrics": {
                "new_partners_this_month": sum(
                    1 for p in self.partners.values()
                    if p.created_at >= datetime.now(timezone.utc) - timedelta(days=30)
                ),
                "pending_applications": len(self.partner_applications),
                "certification_pipeline": {
                    tier.value: sum(
                        1 for app in self.partner_applications.values()
                        if app.get("target_tier") == tier.value
                    )
                    for tier in PartnerTier
                }
            }
        }


# Global partner registry instance
partner_registry = PartnerRegistry()
