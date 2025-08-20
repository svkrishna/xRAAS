"""
Health Monitor
System health monitoring, status checks, and alerting.
"""

import uuid
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import psutil
import requests

logger = logging.getLogger(__name__)


class HealthStatus(str, Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class CheckType(str, Enum):
    """Types of health checks."""
    HTTP = "http"
    TCP = "tcp"
    DATABASE = "database"
    DISK = "disk"
    MEMORY = "memory"
    CPU = "cpu"
    CUSTOM = "custom"


class AlertLevel(str, Enum):
    """Alert levels for health issues."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class HealthCheck:
    """A health check configuration."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    check_type: CheckType = CheckType.HTTP
    target: str = ""
    interval_seconds: int = 60
    timeout_seconds: int = 10
    retries: int = 3
    alert_threshold: int = 3
    is_active: bool = True
    custom_check: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "check_type": self.check_type.value,
            "target": self.target,
            "interval_seconds": self.interval_seconds,
            "timeout_seconds": self.timeout_seconds,
            "retries": self.retries,
            "alert_threshold": self.alert_threshold,
            "is_active": self.is_active,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HealthCheck':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            check_type=CheckType(data.get("check_type", "http")),
            target=data.get("target", ""),
            interval_seconds=data.get("interval_seconds", 60),
            timeout_seconds=data.get("timeout_seconds", 10),
            retries=data.get("retries", 3),
            alert_threshold=data.get("alert_threshold", 3),
            is_active=data.get("is_active", True),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat()))
        )


@dataclass
class HealthCheckResult:
    """Result of a health check."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    check_id: str = ""
    status: HealthStatus = HealthStatus.UNKNOWN
    response_time_ms: float = 0.0
    error_message: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "check_id": self.check_id,
            "status": self.status.value,
            "response_time_ms": self.response_time_ms,
            "error_message": self.error_message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HealthCheckResult':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            check_id=data.get("check_id", ""),
            status=HealthStatus(data.get("status", "unknown")),
            response_time_ms=data.get("response_time_ms", 0.0),
            error_message=data.get("error_message"),
            details=data.get("details", {}),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.utcnow().isoformat()))
        )


@dataclass
class HealthAlert:
    """Health alert notification."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    check_id: str = ""
    alert_level: AlertLevel = AlertLevel.WARNING
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    is_resolved: bool = False
    resolved_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "check_id": self.check_id,
            "alert_level": self.alert_level.value,
            "message": self.message,
            "details": self.details,
            "is_resolved": self.is_resolved,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HealthAlert':
        """Create from dictionary."""
        alert = cls(
            id=data.get("id", str(uuid.uuid4())),
            check_id=data.get("check_id", ""),
            alert_level=AlertLevel(data.get("alert_level", "warning")),
            message=data.get("message", ""),
            details=data.get("details", {}),
            is_resolved=data.get("is_resolved", False),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat()))
        )
        
        if data.get("resolved_at"):
            alert.resolved_at = datetime.fromisoformat(data["resolved_at"])
        
        return alert


class HealthMonitor:
    """Monitors system health and manages health checks."""
    
    def __init__(self):
        self.health_checks: Dict[str, HealthCheck] = {}
        self.check_results: Dict[str, List[HealthCheckResult]] = {}
        self.alerts: Dict[str, HealthAlert] = {}
        self.running_checks: Dict[str, asyncio.Task] = {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize default health checks
        self._initialize_default_checks()
    
    def add_health_check(self, check: HealthCheck) -> None:
        """Add a health check."""
        try:
            self.health_checks[check.id] = check
            self.check_results[check.id] = []
            
            # Start monitoring if active
            if check.is_active:
                self._start_check_monitoring(check)
            
            self.logger.info(f"Added health check: {check.name} ({check.id})")
            
        except Exception as e:
            self.logger.error(f"Error adding health check: {e}")
            raise
    
    def remove_health_check(self, check_id: str) -> bool:
        """Remove a health check."""
        try:
            if check_id not in self.health_checks:
                return False
            
            # Stop monitoring
            if check_id in self.running_checks:
                self.running_checks[check_id].cancel()
                del self.running_checks[check_id]
            
            # Remove check and results
            del self.health_checks[check_id]
            if check_id in self.check_results:
                del self.check_results[check_id]
            
            self.logger.info(f"Removed health check: {check_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error removing health check: {e}")
            return False
    
    def get_health_check(self, check_id: str) -> Optional[HealthCheck]:
        """Get a health check by ID."""
        return self.health_checks.get(check_id)
    
    def list_health_checks(self) -> List[HealthCheck]:
        """List all health checks."""
        return list(self.health_checks.values())
    
    async def run_health_check(self, check_id: str) -> HealthCheckResult:
        """Run a single health check."""
        try:
            check = self.health_checks.get(check_id)
            if not check:
                raise ValueError(f"Health check {check_id} not found")
            
            start_time = time.time()
            
            # Perform the check based on type
            if check.check_type == CheckType.HTTP:
                result = await self._check_http(check)
            elif check.check_type == CheckType.TCP:
                result = await self._check_tcp(check)
            elif check.check_type == CheckType.DATABASE:
                result = await self._check_database(check)
            elif check.check_type == CheckType.DISK:
                result = await self._check_disk(check)
            elif check.check_type == CheckType.MEMORY:
                result = await self._check_memory(check)
            elif check.check_type == CheckType.CPU:
                result = await self._check_cpu(check)
            elif check.check_type == CheckType.CUSTOM and check.custom_check:
                result = await self._check_custom(check)
            else:
                result = HealthCheckResult(
                    check_id=check.id,
                    status=HealthStatus.UNKNOWN,
                    error_message="Unknown check type"
                )
            
            # Calculate response time
            result.response_time_ms = (time.time() - start_time) * 1000
            
            # Store result
            self.check_results[check_id].append(result)
            
            # Keep only recent results
            if len(self.check_results[check_id]) > 100:
                self.check_results[check_id] = self.check_results[check_id][-100:]
            
            # Check for alerts
            await self._check_alerts(check, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error running health check {check_id}: {e}")
            result = HealthCheckResult(
                check_id=check_id,
                status=HealthStatus.UNHEALTHY,
                error_message=str(e)
            )
            return result
    
    async def _check_http(self, check: HealthCheck) -> HealthCheckResult:
        """Perform HTTP health check."""
        try:
            response = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: requests.get(check.target, timeout=check.timeout_seconds)
                ),
                timeout=check.timeout_seconds
            )
            
            if response.status_code < 400:
                return HealthCheckResult(
                    check_id=check.id,
                    status=HealthStatus.HEALTHY,
                    details={"status_code": response.status_code}
                )
            else:
                return HealthCheckResult(
                    check_id=check.id,
                    status=HealthStatus.UNHEALTHY,
                    error_message=f"HTTP {response.status_code}",
                    details={"status_code": response.status_code}
                )
                
        except Exception as e:
            return HealthCheckResult(
                check_id=check.id,
                status=HealthStatus.UNHEALTHY,
                error_message=str(e)
            )
    
    async def _check_tcp(self, check: HealthCheck) -> HealthCheckResult:
        """Perform TCP health check."""
        try:
            host, port = check.target.split(":")
            port = int(port)
            
            await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=check.timeout_seconds
            )
            
            return HealthCheckResult(
                check_id=check.id,
                status=HealthStatus.HEALTHY
            )
            
        except Exception as e:
            return HealthCheckResult(
                check_id=check.id,
                status=HealthStatus.UNHEALTHY,
                error_message=str(e)
            )
    
    async def _check_database(self, check: HealthCheck) -> HealthCheckResult:
        """Perform database health check."""
        try:
            # Simplified database check - in real implementation, test actual connection
            await asyncio.sleep(0.1)  # Simulate database query
            
            return HealthCheckResult(
                check_id=check.id,
                status=HealthStatus.HEALTHY,
                details={"connection": "active"}
            )
            
        except Exception as e:
            return HealthCheckResult(
                check_id=check.id,
                status=HealthStatus.UNHEALTHY,
                error_message=str(e)
            )
    
    async def _check_disk(self, check: HealthCheck) -> HealthCheckResult:
        """Perform disk health check."""
        try:
            disk_usage = psutil.disk_usage(check.target or "/")
            usage_percent = disk_usage.percent
            
            if usage_percent < 80:
                status = HealthStatus.HEALTHY
            elif usage_percent < 90:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY
            
            return HealthCheckResult(
                check_id=check.id,
                status=status,
                details={
                    "usage_percent": usage_percent,
                    "free_gb": disk_usage.free / (1024**3),
                    "total_gb": disk_usage.total / (1024**3)
                }
            )
            
        except Exception as e:
            return HealthCheckResult(
                check_id=check.id,
                status=HealthStatus.UNHEALTHY,
                error_message=str(e)
            )
    
    async def _check_memory(self, check: HealthCheck) -> HealthCheckResult:
        """Perform memory health check."""
        try:
            memory = psutil.virtual_memory()
            usage_percent = memory.percent
            
            if usage_percent < 80:
                status = HealthStatus.HEALTHY
            elif usage_percent < 90:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY
            
            return HealthCheckResult(
                check_id=check.id,
                status=status,
                details={
                    "usage_percent": usage_percent,
                    "available_gb": memory.available / (1024**3),
                    "total_gb": memory.total / (1024**3)
                }
            )
            
        except Exception as e:
            return HealthCheckResult(
                check_id=check.id,
                status=HealthStatus.UNHEALTHY,
                error_message=str(e)
            )
    
    async def _check_cpu(self, check: HealthCheck) -> HealthCheckResult:
        """Perform CPU health check."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            
            if cpu_percent < 80:
                status = HealthStatus.HEALTHY
            elif cpu_percent < 90:
                status = HealthStatus.DEGRADED
            else:
                status = HealthStatus.UNHEALTHY
            
            return HealthCheckResult(
                check_id=check.id,
                status=status,
                details={
                    "cpu_percent": cpu_percent,
                    "load_average": psutil.getloadavg()
                }
            )
            
        except Exception as e:
            return HealthCheckResult(
                check_id=check.id,
                status=HealthStatus.UNHEALTHY,
                error_message=str(e)
            )
    
    async def _check_custom(self, check: HealthCheck) -> HealthCheckResult:
        """Perform custom health check."""
        try:
            if check.custom_check:
                result = await check.custom_check()
                return HealthCheckResult(
                    check_id=check.id,
                    status=result.get("status", HealthStatus.UNKNOWN),
                    details=result.get("details", {})
                )
            else:
                return HealthCheckResult(
                    check_id=check.id,
                    status=HealthStatus.UNKNOWN,
                    error_message="No custom check function provided"
                )
                
        except Exception as e:
            return HealthCheckResult(
                check_id=check.id,
                status=HealthStatus.UNHEALTHY,
                error_message=str(e)
            )
    
    async def _check_alerts(self, check: HealthCheck, result: HealthCheckResult):
        """Check if alert should be triggered."""
        try:
            # Count recent failures
            recent_results = [
                r for r in self.check_results[check.id][-check.alert_threshold:]
                if r.status != HealthStatus.HEALTHY
            ]
            
            if len(recent_results) >= check.alert_threshold:
                # Create or update alert
                alert_id = f"{check.id}_alert"
                
                if alert_id not in self.alerts or self.alerts[alert_id].is_resolved:
                    alert = HealthAlert(
                        check_id=check.id,
                        alert_level=AlertLevel.ERROR if result.status == HealthStatus.UNHEALTHY else AlertLevel.WARNING,
                        message=f"Health check '{check.name}' is {result.status.value}",
                        details={
                            "check_type": check.check_type.value,
                            "target": check.target,
                            "error_message": result.error_message,
                            "response_time_ms": result.response_time_ms
                        }
                    )
                    self.alerts[alert_id] = alert
                    self.logger.warning(f"Health alert created: {alert.message}")
            
            # Resolve alert if check is healthy
            elif result.status == HealthStatus.HEALTHY:
                alert_id = f"{check.id}_alert"
                if alert_id in self.alerts and not self.alerts[alert_id].is_resolved:
                    self.alerts[alert_id].is_resolved = True
                    self.alerts[alert_id].resolved_at = datetime.utcnow()
                    self.logger.info(f"Health alert resolved: {check.name}")
                    
        except Exception as e:
            self.logger.error(f"Error checking alerts: {e}")
    
    def _start_check_monitoring(self, check: HealthCheck):
        """Start monitoring a health check."""
        try:
            if check.id in self.running_checks:
                self.running_checks[check.id].cancel()
            
            async def monitor_check():
                while True:
                    try:
                        await self.run_health_check(check.id)
                        await asyncio.sleep(check.interval_seconds)
                    except asyncio.CancelledError:
                        break
                    except Exception as e:
                        self.logger.error(f"Error in check monitoring: {e}")
                        await asyncio.sleep(check.interval_seconds)
            
            self.running_checks[check.id] = asyncio.create_task(monitor_check())
            
        except Exception as e:
            self.logger.error(f"Error starting check monitoring: {e}")
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        try:
            total_checks = len(self.health_checks)
            healthy_checks = 0
            degraded_checks = 0
            unhealthy_checks = 0
            
            for check_id in self.health_checks:
                if check_id in self.check_results and self.check_results[check_id]:
                    latest_result = self.check_results[check_id][-1]
                    if latest_result.status == HealthStatus.HEALTHY:
                        healthy_checks += 1
                    elif latest_result.status == HealthStatus.DEGRADED:
                        degraded_checks += 1
                    elif latest_result.status == HealthStatus.UNHEALTHY:
                        unhealthy_checks += 1
            
            # Determine overall status
            if unhealthy_checks > 0:
                overall_status = HealthStatus.UNHEALTHY
            elif degraded_checks > 0:
                overall_status = HealthStatus.DEGRADED
            elif healthy_checks == total_checks:
                overall_status = HealthStatus.HEALTHY
            else:
                overall_status = HealthStatus.UNKNOWN
            
            return {
                "status": overall_status.value,
                "total_checks": total_checks,
                "healthy_checks": healthy_checks,
                "degraded_checks": degraded_checks,
                "unhealthy_checks": unhealthy_checks,
                "health_percentage": (healthy_checks / total_checks * 100) if total_checks > 0 else 0,
                "active_alerts": len([a for a in self.alerts.values() if not a.is_resolved]),
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system health: {e}")
            return {
                "status": HealthStatus.UNKNOWN.value,
                "error": str(e)
            }
    
    def get_check_history(self, check_id: str, hours: int = 24) -> List[HealthCheckResult]:
        """Get health check history."""
        try:
            if check_id not in self.check_results:
                return []
            
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            return [
                result for result in self.check_results[check_id]
                if result.timestamp >= cutoff_time
            ]
            
        except Exception as e:
            self.logger.error(f"Error getting check history: {e}")
            return []
    
    def get_active_alerts(self) -> List[HealthAlert]:
        """Get active (unresolved) alerts."""
        return [alert for alert in self.alerts.values() if not alert.is_resolved]
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved."""
        try:
            if alert_id in self.alerts:
                self.alerts[alert_id].is_resolved = True
                self.alerts[alert_id].resolved_at = datetime.utcnow()
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error resolving alert: {e}")
            return False
    
    def _initialize_default_checks(self):
        """Initialize default health checks."""
        
        # System resource checks
        disk_check = HealthCheck(
            name="Disk Usage",
            description="Monitor disk usage",
            check_type=CheckType.DISK,
            target="/",
            interval_seconds=300  # 5 minutes
        )
        self.add_health_check(disk_check)
        
        memory_check = HealthCheck(
            name="Memory Usage",
            description="Monitor memory usage",
            check_type=CheckType.MEMORY,
            interval_seconds=300  # 5 minutes
        )
        self.add_health_check(memory_check)
        
        cpu_check = HealthCheck(
            name="CPU Usage",
            description="Monitor CPU usage",
            check_type=CheckType.CPU,
            interval_seconds=300  # 5 minutes
        )
        self.add_health_check(cpu_check)
        
        self.logger.info("Initialized default health checks")


# Global health monitor instance
health_monitor = HealthMonitor()
