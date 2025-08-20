"""
Quota Manager for XReason
Manages usage quotas, limits, and violations for billing.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class QuotaType(str, Enum):
    """Types of quotas that can be enforced."""
    REASONING_UNITS = "reasoning_units"
    API_CALLS = "api_calls"
    STORAGE_BYTES = "storage_bytes"
    COMPUTE_SECONDS = "compute_seconds"
    LLM_TOKENS = "llm_tokens"
    PROLOG_QUERIES = "prolog_queries"
    GRAPH_OPERATIONS = "graph_operations"
    USERS = "users"
    PROJECTS = "projects"
    RULESETS = "rulesets"


class QuotaPeriod(str, Enum):
    """Quota periods."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class QuotaViolationLevel(str, Enum):
    """Levels of quota violations."""
    WARNING = "warning"
    SOFT_LIMIT = "soft_limit"
    HARD_LIMIT = "hard_limit"
    CRITICAL = "critical"


@dataclass
class QuotaViolation:
    """Represents a quota violation."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    user_id: Optional[str] = None
    quota_type: QuotaType = QuotaType.REASONING_UNITS
    current_usage: float = 0.0
    limit: float = 0.0
    violation_level: QuotaViolationLevel = QuotaViolationLevel.WARNING
    message: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "quota_type": self.quota_type.value,
            "current_usage": self.current_usage,
            "limit": self.limit,
            "violation_level": self.violation_level.value,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QuotaViolation':
        """Create from dictionary."""
        violation = cls(
            id=data.get("id", str(uuid.uuid4())),
            tenant_id=data.get("tenant_id", ""),
            user_id=data.get("user_id"),
            quota_type=QuotaType(data.get("quota_type", "reasoning_units")),
            current_usage=data.get("current_usage", 0.0),
            limit=data.get("limit", 0.0),
            violation_level=QuotaViolationLevel(data.get("violation_level", "warning")),
            message=data.get("message", ""),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.utcnow().isoformat())),
            resolved=data.get("resolved", False),
            metadata=data.get("metadata", {})
        )
        
        if data.get("resolved_at"):
            violation.resolved_at = datetime.fromisoformat(data["resolved_at"])
        
        return violation


@dataclass
class QuotaLimit:
    """Defines a quota limit for a tenant."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    quota_type: QuotaType = QuotaType.REASONING_UNITS
    period: QuotaPeriod = QuotaPeriod.MONTHLY
    limit: float = 0.0
    soft_limit: float = 0.0  # Warning threshold
    hard_limit: float = 0.0  # Blocking threshold
    current_usage: float = 0.0
    reset_date: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Set default limits if not provided."""
        if self.soft_limit == 0.0:
            self.soft_limit = self.limit * 0.8
        if self.hard_limit == 0.0:
            self.hard_limit = self.limit * 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "quota_type": self.quota_type.value,
            "period": self.period.value,
            "limit": self.limit,
            "soft_limit": self.soft_limit,
            "hard_limit": self.hard_limit,
            "current_usage": self.current_usage,
            "reset_date": self.reset_date.isoformat(),
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QuotaLimit':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            tenant_id=data.get("tenant_id", ""),
            quota_type=QuotaType(data.get("quota_type", "reasoning_units")),
            period=QuotaPeriod(data.get("period", "monthly")),
            limit=data.get("limit", 0.0),
            soft_limit=data.get("soft_limit", 0.0),
            hard_limit=data.get("hard_limit", 0.0),
            current_usage=data.get("current_usage", 0.0),
            reset_date=datetime.fromisoformat(data.get("reset_date", datetime.utcnow().isoformat())),
            is_active=data.get("is_active", True),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.utcnow().isoformat()))
        )


class QuotaManager:
    """Manages quotas and usage limits for tenants."""
    
    def __init__(self):
        self.quotas: Dict[str, Dict[QuotaType, QuotaLimit]] = {}
        self.violations: Dict[str, List[QuotaViolation]] = {}
        self.logger = logging.getLogger(__name__)
    
    def set_quota(self, tenant_id: str, quota_type: QuotaType, limit: float,
                  period: QuotaPeriod = QuotaPeriod.MONTHLY,
                  soft_limit: Optional[float] = None,
                  hard_limit: Optional[float] = None) -> QuotaLimit:
        """Set a quota limit for a tenant."""
        try:
            if tenant_id not in self.quotas:
                self.quotas[tenant_id] = {}
            
            quota = QuotaLimit(
                tenant_id=tenant_id,
                quota_type=quota_type,
                period=period,
                limit=limit,
                soft_limit=soft_limit or (limit * 0.8),
                hard_limit=hard_limit or limit
            )
            
            self.quotas[tenant_id][quota_type] = quota
            
            self.logger.info(f"Set quota for tenant {tenant_id}: {quota_type.value} = {limit}")
            return quota
            
        except Exception as e:
            self.logger.error(f"Error setting quota: {e}")
            raise
    
    def get_quota(self, tenant_id: str, quota_type: QuotaType) -> Optional[QuotaLimit]:
        """Get a quota limit for a tenant."""
        return self.quotas.get(tenant_id, {}).get(quota_type)
    
    def get_all_quotas(self, tenant_id: str) -> Dict[QuotaType, QuotaLimit]:
        """Get all quotas for a tenant."""
        return self.quotas.get(tenant_id, {})
    
    def update_usage(self, tenant_id: str, quota_type: QuotaType, 
                    usage_delta: float, user_id: Optional[str] = None) -> bool:
        """Update usage for a quota and check for violations."""
        try:
            quota = self.get_quota(tenant_id, quota_type)
            if not quota:
                return True  # No quota set, allow usage
            
            # Check if quota period has reset
            if datetime.utcnow() >= quota.reset_date:
                self._reset_quota(quota)
            
            # Update usage
            old_usage = quota.current_usage
            quota.current_usage += usage_delta
            quota.updated_at = datetime.utcnow()
            
            # Check for violations
            violation = self._check_violation(quota, user_id)
            if violation:
                self._record_violation(violation)
                
                # Handle hard limit violations
                if violation.violation_level == QuotaViolationLevel.HARD_LIMIT:
                    self.logger.warning(f"Hard limit violation for tenant {tenant_id}: {quota_type.value}")
                    return False  # Block the operation
            
            self.logger.debug(f"Updated usage for tenant {tenant_id}: {quota_type.value} = {quota.current_usage}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating usage: {e}")
            return False
    
    def check_usage(self, tenant_id: str, quota_type: QuotaType, 
                   required_amount: float = 1.0) -> bool:
        """Check if usage is allowed without updating."""
        try:
            quota = self.get_quota(tenant_id, quota_type)
            if not quota:
                return True  # No quota set, allow usage
            
            # Check if quota period has reset
            if datetime.utcnow() >= quota.reset_date:
                self._reset_quota(quota)
            
            # Check if usage would exceed hard limit
            if quota.current_usage + required_amount > quota.hard_limit:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking usage: {e}")
            return False
    
    def get_usage_summary(self, tenant_id: str) -> Dict[str, Any]:
        """Get usage summary for a tenant."""
        try:
            quotas = self.get_all_quotas(tenant_id)
            summary = {
                "tenant_id": tenant_id,
                "quotas": {},
                "violations": self.get_active_violations(tenant_id)
            }
            
            for quota_type, quota in quotas.items():
                summary["quotas"][quota_type.value] = {
                    "current_usage": quota.current_usage,
                    "limit": quota.limit,
                    "soft_limit": quota.soft_limit,
                    "hard_limit": quota.hard_limit,
                    "period": quota.period.value,
                    "reset_date": quota.reset_date.isoformat(),
                    "usage_percentage": (quota.current_usage / quota.limit * 100) if quota.limit > 0 else 0,
                    "remaining": max(0, quota.limit - quota.current_usage)
                }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error getting usage summary: {e}")
            return {}
    
    def get_active_violations(self, tenant_id: str) -> List[QuotaViolation]:
        """Get active violations for a tenant."""
        violations = self.violations.get(tenant_id, [])
        return [v for v in violations if not v.resolved]
    
    def resolve_violation(self, violation_id: str, tenant_id: str) -> bool:
        """Mark a violation as resolved."""
        try:
            violations = self.violations.get(tenant_id, [])
            for violation in violations:
                if violation.id == violation_id:
                    violation.resolved = True
                    violation.resolved_at = datetime.utcnow()
                    self.logger.info(f"Resolved violation {violation_id} for tenant {tenant_id}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error resolving violation: {e}")
            return False
    
    def _check_violation(self, quota: QuotaLimit, user_id: Optional[str] = None) -> Optional[QuotaViolation]:
        """Check if quota usage violates limits."""
        if quota.current_usage > quota.hard_limit:
            return QuotaViolation(
                tenant_id=quota.tenant_id,
                user_id=user_id,
                quota_type=quota.quota_type,
                current_usage=quota.current_usage,
                limit=quota.limit,
                violation_level=QuotaViolationLevel.HARD_LIMIT,
                message=f"Hard limit exceeded: {quota.current_usage} > {quota.hard_limit}"
            )
        elif quota.current_usage > quota.limit:
            return QuotaViolation(
                tenant_id=quota.tenant_id,
                user_id=user_id,
                quota_type=quota.quota_type,
                current_usage=quota.current_usage,
                limit=quota.limit,
                violation_level=QuotaViolationLevel.SOFT_LIMIT,
                message=f"Soft limit exceeded: {quota.current_usage} > {quota.limit}"
            )
        elif quota.current_usage > quota.soft_limit:
            return QuotaViolation(
                tenant_id=quota.tenant_id,
                user_id=user_id,
                quota_type=quota.quota_type,
                current_usage=quota.current_usage,
                limit=quota.limit,
                violation_level=QuotaViolationLevel.WARNING,
                message=f"Approaching limit: {quota.current_usage} > {quota.soft_limit}"
            )
        
        return None
    
    def _record_violation(self, violation: QuotaViolation) -> None:
        """Record a quota violation."""
        try:
            tenant_id = violation.tenant_id
            if tenant_id not in self.violations:
                self.violations[tenant_id] = []
            
            self.violations[tenant_id].append(violation)
            
            self.logger.warning(f"Quota violation recorded: {violation.message}")
            
        except Exception as e:
            self.logger.error(f"Error recording violation: {e}")
    
    def _reset_quota(self, quota: QuotaLimit) -> None:
        """Reset quota usage for a new period."""
        try:
            # Calculate next reset date based on period
            if quota.period == QuotaPeriod.DAILY:
                quota.reset_date = datetime.utcnow() + timedelta(days=1)
            elif quota.period == QuotaPeriod.WEEKLY:
                quota.reset_date = datetime.utcnow() + timedelta(weeks=1)
            elif quota.period == QuotaPeriod.MONTHLY:
                # Approximate - add 30 days
                quota.reset_date = datetime.utcnow() + timedelta(days=30)
            elif quota.period == QuotaPeriod.YEARLY:
                quota.reset_date = datetime.utcnow() + timedelta(days=365)
            
            # Reset usage
            quota.current_usage = 0.0
            quota.updated_at = datetime.utcnow()
            
            self.logger.info(f"Reset quota {quota.quota_type.value} for tenant {quota.tenant_id}")
            
        except Exception as e:
            self.logger.error(f"Error resetting quota: {e}")
    
    def set_default_quotas(self, tenant_id: str, subscription_tier: str) -> None:
        """Set default quotas based on subscription tier."""
        try:
            # Define default quotas by tier
            default_quotas = {
                "starter": {
                    QuotaType.REASONING_UNITS: 1000,
                    QuotaType.API_CALLS: 10000,
                    QuotaType.STORAGE_BYTES: 1024 * 1024 * 1024,  # 1GB
                    QuotaType.LLM_TOKENS: 100000,
                    QuotaType.USERS: 5,
                    QuotaType.PROJECTS: 3,
                    QuotaType.RULESETS: 10
                },
                "professional": {
                    QuotaType.REASONING_UNITS: 10000,
                    QuotaType.API_CALLS: 100000,
                    QuotaType.STORAGE_BYTES: 10 * 1024 * 1024 * 1024,  # 10GB
                    QuotaType.LLM_TOKENS: 1000000,
                    QuotaType.USERS: 25,
                    QuotaType.PROJECTS: 15,
                    QuotaType.RULESETS: 50
                },
                "enterprise": {
                    QuotaType.REASONING_UNITS: 100000,
                    QuotaType.API_CALLS: 1000000,
                    QuotaType.STORAGE_BYTES: 100 * 1024 * 1024 * 1024,  # 100GB
                    QuotaType.LLM_TOKENS: 10000000,
                    QuotaType.USERS: 100,
                    QuotaType.PROJECTS: 50,
                    QuotaType.RULESETS: 200
                },
                "mission_critical": {
                    QuotaType.REASONING_UNITS: 1000000,
                    QuotaType.API_CALLS: 10000000,
                    QuotaType.STORAGE_BYTES: 1024 * 1024 * 1024 * 1024,  # 1TB
                    QuotaType.LLM_TOKENS: 100000000,
                    QuotaType.USERS: 500,
                    QuotaType.PROJECTS: 200,
                    QuotaType.RULESETS: 1000
                }
            }
            
            quotas = default_quotas.get(subscription_tier.lower(), default_quotas["starter"])
            
            for quota_type, limit in quotas.items():
                self.set_quota(tenant_id, quota_type, limit)
            
            self.logger.info(f"Set default quotas for tenant {tenant_id} (tier: {subscription_tier})")
            
        except Exception as e:
            self.logger.error(f"Error setting default quotas: {e}")
    
    def clear_old_violations(self, days_to_keep: int = 90) -> None:
        """Clear old resolved violations."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            
            for tenant_id in list(self.violations.keys()):
                self.violations[tenant_id] = [
                    v for v in self.violations[tenant_id]
                    if not v.resolved or v.timestamp >= cutoff_date
                ]
                
                if not self.violations[tenant_id]:
                    del self.violations[tenant_id]
            
            self.logger.info(f"Cleared violations older than {days_to_keep} days")
            
        except Exception as e:
            self.logger.error(f"Error clearing old violations: {e}")


# Global quota manager instance
quota_manager = QuotaManager()
