"""
Usage Metering for XReason
Tracks reasoning units, API calls, and usage metrics for billing.
"""

import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class UsageMetricType(str, Enum):
    """Types of usage metrics."""
    REASONING_UNITS = "reasoning_units"
    API_CALLS = "api_calls"
    STORAGE_BYTES = "storage_bytes"
    COMPUTE_SECONDS = "compute_seconds"
    LLM_TOKENS = "llm_tokens"
    PROLOG_QUERIES = "prolog_queries"
    GRAPH_OPERATIONS = "graph_operations"


class ReasoningUnitType(str, Enum):
    """Types of reasoning units."""
    BASIC_REASONING = "basic_reasoning"
    ADVANCED_REASONING = "advanced_reasoning"
    COMPLIANCE_CHECK = "compliance_check"
    FINANCIAL_ANALYSIS = "financial_analysis"
    HEALTHCARE_VALIDATION = "healthcare_validation"
    LEGAL_REVIEW = "legal_review"
    SCIENTIFIC_VALIDATION = "scientific_validation"
    CUSTOM_RULESET = "custom_ruleset"


@dataclass
class ReasoningUnit:
    """Represents a single reasoning unit for billing."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: ReasoningUnitType = ReasoningUnitType.BASIC_REASONING
    complexity: float = 1.0  # Multiplier for billing
    duration_ms: float = 0.0
    token_count: int = 0
    rule_count: int = 0
    confidence_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "type": self.type.value,
            "complexity": self.complexity,
            "duration_ms": self.duration_ms,
            "token_count": self.token_count,
            "rule_count": self.rule_count,
            "confidence_score": self.confidence_score,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReasoningUnit':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            type=ReasoningUnitType(data.get("type", "basic_reasoning")),
            complexity=data.get("complexity", 1.0),
            duration_ms=data.get("duration_ms", 0.0),
            token_count=data.get("token_count", 0),
            rule_count=data.get("rule_count", 0),
            confidence_score=data.get("confidence_score", 0.0),
            metadata=data.get("metadata", {}),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.utcnow().isoformat()))
        )


@dataclass
class UsageMetric:
    """Represents a usage metric for tracking."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    user_id: Optional[str] = None
    metric_type: UsageMetricType = UsageMetricType.REASONING_UNITS
    value: float = 0.0
    unit: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "metric_type": self.metric_type.value,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UsageMetric':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            tenant_id=data.get("tenant_id", ""),
            user_id=data.get("user_id"),
            metric_type=UsageMetricType(data.get("metric_type", "reasoning_units")),
            value=data.get("value", 0.0),
            unit=data.get("unit", ""),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.utcnow().isoformat())),
            metadata=data.get("metadata", {})
        )


class UsageMeter:
    """Meter for tracking usage and reasoning units."""
    
    def __init__(self):
        self.metrics: Dict[str, List[UsageMetric]] = {}
        self.reasoning_units: Dict[str, List[ReasoningUnit]] = {}
        self.tenant_usage: Dict[str, Dict[str, float]] = {}
        self.logger = logging.getLogger(__name__)
    
    def record_reasoning_unit(self, tenant_id: str, reasoning_unit: ReasoningUnit, 
                            user_id: Optional[str] = None) -> None:
        """Record a reasoning unit for billing."""
        try:
            if tenant_id not in self.reasoning_units:
                self.reasoning_units[tenant_id] = []
            
            self.reasoning_units[tenant_id].append(reasoning_unit)
            
            # Update tenant usage
            if tenant_id not in self.tenant_usage:
                self.tenant_usage[tenant_id] = {}
            
            unit_type = reasoning_unit.type.value
            if unit_type not in self.tenant_usage[tenant_id]:
                self.tenant_usage[tenant_id][unit_type] = 0.0
            
            self.tenant_usage[tenant_id][unit_type] += reasoning_unit.complexity
            
            # Record metric
            metric = UsageMetric(
                tenant_id=tenant_id,
                user_id=user_id,
                metric_type=UsageMetricType.REASONING_UNITS,
                value=reasoning_unit.complexity,
                unit="RU",
                metadata={
                    "reasoning_unit_id": reasoning_unit.id,
                    "type": reasoning_unit.type.value,
                    "duration_ms": reasoning_unit.duration_ms,
                    "token_count": reasoning_unit.token_count,
                    "rule_count": reasoning_unit.rule_count
                }
            )
            self.record_metric(metric)
            
            self.logger.info(f"Recorded reasoning unit: {reasoning_unit.id} for tenant: {tenant_id}")
            
        except Exception as e:
            self.logger.error(f"Error recording reasoning unit: {e}")
    
    def record_metric(self, metric: UsageMetric) -> None:
        """Record a usage metric."""
        try:
            metric_key = f"{metric.tenant_id}_{metric.metric_type.value}"
            if metric_key not in self.metrics:
                self.metrics[metric_key] = []
            
            self.metrics[metric_key].append(metric)
            
            self.logger.debug(f"Recorded metric: {metric.metric_type.value} = {metric.value} {metric.unit}")
            
        except Exception as e:
            self.logger.error(f"Error recording metric: {e}")
    
    def record_api_call(self, tenant_id: str, endpoint: str, duration_ms: float, 
                       user_id: Optional[str] = None) -> None:
        """Record an API call."""
        try:
            metric = UsageMetric(
                tenant_id=tenant_id,
                user_id=user_id,
                metric_type=UsageMetricType.API_CALLS,
                value=1.0,
                unit="calls",
                metadata={
                    "endpoint": endpoint,
                    "duration_ms": duration_ms
                }
            )
            self.record_metric(metric)
            
        except Exception as e:
            self.logger.error(f"Error recording API call: {e}")
    
    def record_llm_usage(self, tenant_id: str, token_count: int, model: str,
                        user_id: Optional[str] = None) -> None:
        """Record LLM token usage."""
        try:
            metric = UsageMetric(
                tenant_id=tenant_id,
                user_id=user_id,
                metric_type=UsageMetricType.LLM_TOKENS,
                value=float(token_count),
                unit="tokens",
                metadata={
                    "model": model
                }
            )
            self.record_metric(metric)
            
        except Exception as e:
            self.logger.error(f"Error recording LLM usage: {e}")
    
    def record_storage_usage(self, tenant_id: str, bytes_used: int,
                           user_id: Optional[str] = None) -> None:
        """Record storage usage."""
        try:
            metric = UsageMetric(
                tenant_id=tenant_id,
                user_id=user_id,
                metric_type=UsageMetricType.STORAGE_BYTES,
                value=float(bytes_used),
                unit="bytes",
                metadata={}
            )
            self.record_metric(metric)
            
        except Exception as e:
            self.logger.error(f"Error recording storage usage: {e}")
    
    def get_tenant_usage(self, tenant_id: str, start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None) -> Dict[str, float]:
        """Get usage summary for a tenant."""
        try:
            if start_date is None:
                start_date = datetime.utcnow() - timedelta(days=30)
            if end_date is None:
                end_date = datetime.utcnow()
            
            usage_summary = {}
            
            # Get reasoning units
            if tenant_id in self.reasoning_units:
                units = [
                    unit for unit in self.reasoning_units[tenant_id]
                    if start_date <= unit.timestamp <= end_date
                ]
                
                for unit_type in ReasoningUnitType:
                    type_units = [u for u in units if u.type == unit_type]
                    usage_summary[f"{unit_type.value}_units"] = sum(u.complexity for u in type_units)
                    usage_summary[f"{unit_type.value}_count"] = len(type_units)
            
            # Get metrics
            for metric_type in UsageMetricType:
                metric_key = f"{tenant_id}_{metric_type.value}"
                if metric_key in self.metrics:
                    metrics = [
                        m for m in self.metrics[metric_key]
                        if start_date <= m.timestamp <= end_date
                    ]
                    usage_summary[f"{metric_type.value}_total"] = sum(m.value for m in metrics)
                    usage_summary[f"{metric_type.value}_count"] = len(metrics)
            
            return usage_summary
            
        except Exception as e:
            self.logger.error(f"Error getting tenant usage: {e}")
            return {}
    
    def get_user_usage(self, tenant_id: str, user_id: str, 
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None) -> Dict[str, float]:
        """Get usage summary for a specific user."""
        try:
            if start_date is None:
                start_date = datetime.utcnow() - timedelta(days=30)
            if end_date is None:
                end_date = datetime.utcnow()
            
            usage_summary = {}
            
            # Get user-specific metrics
            for metric_type in UsageMetricType:
                metric_key = f"{tenant_id}_{metric_type.value}"
                if metric_key in self.metrics:
                    metrics = [
                        m for m in self.metrics[metric_key]
                        if m.user_id == user_id and start_date <= m.timestamp <= end_date
                    ]
                    usage_summary[f"{metric_type.value}_total"] = sum(m.value for m in metrics)
                    usage_summary[f"{metric_type.value}_count"] = len(metrics)
            
            return usage_summary
            
        except Exception as e:
            self.logger.error(f"Error getting user usage: {e}")
            return {}
    
    def calculate_billing_units(self, tenant_id: str, start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None) -> float:
        """Calculate total billing units for a tenant."""
        try:
            usage = self.get_tenant_usage(tenant_id, start_date, end_date)
            
            # Calculate total reasoning units
            total_units = 0.0
            for unit_type in ReasoningUnitType:
                total_units += usage.get(f"{unit_type.value}_units", 0.0)
            
            # Add API call costs (if any)
            api_calls = usage.get("api_calls_total", 0.0)
            total_units += api_calls * 0.01  # 0.01 RU per API call
            
            # Add storage costs (if any)
            storage_bytes = usage.get("storage_bytes_total", 0.0)
            total_units += storage_bytes / (1024 * 1024 * 1024) * 0.1  # 0.1 RU per GB
            
            return total_units
            
        except Exception as e:
            self.logger.error(f"Error calculating billing units: {e}")
            return 0.0
    
    def export_usage_data(self, tenant_id: str, start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Export usage data for reporting."""
        try:
            if start_date is None:
                start_date = datetime.utcnow() - timedelta(days=30)
            if end_date is None:
                end_date = datetime.utcnow()
            
            export_data = {
                "tenant_id": tenant_id,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "export_timestamp": datetime.utcnow().isoformat(),
                "usage_summary": self.get_tenant_usage(tenant_id, start_date, end_date),
                "billing_units": self.calculate_billing_units(tenant_id, start_date, end_date),
                "reasoning_units": [],
                "metrics": []
            }
            
            # Export reasoning units
            if tenant_id in self.reasoning_units:
                units = [
                    unit for unit in self.reasoning_units[tenant_id]
                    if start_date <= unit.timestamp <= end_date
                ]
                export_data["reasoning_units"] = [unit.to_dict() for unit in units]
            
            # Export metrics
            for metric_type in UsageMetricType:
                metric_key = f"{tenant_id}_{metric_type.value}"
                if metric_key in self.metrics:
                    metrics = [
                        m for m in self.metrics[metric_key]
                        if start_date <= m.timestamp <= end_date
                    ]
                    export_data["metrics"].extend([m.to_dict() for m in metrics])
            
            return export_data
            
        except Exception as e:
            self.logger.error(f"Error exporting usage data: {e}")
            return {}
    
    def clear_old_data(self, days_to_keep: int = 90) -> None:
        """Clear old usage data to prevent memory bloat."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            
            # Clear old reasoning units
            for tenant_id in list(self.reasoning_units.keys()):
                self.reasoning_units[tenant_id] = [
                    unit for unit in self.reasoning_units[tenant_id]
                    if unit.timestamp >= cutoff_date
                ]
                if not self.reasoning_units[tenant_id]:
                    del self.reasoning_units[tenant_id]
            
            # Clear old metrics
            for metric_key in list(self.metrics.keys()):
                self.metrics[metric_key] = [
                    metric for metric in self.metrics[metric_key]
                    if metric.timestamp >= cutoff_date
                ]
                if not self.metrics[metric_key]:
                    del self.metrics[metric_key]
            
            self.logger.info(f"Cleared usage data older than {days_to_keep} days")
            
        except Exception as e:
            self.logger.error(f"Error clearing old data: {e}")


# Global usage meter instance
usage_meter = UsageMeter()
