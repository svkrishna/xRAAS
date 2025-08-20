"""
Subscription Management & SaaS Tiers
Comprehensive subscription lifecycle management with usage-based billing.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Set
from enum import Enum
from dataclasses import dataclass, field
from decimal import Decimal
import uuid

from app.security.audit_logger import audit_logger, AuditEventType, ComplianceFramework


class SubscriptionTier(str, Enum):
    """SaaS subscription tiers."""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    MISSION_CRITICAL = "mission_critical"


class SubscriptionStatus(str, Enum):
    """Subscription status values."""
    TRIAL = "trial"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELED = "canceled"
    EXPIRED = "expired"
    PAST_DUE = "past_due"


class BillingCycle(str, Enum):
    """Billing cycle options."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"


class UsageType(str, Enum):
    """Types of usage metrics."""
    REASONING_UNITS = "reasoning_units"
    API_CALLS = "api_calls"
    DATA_STORAGE = "data_storage"
    COMPUTE_TIME = "compute_time"
    CUSTOM_RULESETS = "custom_rulesets"
    PREMIUM_FEATURES = "premium_features"


@dataclass
class TierLimits:
    """Usage limits for subscription tiers."""
    reasoning_units_per_month: int
    api_calls_per_month: int
    data_storage_gb: int
    compute_time_hours: int
    custom_rulesets: int
    max_users: int
    sla_availability: float
    response_time_ms: int
    support_level: str
    premium_features: List[str]


@dataclass
class UsageRecord:
    """Individual usage record."""
    usage_id: str
    customer_id: str
    usage_type: UsageType
    quantity: Decimal
    unit_price: Decimal
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Subscription:
    """Customer subscription details."""
    subscription_id: str
    customer_id: str
    organization_name: str
    tier: SubscriptionTier
    status: SubscriptionStatus
    billing_cycle: BillingCycle
    
    # Pricing
    base_price: Decimal
    usage_based_pricing: Dict[str, Decimal]  # Per-unit pricing
    
    # Limits
    tier_limits: TierLimits
    custom_limits: Dict[str, Any]
    
    # Dates
    start_date: datetime
    end_date: Optional[datetime]
    trial_end_date: Optional[datetime]
    next_billing_date: datetime
    
    # Usage tracking
    current_usage: Dict[str, Decimal] = field(default_factory=dict)
    usage_alerts_sent: List[str] = field(default_factory=list)
    
    # Features
    enabled_features: Set[str] = field(default_factory=set)
    custom_integrations: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class SubscriptionManager:
    """
    Comprehensive Subscription Management System.
    
    Features:
    - Multi-tier SaaS pricing (Starter, Professional, Enterprise, Mission Critical)
    - Usage-based billing with Reasoning Units
    - Flexible billing cycles (monthly, quarterly, annual)
    - Real-time usage tracking and quotas
    - Automated notifications and alerts
    - Trial management and conversions
    - Enterprise custom pricing
    """
    
    def __init__(self):
        self.subscriptions: Dict[str, Subscription] = {}
        self.tier_configurations = self._initialize_tier_configurations()
        self.pricing_matrix = self._initialize_pricing_matrix()
        self.usage_records: List[UsageRecord] = []
        self._initialize_sample_subscriptions()
    
    def _initialize_tier_configurations(self) -> Dict[str, TierLimits]:
        """Initialize tier configurations with limits and features."""
        return {
            SubscriptionTier.STARTER.value: TierLimits(
                reasoning_units_per_month=1000,
                api_calls_per_month=10000,
                data_storage_gb=5,
                compute_time_hours=10,
                custom_rulesets=3,
                max_users=5,
                sla_availability=99.0,
                response_time_ms=5000,
                support_level="email",
                premium_features=["basic_analytics", "email_support"]
            ),
            SubscriptionTier.PROFESSIONAL.value: TierLimits(
                reasoning_units_per_month=10000,
                api_calls_per_month=100000,
                data_storage_gb=50,
                compute_time_hours=100,
                custom_rulesets=25,
                max_users=25,
                sla_availability=99.5,
                response_time_ms=2000,
                support_level="chat_email",
                premium_features=[
                    "basic_analytics", "advanced_analytics", "chat_support",
                    "custom_integrations", "audit_logs", "single_sign_on"
                ]
            ),
            SubscriptionTier.ENTERPRISE.value: TierLimits(
                reasoning_units_per_month=100000,
                api_calls_per_month=1000000,
                data_storage_gb=500,
                compute_time_hours=1000,
                custom_rulesets=100,
                max_users=100,
                sla_availability=99.9,
                response_time_ms=1000,
                support_level="phone_chat_email",
                premium_features=[
                    "basic_analytics", "advanced_analytics", "enterprise_analytics",
                    "phone_support", "dedicated_support", "custom_integrations",
                    "audit_logs", "single_sign_on", "role_based_access",
                    "white_labeling", "api_rate_limiting", "priority_support"
                ]
            ),
            SubscriptionTier.MISSION_CRITICAL.value: TierLimits(
                reasoning_units_per_month=1000000,
                api_calls_per_month=10000000,
                data_storage_gb=5000,
                compute_time_hours=10000,
                custom_rulesets=500,
                max_users=500,
                sla_availability=99.99,
                response_time_ms=500,
                support_level="24x7_dedicated",
                premium_features=[
                    "basic_analytics", "advanced_analytics", "enterprise_analytics",
                    "real_time_analytics", "24x7_support", "dedicated_support",
                    "custom_integrations", "audit_logs", "single_sign_on",
                    "role_based_access", "white_labeling", "api_rate_limiting",
                    "priority_support", "custom_sla", "dedicated_infrastructure",
                    "disaster_recovery", "compliance_certification"
                ]
            )
        }
    
    def _initialize_pricing_matrix(self) -> Dict[str, Dict[str, Any]]:
        """Initialize pricing matrix for all tiers and billing cycles."""
        return {
            SubscriptionTier.STARTER.value: {
                BillingCycle.MONTHLY.value: {
                    "base_price": Decimal("99.00"),
                    "reasoning_unit_overage": Decimal("0.10"),
                    "api_call_overage": Decimal("0.001"),
                    "storage_overage_per_gb": Decimal("2.00"),
                    "discount": 0.0
                },
                BillingCycle.QUARTERLY.value: {
                    "base_price": Decimal("267.30"),  # 10% discount
                    "reasoning_unit_overage": Decimal("0.09"),
                    "api_call_overage": Decimal("0.0009"),
                    "storage_overage_per_gb": Decimal("1.80"),
                    "discount": 10.0
                },
                BillingCycle.ANNUALLY.value: {
                    "base_price": Decimal("950.40"),  # 20% discount
                    "reasoning_unit_overage": Decimal("0.08"),
                    "api_call_overage": Decimal("0.0008"),
                    "storage_overage_per_gb": Decimal("1.60"),
                    "discount": 20.0
                }
            },
            SubscriptionTier.PROFESSIONAL.value: {
                BillingCycle.MONTHLY.value: {
                    "base_price": Decimal("299.00"),
                    "reasoning_unit_overage": Decimal("0.08"),
                    "api_call_overage": Decimal("0.0008"),
                    "storage_overage_per_gb": Decimal("1.50"),
                    "discount": 0.0
                },
                BillingCycle.QUARTERLY.value: {
                    "base_price": Decimal("807.30"),  # 10% discount
                    "reasoning_unit_overage": Decimal("0.072"),
                    "api_call_overage": Decimal("0.00072"),
                    "storage_overage_per_gb": Decimal("1.35"),
                    "discount": 10.0
                },
                BillingCycle.ANNUALLY.value: {
                    "base_price": Decimal("2870.40"),  # 20% discount
                    "reasoning_unit_overage": Decimal("0.064"),
                    "api_call_overage": Decimal("0.00064"),
                    "storage_overage_per_gb": Decimal("1.20"),
                    "discount": 20.0
                }
            },
            SubscriptionTier.ENTERPRISE.value: {
                BillingCycle.MONTHLY.value: {
                    "base_price": Decimal("999.00"),
                    "reasoning_unit_overage": Decimal("0.05"),
                    "api_call_overage": Decimal("0.0005"),
                    "storage_overage_per_gb": Decimal("1.00"),
                    "discount": 0.0
                },
                BillingCycle.QUARTERLY.value: {
                    "base_price": Decimal("2697.30"),  # 10% discount
                    "reasoning_unit_overage": Decimal("0.045"),
                    "api_call_overage": Decimal("0.00045"),
                    "storage_overage_per_gb": Decimal("0.90"),
                    "discount": 10.0
                },
                BillingCycle.ANNUALLY.value: {
                    "base_price": Decimal("9590.40"),  # 20% discount
                    "reasoning_unit_overage": Decimal("0.04"),
                    "api_call_overage": Decimal("0.0004"),
                    "storage_overage_per_gb": Decimal("0.80"),
                    "discount": 20.0
                }
            },
            SubscriptionTier.MISSION_CRITICAL.value: {
                BillingCycle.MONTHLY.value: {
                    "base_price": Decimal("2999.00"),
                    "reasoning_unit_overage": Decimal("0.03"),
                    "api_call_overage": Decimal("0.0003"),
                    "storage_overage_per_gb": Decimal("0.50"),
                    "discount": 0.0
                },
                BillingCycle.QUARTERLY.value: {
                    "base_price": Decimal("8097.30"),  # 10% discount
                    "reasoning_unit_overage": Decimal("0.027"),
                    "api_call_overage": Decimal("0.00027"),
                    "storage_overage_per_gb": Decimal("0.45"),
                    "discount": 10.0
                },
                BillingCycle.ANNUALLY.value: {
                    "base_price": Decimal("28790.40"),  # 20% discount
                    "reasoning_unit_overage": Decimal("0.024"),
                    "api_call_overage": Decimal("0.00024"),
                    "storage_overage_per_gb": Decimal("0.40"),
                    "discount": 20.0
                }
            }
        }
    
    def _initialize_sample_subscriptions(self):
        """Initialize with sample subscriptions for demonstration."""
        sample_customers = [
            {
                "customer_id": "customer_demo_001",
                "organization_name": "TechStartup Inc.",
                "tier": SubscriptionTier.PROFESSIONAL,
                "billing_cycle": BillingCycle.MONTHLY,
                "status": SubscriptionStatus.ACTIVE
            },
            {
                "customer_id": "customer_demo_002", 
                "organization_name": "Enterprise Corp",
                "tier": SubscriptionTier.ENTERPRISE,
                "billing_cycle": BillingCycle.ANNUALLY,
                "status": SubscriptionStatus.ACTIVE
            },
            {
                "customer_id": "customer_demo_003",
                "organization_name": "Mission Critical Systems",
                "tier": SubscriptionTier.MISSION_CRITICAL,
                "billing_cycle": BillingCycle.MONTHLY,
                "status": SubscriptionStatus.ACTIVE
            }
        ]
        
        for customer_data in sample_customers:
            try:
                self.create_subscription(
                    customer_id=customer_data["customer_id"],
                    organization_name=customer_data["organization_name"],
                    tier=customer_data["tier"],
                    billing_cycle=customer_data["billing_cycle"],
                    start_trial=False
                )
            except Exception:
                # Subscription might already exist
                pass
    
    def create_subscription(
        self,
        customer_id: str,
        organization_name: str,
        tier: SubscriptionTier,
        billing_cycle: BillingCycle = BillingCycle.MONTHLY,
        start_trial: bool = True,
        custom_limits: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new subscription.
        
        Args:
            customer_id: Unique customer identifier
            organization_name: Organization name
            tier: Subscription tier
            billing_cycle: Billing cycle preference
            start_trial: Whether to start with trial
            custom_limits: Custom limits for enterprise customers
            
        Returns:
            str: Subscription ID
        """
        subscription_id = f"sub_{uuid.uuid4().hex[:12]}"
        
        # Get tier configuration and pricing
        tier_limits = self.tier_configurations[tier.value]
        pricing = self.pricing_matrix[tier.value][billing_cycle.value]
        
        # Calculate trial and billing dates
        start_date = datetime.now(timezone.utc)
        trial_end_date = start_date + timedelta(days=14) if start_trial else None
        
        if billing_cycle == BillingCycle.MONTHLY:
            next_billing_date = start_date + timedelta(days=30)
        elif billing_cycle == BillingCycle.QUARTERLY:
            next_billing_date = start_date + timedelta(days=90)
        else:  # ANNUALLY
            next_billing_date = start_date + timedelta(days=365)
        
        # Create subscription
        subscription = Subscription(
            subscription_id=subscription_id,
            customer_id=customer_id,
            organization_name=organization_name,
            tier=tier,
            status=SubscriptionStatus.TRIAL if start_trial else SubscriptionStatus.ACTIVE,
            billing_cycle=billing_cycle,
            base_price=pricing["base_price"],
            usage_based_pricing={
                "reasoning_unit_overage": pricing["reasoning_unit_overage"],
                "api_call_overage": pricing["api_call_overage"],
                "storage_overage_per_gb": pricing["storage_overage_per_gb"]
            },
            tier_limits=tier_limits,
            custom_limits=custom_limits or {},
            start_date=start_date,
            end_date=None,
            trial_end_date=trial_end_date,
            next_billing_date=next_billing_date,
            enabled_features=set(tier_limits.premium_features)
        )
        
        self.subscriptions[subscription_id] = subscription
        
        # Log subscription creation
        audit_logger.log_event(
            event_type=AuditEventType.ADMIN_ACTION,
            action="create_subscription",
            result="success",
            details={
                "subscription_id": subscription_id,
                "customer_id": customer_id,
                "organization_name": organization_name,
                "tier": tier.value,
                "billing_cycle": billing_cycle.value,
                "base_price": float(subscription.base_price),
                "trial": start_trial
            },
            user_id=customer_id,
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="low"
        )
        
        return subscription_id
    
    def record_usage(
        self,
        customer_id: str,
        usage_type: UsageType,
        quantity: Decimal,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Record usage for a customer.
        
        Args:
            customer_id: Customer ID
            usage_type: Type of usage
            quantity: Usage quantity
            metadata: Additional metadata
            
        Returns:
            str: Usage record ID
        """
        # Find customer subscription
        subscription = None
        for sub in self.subscriptions.values():
            if sub.customer_id == customer_id and sub.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIAL]:
                subscription = sub
                break
        
        if not subscription:
            raise ValueError(f"No active subscription found for customer: {customer_id}")
        
        # Get unit pricing
        pricing = self.pricing_matrix[subscription.tier.value][subscription.billing_cycle.value]
        unit_price = Decimal("0.00")
        
        if usage_type == UsageType.REASONING_UNITS:
            unit_price = pricing["reasoning_unit_overage"]
        elif usage_type == UsageType.API_CALLS:
            unit_price = pricing["api_call_overage"]
        elif usage_type == UsageType.DATA_STORAGE:
            unit_price = pricing["storage_overage_per_gb"]
        
        # Create usage record
        usage_id = f"usage_{uuid.uuid4().hex[:8]}"
        usage_record = UsageRecord(
            usage_id=usage_id,
            customer_id=customer_id,
            usage_type=usage_type,
            quantity=quantity,
            unit_price=unit_price,
            timestamp=datetime.now(timezone.utc),
            metadata=metadata or {}
        )
        
        self.usage_records.append(usage_record)
        
        # Update subscription current usage
        usage_key = usage_type.value
        if usage_key not in subscription.current_usage:
            subscription.current_usage[usage_key] = Decimal("0")
        
        subscription.current_usage[usage_key] += quantity
        subscription.updated_at = datetime.now(timezone.utc)
        
        # Check for quota violations
        self._check_usage_limits(subscription, usage_type, quantity)
        
        return usage_id
    
    def _check_usage_limits(self, subscription: Subscription, usage_type: UsageType, quantity: Decimal):
        """Check if usage exceeds limits and send alerts."""
        current_usage = subscription.current_usage.get(usage_type.value, Decimal("0"))
        
        # Get limit based on usage type
        limit = 0
        if usage_type == UsageType.REASONING_UNITS:
            limit = subscription.tier_limits.reasoning_units_per_month
        elif usage_type == UsageType.API_CALLS:
            limit = subscription.tier_limits.api_calls_per_month
        elif usage_type == UsageType.DATA_STORAGE:
            limit = subscription.tier_limits.data_storage_gb
        
        if limit == 0:
            return
        
        usage_percentage = float(current_usage) / limit * 100
        
        # Send alerts at 80%, 90%, 100%
        alert_thresholds = [80, 90, 100]
        for threshold in alert_thresholds:
            alert_key = f"{usage_type.value}_{threshold}"
            
            if usage_percentage >= threshold and alert_key not in subscription.usage_alerts_sent:
                self._send_usage_alert(subscription, usage_type, usage_percentage, threshold)
                subscription.usage_alerts_sent.append(alert_key)
    
    def _send_usage_alert(
        self,
        subscription: Subscription,
        usage_type: UsageType,
        usage_percentage: float,
        threshold: int
    ):
        """Send usage alert to customer."""
        alert_data = {
            "subscription_id": subscription.subscription_id,
            "customer_id": subscription.customer_id,
            "organization_name": subscription.organization_name,
            "usage_type": usage_type.value,
            "usage_percentage": usage_percentage,
            "threshold": threshold,
            "tier": subscription.tier.value
        }
        
        # Log usage alert
        audit_logger.log_event(
            event_type=AuditEventType.ADMIN_ACTION,
            action="send_usage_alert",
            result="success",
            details=alert_data,
            user_id=subscription.customer_id,
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="medium" if threshold >= 90 else "low"
        )
    
    def get_subscription(self, subscription_id: str) -> Optional[Subscription]:
        """Get subscription by ID."""
        return self.subscriptions.get(subscription_id)
    
    def get_customer_subscription(self, customer_id: str) -> Optional[Subscription]:
        """Get active subscription for customer."""
        for subscription in self.subscriptions.values():
            if (subscription.customer_id == customer_id and 
                subscription.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIAL]):
                return subscription
        return None
    
    def calculate_monthly_bill(self, subscription_id: str) -> Dict[str, Any]:
        """
        Calculate monthly bill for subscription.
        
        Args:
            subscription_id: Subscription to calculate bill for
            
        Returns:
            Dict: Bill calculation details
        """
        subscription = self.subscriptions.get(subscription_id)
        if not subscription:
            raise ValueError(f"Subscription not found: {subscription_id}")
        
        # Calculate base charges
        base_charge = subscription.base_price
        
        # Calculate usage overages for current month
        current_month_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_usage_records = [
            record for record in self.usage_records
            if (record.customer_id == subscription.customer_id and 
                record.timestamp >= current_month_start)
        ]
        
        # Calculate overage charges
        overage_charges = {}
        total_overage = Decimal("0.00")
        
        for usage_type in UsageType:
            usage_records = [r for r in monthly_usage_records if r.usage_type == usage_type]
            total_usage = sum(r.quantity for r in usage_records)
            
            # Get included limits
            included = 0
            if usage_type == UsageType.REASONING_UNITS:
                included = subscription.tier_limits.reasoning_units_per_month
            elif usage_type == UsageType.API_CALLS:
                included = subscription.tier_limits.api_calls_per_month
            elif usage_type == UsageType.DATA_STORAGE:
                included = subscription.tier_limits.data_storage_gb
            
            # Calculate overage
            overage = max(0, total_usage - included)
            overage_cost = sum(r.quantity * r.unit_price for r in usage_records if total_usage > included)
            
            if overage > 0:
                overage_charges[usage_type.value] = {
                    "included": included,
                    "used": int(total_usage),
                    "overage": int(overage),
                    "cost": float(overage_cost)
                }
                total_overage += overage_cost
        
        # Calculate total
        subtotal = base_charge + total_overage
        tax_rate = Decimal("0.08")  # 8% tax
        tax_amount = subtotal * tax_rate
        total_amount = subtotal + tax_amount
        
        return {
            "subscription_id": subscription_id,
            "billing_period": {
                "start": current_month_start.isoformat(),
                "end": (current_month_start + timedelta(days=32)).replace(day=1).isoformat()
            },
            "charges": {
                "base_charge": float(base_charge),
                "overage_charges": overage_charges,
                "total_overage": float(total_overage),
                "subtotal": float(subtotal),
                "tax_rate": float(tax_rate),
                "tax_amount": float(tax_amount),
                "total_amount": float(total_amount)
            },
            "tier_info": {
                "tier": subscription.tier.value,
                "billing_cycle": subscription.billing_cycle.value,
                "included_features": list(subscription.enabled_features)
            }
        }
    
    def get_pricing_calculator(self) -> Dict[str, Any]:
        """Get pricing calculator information for all tiers."""
        return {
            "tiers": {
                tier.value: {
                    "name": tier.value.title(),
                    "limits": {
                        "reasoning_units_per_month": self.tier_configurations[tier.value].reasoning_units_per_month,
                        "api_calls_per_month": self.tier_configurations[tier.value].api_calls_per_month,
                        "data_storage_gb": self.tier_configurations[tier.value].data_storage_gb,
                        "max_users": self.tier_configurations[tier.value].max_users,
                        "sla_availability": self.tier_configurations[tier.value].sla_availability,
                        "response_time_ms": self.tier_configurations[tier.value].response_time_ms,
                        "support_level": self.tier_configurations[tier.value].support_level
                    },
                    "pricing": {
                        billing_cycle.value: {
                            "base_price": float(self.pricing_matrix[tier.value][billing_cycle.value]["base_price"]),
                            "reasoning_unit_overage": float(self.pricing_matrix[tier.value][billing_cycle.value]["reasoning_unit_overage"]),
                            "api_call_overage": float(self.pricing_matrix[tier.value][billing_cycle.value]["api_call_overage"]),
                            "storage_overage_per_gb": float(self.pricing_matrix[tier.value][billing_cycle.value]["storage_overage_per_gb"]),
                            "discount": self.pricing_matrix[tier.value][billing_cycle.value]["discount"]
                        }
                        for billing_cycle in BillingCycle
                    },
                    "features": self.tier_configurations[tier.value].premium_features
                }
                for tier in SubscriptionTier
            },
            "usage_types": {
                usage_type.value: {
                    "name": usage_type.value.replace("_", " ").title(),
                    "unit": "units" if usage_type == UsageType.REASONING_UNITS else "calls" if usage_type == UsageType.API_CALLS else "GB"
                }
                for usage_type in UsageType
            }
        }
    
    def get_subscription_dashboard(self) -> Dict[str, Any]:
        """Get subscription management dashboard."""
        total_subscriptions = len(self.subscriptions)
        
        # Count by status
        status_counts = {}
        for status in SubscriptionStatus:
            status_counts[status.value] = sum(
                1 for s in self.subscriptions.values() if s.status == status
            )
        
        # Count by tier
        tier_counts = {}
        for tier in SubscriptionTier:
            tier_counts[tier.value] = sum(
                1 for s in self.subscriptions.values() if s.tier == tier
            )
        
        # Calculate revenue metrics
        monthly_recurring_revenue = sum(
            s.base_price for s in self.subscriptions.values()
            if s.status == SubscriptionStatus.ACTIVE and s.billing_cycle == BillingCycle.MONTHLY
        )
        
        annual_recurring_revenue = monthly_recurring_revenue * 12
        
        # Usage metrics
        total_usage_this_month = sum(
            record.quantity * record.unit_price
            for record in self.usage_records
            if record.timestamp >= datetime.now(timezone.utc).replace(day=1)
        )
        
        return {
            "subscription_metrics": {
                "total_subscriptions": total_subscriptions,
                "active_subscriptions": status_counts.get("active", 0),
                "trial_subscriptions": status_counts.get("trial", 0),
                "monthly_recurring_revenue": float(monthly_recurring_revenue),
                "annual_recurring_revenue": float(annual_recurring_revenue)
            },
            "distribution": {
                "by_status": status_counts,
                "by_tier": tier_counts
            },
            "usage_metrics": {
                "total_usage_revenue_this_month": float(total_usage_this_month),
                "total_usage_records": len(self.usage_records),
                "average_usage_per_customer": float(total_usage_this_month / total_subscriptions) if total_subscriptions else 0
            },
            "growth_metrics": {
                "new_subscriptions_this_month": sum(
                    1 for s in self.subscriptions.values()
                    if s.created_at >= datetime.now(timezone.utc).replace(day=1)
                ),
                "trial_conversion_rate": 85.5,  # Mock data
                "churn_rate": 2.3  # Mock data
            }
        }


# Global subscription manager instance
subscription_manager = SubscriptionManager()
