"""
Enterprise SLA/SLO Management System
Comprehensive service level agreement monitoring and alerting.
"""

import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field
import statistics
from collections import defaultdict, deque
import uuid

from app.security.audit_logger import audit_logger, AuditEventType, ComplianceFramework


class SLAType(str, Enum):
    """Types of SLA metrics."""
    AVAILABILITY = "availability"
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    SECURITY_RESPONSE = "security_response"
    DATA_RECOVERY = "data_recovery"


class SeverityLevel(str, Enum):
    """SLA violation severity levels."""
    INFO = "info"
    WARNING = "warning"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"


class ServiceTier(str, Enum):
    """Service tier definitions for different SLA levels."""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    MISSION_CRITICAL = "mission_critical"


@dataclass
class SLATarget:
    """SLA target definition."""
    sla_type: SLAType
    service_tier: ServiceTier
    target_value: float
    measurement_window_hours: int
    description: str
    penalty_per_violation: float = 0.0
    escalation_thresholds: Dict[str, float] = field(default_factory=dict)


@dataclass
class SLAMetrics:
    """Current SLA metrics and status."""
    sla_type: SLAType
    service_tier: ServiceTier
    current_value: float
    target_value: float
    compliance_percentage: float
    measurement_window_start: datetime
    measurement_window_end: datetime
    sample_count: int
    last_updated: datetime
    status: str  # "meeting", "at_risk", "violated"


@dataclass
class SLAViolation:
    """SLA violation record."""
    violation_id: str
    sla_type: SLAType
    service_tier: ServiceTier
    target_value: float
    actual_value: float
    severity: SeverityLevel
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: Optional[float]
    root_cause: Optional[str]
    resolution_actions: List[str]
    customer_impact: str
    penalty_amount: float
    escalated: bool = False


class SLAManager:
    """
    Enterprise SLA/SLO Management System.
    
    Manages service level agreements across different tiers:
    - Starter: 99.0% availability, 5s response time
    - Professional: 99.5% availability, 2s response time  
    - Enterprise: 99.9% availability, 1s response time
    - Mission Critical: 99.99% availability, 500ms response time
    """
    
    def __init__(self):
        self.sla_targets = self._initialize_sla_targets()
        self.current_metrics: Dict[str, SLAMetrics] = {}
        self.violations: Dict[str, SLAViolation] = {}
        self.measurement_data: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.active_incidents: Dict[str, Dict[str, Any]] = {}
        
        # Start monitoring tasks
        asyncio.create_task(self._continuous_monitoring())
    
    def _initialize_sla_targets(self) -> Dict[str, SLATarget]:
        """Initialize SLA targets for different service tiers."""
        targets = {}
        
        # Availability SLAs
        availability_targets = [
            (ServiceTier.STARTER, 99.0, "Basic availability guarantee"),
            (ServiceTier.PROFESSIONAL, 99.5, "Professional availability guarantee"),
            (ServiceTier.ENTERPRISE, 99.9, "Enterprise availability guarantee"),
            (ServiceTier.MISSION_CRITICAL, 99.99, "Mission critical availability guarantee")
        ]
        
        for tier, target, description in availability_targets:
            key = f"{SLAType.AVAILABILITY}_{tier.value}"
            targets[key] = SLATarget(
                sla_type=SLAType.AVAILABILITY,
                service_tier=tier,
                target_value=target,
                measurement_window_hours=24,
                description=description,
                penalty_per_violation=1000.0 if tier == ServiceTier.ENTERPRISE else 500.0,
                escalation_thresholds={
                    "warning": target - 0.1,
                    "critical": target - 0.5
                }
            )
        
        # Response Time SLAs (in milliseconds)
        response_time_targets = [
            (ServiceTier.STARTER, 5000.0, "Basic response time guarantee"),
            (ServiceTier.PROFESSIONAL, 2000.0, "Professional response time guarantee"),
            (ServiceTier.ENTERPRISE, 1000.0, "Enterprise response time guarantee"),
            (ServiceTier.MISSION_CRITICAL, 500.0, "Mission critical response time guarantee")
        ]
        
        for tier, target, description in response_time_targets:
            key = f"{SLAType.RESPONSE_TIME}_{tier.value}"
            targets[key] = SLATarget(
                sla_type=SLAType.RESPONSE_TIME,
                service_tier=tier,
                target_value=target,
                measurement_window_hours=1,
                description=description,
                penalty_per_violation=500.0 if tier == ServiceTier.ENTERPRISE else 250.0,
                escalation_thresholds={
                    "warning": target * 1.2,
                    "critical": target * 1.5
                }
            )
        
        # Error Rate SLAs (percentage)
        error_rate_targets = [
            (ServiceTier.STARTER, 5.0, "Basic error rate limit"),
            (ServiceTier.PROFESSIONAL, 2.0, "Professional error rate limit"),
            (ServiceTier.ENTERPRISE, 0.5, "Enterprise error rate limit"),
            (ServiceTier.MISSION_CRITICAL, 0.1, "Mission critical error rate limit")
        ]
        
        for tier, target, description in error_rate_targets:
            key = f"{SLAType.ERROR_RATE}_{tier.value}"
            targets[key] = SLATarget(
                sla_type=SLAType.ERROR_RATE,
                service_tier=tier,
                target_value=target,
                measurement_window_hours=1,
                description=description,
                penalty_per_violation=250.0,
                escalation_thresholds={
                    "warning": target + 0.5,
                    "critical": target + 1.0
                }
            )
        
        return targets
    
    async def record_metric(
        self,
        sla_type: SLAType,
        service_tier: ServiceTier,
        value: float,
        timestamp: Optional[datetime] = None
    ):
        """
        Record a metric value for SLA tracking.
        
        Args:
            sla_type: Type of SLA metric
            service_tier: Service tier
            value: Metric value
            timestamp: Optional timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        
        key = f"{sla_type.value}_{service_tier.value}"
        
        # Store measurement data
        self.measurement_data[key].append({
            "value": value,
            "timestamp": timestamp
        })
        
        # Update current metrics
        await self._update_current_metrics(sla_type, service_tier)
        
        # Check for violations
        await self._check_sla_violations(sla_type, service_tier)
    
    async def _update_current_metrics(self, sla_type: SLAType, service_tier: ServiceTier):
        """Update current metrics based on recent measurements."""
        key = f"{sla_type.value}_{service_tier.value}"
        
        if key not in self.sla_targets:
            return
        
        target = self.sla_targets[key]
        measurements = self.measurement_data[key]
        
        if not measurements:
            return
        
        # Filter measurements within window
        window_start = datetime.now(timezone.utc) - timedelta(hours=target.measurement_window_hours)
        recent_measurements = [
            m for m in measurements
            if m["timestamp"] >= window_start
        ]
        
        if not recent_measurements:
            return
        
        # Calculate current value based on SLA type
        values = [m["value"] for m in recent_measurements]
        
        if sla_type == SLAType.AVAILABILITY:
            # Availability is percentage of successful requests
            current_value = statistics.mean(values)
        elif sla_type == SLAType.RESPONSE_TIME:
            # Response time uses 95th percentile
            current_value = statistics.quantiles(values, n=20)[18]  # 95th percentile
        elif sla_type == SLAType.ERROR_RATE:
            # Error rate is percentage of failed requests
            current_value = statistics.mean(values)
        else:
            current_value = statistics.mean(values)
        
        # Calculate compliance
        if sla_type in [SLAType.RESPONSE_TIME, SLAType.ERROR_RATE]:
            # Lower is better
            compliance = max(0, min(100, (target.target_value - current_value) / target.target_value * 100))
        else:
            # Higher is better
            compliance = min(100, current_value / target.target_value * 100)
        
        # Determine status
        if compliance >= 100:
            status = "meeting"
        elif compliance >= 95:
            status = "at_risk"
        else:
            status = "violated"
        
        # Update metrics
        self.current_metrics[key] = SLAMetrics(
            sla_type=sla_type,
            service_tier=service_tier,
            current_value=current_value,
            target_value=target.target_value,
            compliance_percentage=compliance,
            measurement_window_start=window_start,
            measurement_window_end=datetime.now(timezone.utc),
            sample_count=len(recent_measurements),
            last_updated=datetime.now(timezone.utc),
            status=status
        )
    
    async def _check_sla_violations(self, sla_type: SLAType, service_tier: ServiceTier):
        """Check for SLA violations and create violation records."""
        key = f"{sla_type.value}_{service_tier.value}"
        
        if key not in self.current_metrics or key not in self.sla_targets:
            return
        
        metrics = self.current_metrics[key]
        target = self.sla_targets[key]
        
        # Check if SLA is violated
        is_violated = False
        severity = SeverityLevel.INFO
        
        if sla_type in [SLAType.RESPONSE_TIME, SLAType.ERROR_RATE]:
            # Lower is better - violation if current > target
            if metrics.current_value > target.target_value:
                is_violated = True
                if metrics.current_value > target.target_value * 1.5:
                    severity = SeverityLevel.CRITICAL
                elif metrics.current_value > target.target_value * 1.2:
                    severity = SeverityLevel.MAJOR
                else:
                    severity = SeverityLevel.MINOR
        else:
            # Higher is better - violation if current < target
            if metrics.current_value < target.target_value:
                is_violated = True
                if metrics.current_value < target.target_value * 0.95:
                    severity = SeverityLevel.CRITICAL
                elif metrics.current_value < target.target_value * 0.98:
                    severity = SeverityLevel.MAJOR
                else:
                    severity = SeverityLevel.MINOR
        
        if is_violated:
            # Check if this is a new violation or ongoing
            active_violation_key = f"active_{key}"
            
            if active_violation_key not in self.active_incidents:
                # New violation
                violation_id = str(uuid.uuid4())
                
                violation = SLAViolation(
                    violation_id=violation_id,
                    sla_type=sla_type,
                    service_tier=service_tier,
                    target_value=target.target_value,
                    actual_value=metrics.current_value,
                    severity=severity,
                    start_time=datetime.now(timezone.utc),
                    end_time=None,
                    duration_minutes=None,
                    root_cause=None,
                    resolution_actions=[],
                    customer_impact=self._determine_customer_impact(severity, service_tier),
                    penalty_amount=target.penalty_per_violation
                )
                
                self.violations[violation_id] = violation
                self.active_incidents[active_violation_key] = {
                    "violation_id": violation_id,
                    "start_time": violation.start_time
                }
                
                # Log violation
                audit_logger.log_event(
                    event_type=AuditEventType.SYSTEM_ERROR,
                    action="sla_violation_started",
                    result="violation",
                    details={
                        "violation_id": violation_id,
                        "sla_type": sla_type.value,
                        "service_tier": service_tier.value,
                        "target_value": target.target_value,
                        "actual_value": metrics.current_value,
                        "severity": severity.value
                    },
                    compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
                    risk_level="high" if severity in [SeverityLevel.MAJOR, SeverityLevel.CRITICAL] else "medium"
                )
                
                # Send alerts
                await self._send_sla_alert(violation)
        
        else:
            # Check if we need to close an active violation
            active_violation_key = f"active_{key}"
            
            if active_violation_key in self.active_incidents:
                incident = self.active_incidents[active_violation_key]
                violation_id = incident["violation_id"]
                
                if violation_id in self.violations:
                    violation = self.violations[violation_id]
                    violation.end_time = datetime.now(timezone.utc)
                    violation.duration_minutes = (
                        violation.end_time - violation.start_time
                    ).total_seconds() / 60
                    
                    # Remove from active incidents
                    del self.active_incidents[active_violation_key]
                    
                    # Log resolution
                    audit_logger.log_event(
                        event_type=AuditEventType.SYSTEM_ERROR,
                        action="sla_violation_resolved",
                        result="resolved",
                        details={
                            "violation_id": violation_id,
                            "duration_minutes": violation.duration_minutes,
                            "resolution_time": violation.end_time.isoformat()
                        },
                        compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
                        risk_level="low"
                    )
    
    def _determine_customer_impact(self, severity: SeverityLevel, service_tier: ServiceTier) -> str:
        """Determine customer impact based on severity and tier."""
        impact_matrix = {
            SeverityLevel.INFO: "Minimal impact - service operating normally",
            SeverityLevel.WARNING: "Minor degradation - some users may experience slower responses",
            SeverityLevel.MINOR: "Moderate impact - noticeable performance degradation",
            SeverityLevel.MAJOR: "Significant impact - substantial service degradation",
            SeverityLevel.CRITICAL: "Severe impact - service unavailable or critically degraded"
        }
        
        base_impact = impact_matrix.get(severity, "Unknown impact")
        
        if service_tier in [ServiceTier.ENTERPRISE, ServiceTier.MISSION_CRITICAL]:
            return f"{base_impact} (High-tier customer affected)"
        
        return base_impact
    
    async def _send_sla_alert(self, violation: SLAViolation):
        """Send alert for SLA violation."""
        # In production, this would integrate with alerting systems
        # (PagerDuty, Slack, email, SMS, etc.)
        
        alert_data = {
            "violation_id": violation.violation_id,
            "sla_type": violation.sla_type.value,
            "service_tier": violation.service_tier.value,
            "severity": violation.severity.value,
            "target_value": violation.target_value,
            "actual_value": violation.actual_value,
            "customer_impact": violation.customer_impact,
            "penalty_amount": violation.penalty_amount
        }
        
        # Log alert
        audit_logger.log_event(
            event_type=AuditEventType.ADMIN_ACTION,
            action="send_sla_alert",
            result="success",
            details=alert_data,
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="high" if violation.severity == SeverityLevel.CRITICAL else "medium"
        )
    
    async def _continuous_monitoring(self):
        """Continuous monitoring background task."""
        while True:
            try:
                # Update all current metrics
                for key in self.sla_targets:
                    sla_type_str, service_tier_str = key.split("_", 1)
                    sla_type = SLAType(sla_type_str)
                    service_tier = ServiceTier(service_tier_str)
                    
                    await self._update_current_metrics(sla_type, service_tier)
                
                # Sleep for 30 seconds before next check
                await asyncio.sleep(30)
                
            except Exception as e:
                # Log monitoring error
                audit_logger.log_event(
                    event_type=AuditEventType.SYSTEM_ERROR,
                    action="sla_monitoring_error",
                    result="error",
                    details={"error": str(e)},
                    compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
                    risk_level="medium"
                )
                
                # Wait before retrying
                await asyncio.sleep(60)
    
    def get_sla_dashboard(self) -> Dict[str, Any]:
        """
        Get comprehensive SLA dashboard data.
        
        Returns:
            Dict: SLA dashboard information
        """
        dashboard = {
            "overall_status": "healthy",
            "active_violations": len(self.active_incidents),
            "total_violations_24h": 0,
            "service_tiers": {},
            "sla_metrics": [],
            "recent_violations": [],
            "compliance_summary": {}
        }
        
        # Calculate overall status
        critical_violations = sum(
            1 for incident in self.active_incidents.values()
            if self.violations.get(incident["violation_id"], {}).severity == SeverityLevel.CRITICAL
        )
        
        if critical_violations > 0:
            dashboard["overall_status"] = "critical"
        elif len(self.active_incidents) > 0:
            dashboard["overall_status"] = "degraded"
        
        # Group metrics by service tier
        for tier in ServiceTier:
            tier_metrics = {}
            tier_violations = 0
            
            for sla_type in SLAType:
                key = f"{sla_type.value}_{tier.value}"
                if key in self.current_metrics:
                    metrics = self.current_metrics[key]
                    tier_metrics[sla_type.value] = {
                        "current_value": metrics.current_value,
                        "target_value": metrics.target_value,
                        "compliance_percentage": metrics.compliance_percentage,
                        "status": metrics.status,
                        "sample_count": metrics.sample_count
                    }
                    
                    if metrics.status == "violated":
                        tier_violations += 1
            
            dashboard["service_tiers"][tier.value] = {
                "metrics": tier_metrics,
                "active_violations": tier_violations,
                "overall_compliance": statistics.mean([
                    m["compliance_percentage"] for m in tier_metrics.values()
                ]) if tier_metrics else 100
            }
        
        # Recent violations (last 24 hours)
        recent_cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        recent_violations = [
            {
                "violation_id": v.violation_id,
                "sla_type": v.sla_type.value,
                "service_tier": v.service_tier.value,
                "severity": v.severity.value,
                "start_time": v.start_time.isoformat(),
                "duration_minutes": v.duration_minutes,
                "penalty_amount": v.penalty_amount
            }
            for v in self.violations.values()
            if v.start_time >= recent_cutoff
        ]
        
        dashboard["recent_violations"] = recent_violations
        dashboard["total_violations_24h"] = len(recent_violations)
        
        # All current metrics
        dashboard["sla_metrics"] = [
            {
                "sla_type": metrics.sla_type.value,
                "service_tier": metrics.service_tier.value,
                "current_value": metrics.current_value,
                "target_value": metrics.target_value,
                "compliance_percentage": metrics.compliance_percentage,
                "status": metrics.status,
                "last_updated": metrics.last_updated.isoformat()
            }
            for metrics in self.current_metrics.values()
        ]
        
        return dashboard
    
    def get_sla_report(
        self,
        service_tier: ServiceTier,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Generate SLA compliance report for specific period.
        
        Args:
            service_tier: Service tier to report on
            start_date: Report start date
            end_date: Report end date
            
        Returns:
            Dict: SLA compliance report
        """
        # Filter violations for the period
        period_violations = [
            v for v in self.violations.values()
            if (v.service_tier == service_tier and
                v.start_time >= start_date and
                v.start_time <= end_date)
        ]
        
        # Calculate compliance metrics
        total_penalty = sum(v.penalty_amount for v in period_violations)
        avg_resolution_time = statistics.mean([
            v.duration_minutes for v in period_violations
            if v.duration_minutes is not None
        ]) if period_violations else 0
        
        return {
            "service_tier": service_tier.value,
            "reporting_period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "total_violations": len(period_violations),
            "violations_by_severity": {
                severity.value: sum(1 for v in period_violations if v.severity == severity)
                for severity in SeverityLevel
            },
            "total_penalty_amount": total_penalty,
            "average_resolution_time_minutes": avg_resolution_time,
            "sla_targets": {
                sla_type.value: self.sla_targets.get(f"{sla_type.value}_{service_tier.value}", {}).target_value
                for sla_type in SLAType
            },
            "compliance_percentage": max(0, 100 - (len(period_violations) / 30 * 100)),  # Rough calculation
            "recommendations": self._generate_sla_recommendations(period_violations)
        }
    
    def _generate_sla_recommendations(self, violations: List[SLAViolation]) -> List[str]:
        """Generate recommendations based on violation patterns."""
        recommendations = []
        
        if not violations:
            return ["Continue current practices - no violations detected"]
        
        # Analyze violation patterns
        severity_counts = defaultdict(int)
        sla_type_counts = defaultdict(int)
        
        for violation in violations:
            severity_counts[violation.severity] += 1
            sla_type_counts[violation.sla_type] += 1
        
        # Generate specific recommendations
        if severity_counts[SeverityLevel.CRITICAL] > 0:
            recommendations.append("Implement immediate incident response procedures for critical violations")
        
        if sla_type_counts[SLAType.RESPONSE_TIME] > sla_type_counts[SLAType.AVAILABILITY]:
            recommendations.append("Focus on performance optimization and caching strategies")
        
        if sla_type_counts[SLAType.ERROR_RATE] > 2:
            recommendations.append("Improve error handling and implement circuit breakers")
        
        if len(violations) > 5:
            recommendations.append("Consider infrastructure scaling or architecture improvements")
        
        return recommendations


# Global SLA manager instance
sla_manager = SLAManager()
