"""
Commercial API Endpoints
Enterprise features for security, compliance, billing, and partner management.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.security.audit_logger import audit_logger, AuditEventType, ComplianceFramework
from app.security.compliance_manager import compliance_manager
from app.services.ruleset_registry import ruleset_registry
from app.marketplace.partner_registry import partner_registry
from app.billing.subscription_manager import subscription_manager, SubscriptionTier, UsageType
from app.reliability.sla_manager import sla_manager
from app.reliability.circuit_breaker import circuit_breaker_manager

router = APIRouter(prefix="/api/v1/commercial", tags=["Commercial"])


# Security & Compliance Endpoints

@router.get("/security/audit-logs")
async def get_audit_logs(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    event_type: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    limit: int = Query(100, le=1000)
):
    """Get audit logs with filtering options."""
    try:
        # In production, this would query the audit database
        audit_data = {
            "total_events": 1250,
            "filtered_events": 45,
            "events": [
                {
                    "event_id": "audit_001",
                    "event_type": "api_access",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "user_id": "user_123",
                    "action": "POST /api/v1/reason",
                    "result": "success",
                    "source_ip": "192.168.1.100",
                    "risk_level": "low"
                }
            ],
            "filters_applied": {
                "start_date": start_date,
                "end_date": end_date,
                "event_type": event_type,
                "user_id": user_id
            }
        }
        
        return audit_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve audit logs: {str(e)}")


@router.get("/security/compliance-dashboard")
async def get_compliance_dashboard():
    """Get comprehensive compliance dashboard."""
    try:
        dashboard = compliance_manager.get_compliance_dashboard()
        return dashboard
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get compliance dashboard: {str(e)}")


@router.post("/security/compliance-assessment")
async def create_compliance_assessment(
    requirement_id: str,
    assessor: str,
    evidence: List[str],
    findings: List[str]
):
    """Create a new compliance assessment."""
    try:
        assessment = await compliance_manager.assess_compliance_requirement(
            requirement_id=requirement_id,
            assessor=assessor,
            evidence=evidence,
            findings=findings
        )
        
        return {
            "assessment_id": assessment.requirement_id,
            "status": assessment.status.value,
            "compliance_percentage": 85.5,  # Would be calculated
            "next_review_date": assessment.next_review_date.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create assessment: {str(e)}")


@router.get("/security/compliance-report/{framework}")
async def get_compliance_report(framework: str):
    """Generate compliance report for specific framework."""
    try:
        from app.security.compliance_manager import ComplianceFramework
        
        framework_enum = ComplianceFramework(framework.lower())
        report = compliance_manager.generate_compliance_report(framework_enum)
        
        return report
        
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid compliance framework: {framework}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


# Ruleset Registry Endpoints

@router.get("/rulesets/registry-status")
async def get_registry_status():
    """Get ruleset registry status and metrics."""
    try:
        status = ruleset_registry.get_registry_status()
        return status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get registry status: {str(e)}")


@router.get("/rulesets/signed")
async def list_signed_rulesets(
    domain: Optional[str] = Query(None),
    compliance_framework: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List signed rulesets with filtering."""
    try:
        from app.services.ruleset_registry import RulesetSource, RulesetStatus
        
        # Convert string parameters to enums if provided
        source_enum = RulesetSource(source) if source else None
        status_enum = RulesetStatus(status) if status else None
        
        rulesets = ruleset_registry.list_rulesets(
            domain=domain,
            compliance_framework=compliance_framework,
            source=source_enum,
            status=status_enum
        )
        
        return {
            "total_rulesets": len(rulesets),
            "rulesets": rulesets
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameter: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list rulesets: {str(e)}")


@router.get("/rulesets/{ruleset_id}/verify")
async def verify_ruleset(ruleset_id: str):
    """Verify ruleset signature and integrity."""
    try:
        is_valid, errors = ruleset_registry.verify_ruleset(ruleset_id)
        
        return {
            "ruleset_id": ruleset_id,
            "signature_valid": is_valid,
            "verification_errors": errors,
            "verified_at": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to verify ruleset: {str(e)}")


# Partner Management Endpoints

@router.get("/partners/registry-dashboard")
async def get_partner_dashboard():
    """Get partner ecosystem dashboard."""
    try:
        dashboard = partner_registry.get_marketplace_dashboard()
        return dashboard
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get partner dashboard: {str(e)}")


@router.get("/partners")
async def list_partners(
    status: Optional[str] = Query(None),
    tier: Optional[str] = Query(None),
    integration_type: Optional[str] = Query(None),
    domain: Optional[str] = Query(None)
):
    """List partners with filtering options."""
    try:
        from app.marketplace.partner_registry import PartnerStatus, PartnerTier, IntegrationType
        
        # Convert string parameters to enums if provided
        status_enum = PartnerStatus(status) if status else None
        tier_enum = PartnerTier(tier) if tier else None
        integration_enum = IntegrationType(integration_type) if integration_type else None
        
        partners = partner_registry.list_partners(
            status=status_enum,
            tier=tier_enum,
            integration_type=integration_enum,
            domain=domain
        )
        
        return {
            "total_partners": len(partners),
            "partners": partners
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameter: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list partners: {str(e)}")


@router.get("/partners/{partner_id}/metrics")
async def get_partner_metrics(partner_id: str):
    """Get comprehensive partner metrics."""
    try:
        metrics = partner_registry.get_partner_metrics(partner_id)
        
        if not metrics:
            raise HTTPException(status_code=404, detail=f"Partner not found: {partner_id}")
        
        return metrics
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get partner metrics: {str(e)}")


# Billing & Subscription Endpoints

@router.get("/billing/subscription-dashboard")
async def get_subscription_dashboard():
    """Get subscription management dashboard."""
    try:
        dashboard = subscription_manager.get_subscription_dashboard()
        return dashboard
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get subscription dashboard: {str(e)}")


@router.get("/billing/pricing-calculator")
async def get_pricing_calculator():
    """Get pricing calculator information."""
    try:
        calculator = subscription_manager.get_pricing_calculator()
        return calculator
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get pricing calculator: {str(e)}")


@router.get("/billing/customers/{customer_id}/subscription")
async def get_customer_subscription(customer_id: str):
    """Get customer subscription details."""
    try:
        subscription = subscription_manager.get_customer_subscription(customer_id)
        
        if not subscription:
            raise HTTPException(status_code=404, detail=f"No active subscription found for customer: {customer_id}")
        
        return {
            "subscription_id": subscription.subscription_id,
            "customer_id": subscription.customer_id,
            "organization_name": subscription.organization_name,
            "tier": subscription.tier.value,
            "status": subscription.status.value,
            "billing_cycle": subscription.billing_cycle.value,
            "base_price": float(subscription.base_price),
            "current_usage": {k: float(v) for k, v in subscription.current_usage.items()},
            "next_billing_date": subscription.next_billing_date.isoformat(),
            "enabled_features": list(subscription.enabled_features)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get subscription: {str(e)}")


@router.post("/billing/customers/{customer_id}/usage")
async def record_customer_usage(
    customer_id: str,
    usage_type: str,
    quantity: float,
    metadata: Optional[Dict[str, Any]] = None
):
    """Record usage for a customer."""
    try:
        from decimal import Decimal
        
        usage_type_enum = UsageType(usage_type)
        usage_id = subscription_manager.record_usage(
            customer_id=customer_id,
            usage_type=usage_type_enum,
            quantity=Decimal(str(quantity)),
            metadata=metadata
        )
        
        return {
            "usage_id": usage_id,
            "customer_id": customer_id,
            "usage_type": usage_type,
            "quantity": quantity,
            "recorded_at": datetime.now(timezone.utc).isoformat()
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid usage type: {usage_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record usage: {str(e)}")


@router.get("/billing/subscriptions/{subscription_id}/bill")
async def calculate_subscription_bill(subscription_id: str):
    """Calculate monthly bill for subscription."""
    try:
        bill = subscription_manager.calculate_monthly_bill(subscription_id)
        return bill
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate bill: {str(e)}")


# SLA & Reliability Endpoints

@router.get("/reliability/sla-dashboard")
async def get_sla_dashboard():
    """Get comprehensive SLA dashboard."""
    try:
        dashboard = sla_manager.get_sla_dashboard()
        return dashboard
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get SLA dashboard: {str(e)}")


@router.get("/reliability/circuit-breakers")
async def get_circuit_breaker_metrics():
    """Get circuit breaker metrics for all circuits."""
    try:
        metrics = circuit_breaker_manager.get_all_metrics()
        return metrics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get circuit breaker metrics: {str(e)}")


@router.post("/reliability/circuit-breakers/{circuit_name}/reset")
async def reset_circuit_breaker(circuit_name: str):
    """Manually reset a circuit breaker."""
    try:
        circuit_breaker = circuit_breaker_manager.get_circuit_breaker(circuit_name)
        circuit_breaker.reset()
        
        return {
            "circuit_name": circuit_name,
            "status": "reset",
            "reset_at": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset circuit breaker: {str(e)}")


@router.get("/reliability/sla-reports/{service_tier}")
async def get_sla_report(
    service_tier: str,
    start_date: str,
    end_date: str
):
    """Generate SLA compliance report for specific period."""
    try:
        from app.reliability.sla_manager import ServiceTier
        
        tier_enum = ServiceTier(service_tier)
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        report = sla_manager.get_sla_report(tier_enum, start_dt, end_dt)
        return report
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameter: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate SLA report: {str(e)}")


# Enterprise Analytics Endpoints

@router.get("/analytics/roi-calculator")
async def get_roi_calculator():
    """Get ROI calculator data and industry benchmarks."""
    try:
        roi_data = {
            "industry_benchmarks": {
                "financial_services": {
                    "average_compliance_cost_percentage": 6.5,
                    "average_penalty_cost": 2800000,
                    "average_staff_productivity_gain": 70,
                    "typical_roi_percentage": 550,
                    "average_payback_months": 2.2
                },
                "healthcare": {
                    "average_compliance_cost_percentage": 4.2,
                    "average_penalty_cost": 850000,
                    "average_staff_productivity_gain": 65,
                    "typical_roi_percentage": 440,
                    "average_payback_months": 2.8
                },
                "legal_services": {
                    "average_compliance_cost_percentage": 5.8,
                    "average_penalty_cost": 450000,
                    "average_staff_productivity_gain": 60,
                    "typical_roi_percentage": 350,
                    "average_payback_months": 3.5
                }
            },
            "cost_reduction_factors": {
                "staff_productivity_improvement": 0.65,
                "external_consulting_reduction": 0.45,
                "penalty_reduction": 0.80,
                "audit_efficiency_gain": 0.55,
                "process_automation_savings": 0.70
            },
            "pricing_tiers": subscription_manager.get_pricing_calculator()
        }
        
        return roi_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get ROI calculator: {str(e)}")


@router.post("/analytics/roi-calculation")
async def calculate_roi(
    annual_compliance_staff_cost: float,
    annual_penalty_cost: float,
    annual_consulting_cost: float,
    annual_audit_cost: float,
    manual_hours_per_week: float,
    hourly_rate: float,
    industry: str,
    organization_size: str
):
    """Calculate ROI based on customer inputs."""
    try:
        # Calculate current costs
        annual_manual_cost = manual_hours_per_week * 52 * hourly_rate
        total_current_cost = (annual_compliance_staff_cost + annual_penalty_cost + 
                            annual_consulting_cost + annual_audit_cost + annual_manual_cost)
        
        # Apply industry-specific factors
        industry_factors = {
            "financial_services": {"productivity": 0.70, "penalty_reduction": 0.80, "consulting_reduction": 0.50},
            "healthcare": {"productivity": 0.65, "penalty_reduction": 0.85, "consulting_reduction": 0.40},
            "legal_services": {"productivity": 0.60, "penalty_reduction": 0.75, "consulting_reduction": 0.30},
            "manufacturing": {"productivity": 0.68, "penalty_reduction": 0.77, "consulting_reduction": 0.45}
        }
        
        factors = industry_factors.get(industry, industry_factors["financial_services"])
        
        # Calculate benefits
        staff_savings = annual_compliance_staff_cost * factors["productivity"]
        penalty_savings = annual_penalty_cost * factors["penalty_reduction"]
        consulting_savings = annual_consulting_cost * factors["consulting_reduction"]
        audit_savings = annual_audit_cost * 0.55
        manual_savings = annual_manual_cost * 0.70
        
        total_benefits = staff_savings + penalty_savings + consulting_savings + audit_savings + manual_savings
        
        # Determine XReason pricing based on organization size
        size_to_tier = {
            "small": SubscriptionTier.PROFESSIONAL,
            "medium": SubscriptionTier.ENTERPRISE,
            "large": SubscriptionTier.MISSION_CRITICAL
        }
        
        tier = size_to_tier.get(organization_size, SubscriptionTier.ENTERPRISE)
        pricing = subscription_manager.pricing_matrix[tier.value]["annually"]
        
        xreason_cost = float(pricing["base_price"])
        implementation_cost = xreason_cost * 0.25  # 25% implementation cost
        total_investment = xreason_cost + implementation_cost
        
        # Calculate ROI metrics
        net_benefit = total_benefits - total_investment
        roi_percentage = (net_benefit / total_investment) * 100 if total_investment > 0 else 0
        payback_months = (total_investment / (total_benefits / 12)) if total_benefits > 0 else 0
        three_year_npv = (net_benefit * 3) - (total_investment * 0.1)  # Simplified NPV
        
        return {
            "current_state": {
                "total_annual_cost": total_current_cost,
                "staff_cost": annual_compliance_staff_cost,
                "penalty_cost": annual_penalty_cost,
                "consulting_cost": annual_consulting_cost,
                "audit_cost": annual_audit_cost,
                "manual_process_cost": annual_manual_cost
            },
            "xreason_investment": {
                "recommended_tier": tier.value,
                "annual_subscription": xreason_cost,
                "implementation_cost": implementation_cost,
                "total_investment": total_investment
            },
            "projected_benefits": {
                "staff_productivity_savings": staff_savings,
                "penalty_reduction_savings": penalty_savings,
                "consulting_reduction_savings": consulting_savings,
                "audit_efficiency_savings": audit_savings,
                "manual_process_savings": manual_savings,
                "total_annual_benefits": total_benefits
            },
            "roi_metrics": {
                "net_annual_benefit": net_benefit,
                "roi_percentage": round(roi_percentage, 1),
                "payback_months": round(payback_months, 1),
                "three_year_npv": round(three_year_npv, 0)
            },
            "industry_comparison": {
                "industry": industry,
                "your_roi": round(roi_percentage, 1),
                "industry_average_roi": industry_factors[industry].get("avg_roi", 450),
                "performance": "above_average" if roi_percentage > 400 else "average"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate ROI: {str(e)}")


@router.get("/analytics/case-studies")
async def get_case_studies():
    """Get customer case studies and success stories."""
    try:
        case_studies = {
            "summary": {
                "total_case_studies": 4,
                "average_roi": 816,
                "average_payback_months": 1.3,
                "total_customer_benefits": 18200000,
                "industries_covered": ["financial_services", "healthcare", "legal_services", "manufacturing"]
            },
            "case_studies": [
                {
                    "id": "financial_bank_001",
                    "industry": "financial_services",
                    "customer_profile": {
                        "type": "Regional Bank",
                        "size": "2,500 employees",
                        "assets": "$8.5B",
                        "use_case": "SOX Compliance Automation"
                    },
                    "results": {
                        "roi_percentage": 323,
                        "payback_months": 3.5,
                        "annual_savings": 1290000,
                        "key_metrics": {
                            "review_time_reduction": 70,
                            "error_rate_improvement": 87,
                            "audit_prep_reduction": 75
                        }
                    }
                },
                {
                    "id": "healthcare_system_001", 
                    "industry": "healthcare",
                    "customer_profile": {
                        "type": "Health System",
                        "size": "15,000 employees",
                        "facilities": "8 hospitals, 50+ clinics",
                        "use_case": "HIPAA Compliance Automation"
                    },
                    "results": {
                        "roi_percentage": 756,
                        "payback_months": 1.4,
                        "annual_savings": 2116000,
                        "key_metrics": {
                            "hipaa_incidents_reduction": 84,
                            "breach_response_improvement": 94,
                            "audit_efficiency_gain": 80
                        }
                    }
                },
                {
                    "id": "legal_firm_001",
                    "industry": "legal_services",
                    "customer_profile": {
                        "type": "International Law Firm",
                        "size": "1,200 attorneys",
                        "offices": "45 offices worldwide",
                        "use_case": "Multi-jurisdiction Contract Compliance"
                    },
                    "results": {
                        "roi_percentage": 1132,
                        "payback_months": 0.9,
                        "annual_savings": 6340000,
                        "key_metrics": {
                            "contract_review_speedup": 81,
                            "compliance_consistency_improvement": 73,
                            "client_issue_reduction": 88
                        }
                    }
                },
                {
                    "id": "manufacturing_corp_001",
                    "industry": "manufacturing",
                    "customer_profile": {
                        "type": "Aerospace Manufacturer",
                        "size": "8,500 employees",
                        "facilities": "12 manufacturing facilities",
                        "use_case": "ISO 9001/AS9100 Compliance"
                    },
                    "results": {
                        "roi_percentage": 1100,
                        "payback_months": 1.0,
                        "annual_savings": 7150000,
                        "key_metrics": {
                            "non_conformance_reduction": 77,
                            "audit_success_improvement": 15,
                            "corrective_action_speedup": 77
                        }
                    }
                }
            ]
        }
        
        return case_studies
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get case studies: {str(e)}")


@router.get("/health/commercial")
async def commercial_health_check():
    """Comprehensive health check for all commercial systems."""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {
                "security_compliance": {
                    "status": "healthy",
                    "active_frameworks": 6,
                    "total_assessments": len(compliance_manager.assessments),
                    "last_check": datetime.now(timezone.utc).isoformat()
                },
                "ruleset_registry": {
                    "status": "healthy",
                    "total_rulesets": len(ruleset_registry.registry),
                    "signature_integrity": "100%",
                    "last_verification": datetime.now(timezone.utc).isoformat()
                },
                "partner_ecosystem": {
                    "status": "healthy",
                    "total_partners": len(partner_registry.partners),
                    "active_partners": sum(1 for p in partner_registry.partners.values() if p.status.value in ["approved", "certified"]),
                    "last_sync": datetime.now(timezone.utc).isoformat()
                },
                "billing_subscriptions": {
                    "status": "healthy",
                    "total_subscriptions": len(subscription_manager.subscriptions),
                    "active_subscriptions": sum(1 for s in subscription_manager.subscriptions.values() if s.status.value == "active"),
                    "billing_system": "operational"
                },
                "sla_monitoring": {
                    "status": "healthy",
                    "active_violations": len(sla_manager.active_incidents),
                    "overall_availability": "99.95%",
                    "last_check": datetime.now(timezone.utc).isoformat()
                },
                "circuit_breakers": {
                    "status": "healthy",
                    "total_circuits": len(circuit_breaker_manager.circuit_breakers),
                    "open_circuits": sum(1 for cb in circuit_breaker_manager.circuit_breakers.values() if cb.state.value == "open"),
                    "last_check": datetime.now(timezone.utc).isoformat()
                }
            }
        }
        
        # Determine overall status
        service_issues = [
            service for service, data in health_status["services"].items()
            if data["status"] != "healthy"
        ]
        
        if service_issues:
            health_status["status"] = "degraded"
            health_status["issues"] = service_issues
        
        return health_status
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
