"""
Circuit Breaker Pattern Implementation
Prevents cascading failures and provides resilient service communication.
"""

import asyncio
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, Callable, Awaitable
from enum import Enum
from dataclasses import dataclass
import statistics
from collections import deque

from app.security.audit_logger import audit_logger, AuditEventType, ComplianceFramework


class CircuitState(str, Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Circuit is open, requests fail fast
    HALF_OPEN = "half_open"  # Testing if service has recovered


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration."""
    failure_threshold: int = 5          # Number of failures to open circuit
    recovery_timeout: int = 60          # Seconds before trying half-open
    success_threshold: int = 3          # Successes needed to close from half-open
    timeout_duration: float = 5.0       # Request timeout in seconds
    monitoring_window: int = 300        # Monitoring window in seconds
    error_rate_threshold: float = 50.0  # Error rate percentage to open circuit


@dataclass
class CircuitBreakerMetrics:
    """Circuit breaker metrics."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    timeouts: int = 0
    circuit_opens: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    current_error_rate: float = 0.0


class CircuitBreakerException(Exception):
    """Exception raised when circuit breaker is open."""
    pass


class CircuitBreaker:
    """
    Circuit Breaker implementation for resilient service communication.
    
    Features:
    - Automatic failure detection
    - Fast-fail when service is down
    - Automatic recovery testing
    - Detailed metrics and monitoring
    - Configurable thresholds
    """
    
    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.metrics = CircuitBreakerMetrics()
        
        # Tracking deques for windowed metrics
        self.recent_requests: deque = deque(maxlen=1000)
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.state_change_time = time.time()
        
        # Lock for thread safety
        self._lock = asyncio.Lock()
    
    async def call(self, func: Callable[[], Awaitable[Any]], *args, **kwargs) -> Any:
        """
        Execute function through circuit breaker.
        
        Args:
            func: Async function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerException: When circuit is open
            Exception: Original function exceptions when circuit is closed
        """
        async with self._lock:
            await self._update_state()
            
            if self.state == CircuitState.OPEN:
                self._record_request(success=False, blocked=True)
                raise CircuitBreakerException(f"Circuit breaker '{self.name}' is OPEN")
            
            # Allow request through
            start_time = time.time()
            
            try:
                # Execute with timeout
                result = await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=self.config.timeout_duration
                )
                
                # Record success
                response_time = time.time() - start_time
                await self._on_success(response_time)
                return result
                
            except asyncio.TimeoutError:
                await self._on_timeout()
                raise
                
            except Exception as e:
                await self._on_failure(e)
                raise
    
    async def _update_state(self):
        """Update circuit breaker state based on current conditions."""
        current_time = time.time()
        
        if self.state == CircuitState.OPEN:
            # Check if we should try half-open
            if current_time - self.state_change_time >= self.config.recovery_timeout:
                await self._change_state(CircuitState.HALF_OPEN)
                
        elif self.state == CircuitState.HALF_OPEN:
            # Check if we have enough successes to close
            if self.success_count >= self.config.success_threshold:
                await self._change_state(CircuitState.CLOSED)
            # Check if we should open again due to failure
            elif self.failure_count >= 1:  # Single failure in half-open reopens circuit
                await self._change_state(CircuitState.OPEN)
                
        elif self.state == CircuitState.CLOSED:
            # Check if we should open due to failures
            if (self.failure_count >= self.config.failure_threshold or
                self._calculate_error_rate() >= self.config.error_rate_threshold):
                await self._change_state(CircuitState.OPEN)
    
    async def _change_state(self, new_state: CircuitState):
        """Change circuit breaker state."""
        old_state = self.state
        self.state = new_state
        self.state_change_time = time.time()
        
        # Reset counters based on new state
        if new_state == CircuitState.CLOSED:
            self.failure_count = 0
            self.success_count = 0
        elif new_state == CircuitState.HALF_OPEN:
            self.failure_count = 0
            self.success_count = 0
        elif new_state == CircuitState.OPEN:
            self.metrics.circuit_opens += 1
        
        # Log state change
        audit_logger.log_event(
            event_type=AuditEventType.SYSTEM_ERROR,
            action="circuit_breaker_state_change",
            result="state_changed",
            details={
                "circuit_name": self.name,
                "old_state": old_state.value,
                "new_state": new_state.value,
                "failure_count": self.failure_count,
                "error_rate": self._calculate_error_rate(),
                "metrics": {
                    "total_requests": self.metrics.total_requests,
                    "failed_requests": self.metrics.failed_requests,
                    "current_error_rate": self.metrics.current_error_rate
                }
            },
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="high" if new_state == CircuitState.OPEN else "medium"
        )
    
    async def _on_success(self, response_time: float):
        """Handle successful request."""
        self.success_count += 1
        self.metrics.successful_requests += 1
        self.metrics.last_success_time = datetime.now(timezone.utc)
        
        self._record_request(success=True, response_time=response_time)
        
        # Reset failure count on success in closed state
        if self.state == CircuitState.CLOSED:
            self.failure_count = 0
    
    async def _on_failure(self, exception: Exception):
        """Handle failed request."""
        self.failure_count += 1
        self.metrics.failed_requests += 1
        self.metrics.last_failure_time = datetime.now(timezone.utc)
        self.last_failure_time = time.time()
        
        self._record_request(success=False, exception=exception)
        
        # Reset success count on failure in half-open state
        if self.state == CircuitState.HALF_OPEN:
            self.success_count = 0
    
    async def _on_timeout(self):
        """Handle request timeout."""
        self.failure_count += 1
        self.metrics.timeouts += 1
        self.metrics.failed_requests += 1
        self.metrics.last_failure_time = datetime.now(timezone.utc)
        
        self._record_request(success=False, timeout=True)
    
    def _record_request(
        self,
        success: bool,
        blocked: bool = False,
        timeout: bool = False,
        response_time: Optional[float] = None,
        exception: Optional[Exception] = None
    ):
        """Record request metrics."""
        self.metrics.total_requests += 1
        
        request_record = {
            "timestamp": time.time(),
            "success": success,
            "blocked": blocked,
            "timeout": timeout,
            "response_time": response_time,
            "exception_type": type(exception).__name__ if exception else None
        }
        
        self.recent_requests.append(request_record)
        self.metrics.current_error_rate = self._calculate_error_rate()
    
    def _calculate_error_rate(self) -> float:
        """Calculate current error rate percentage."""
        if not self.recent_requests:
            return 0.0
        
        # Calculate error rate for recent window
        current_time = time.time()
        window_start = current_time - self.config.monitoring_window
        
        recent_in_window = [
            r for r in self.recent_requests
            if r["timestamp"] >= window_start
        ]
        
        if not recent_in_window:
            return 0.0
        
        failed_requests = sum(1 for r in recent_in_window if not r["success"] and not r["blocked"])
        total_requests = len(recent_in_window)
        
        return (failed_requests / total_requests) * 100 if total_requests > 0 else 0.0
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get circuit breaker metrics."""
        recent_response_times = [
            r["response_time"] for r in self.recent_requests
            if r["response_time"] is not None and r["success"]
        ]
        
        return {
            "name": self.name,
            "state": self.state.value,
            "total_requests": self.metrics.total_requests,
            "successful_requests": self.metrics.successful_requests,
            "failed_requests": self.metrics.failed_requests,
            "timeouts": self.metrics.timeouts,
            "circuit_opens": self.metrics.circuit_opens,
            "current_error_rate": self.metrics.current_error_rate,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.metrics.last_failure_time.isoformat() if self.metrics.last_failure_time else None,
            "last_success_time": self.metrics.last_success_time.isoformat() if self.metrics.last_success_time else None,
            "average_response_time": statistics.mean(recent_response_times) if recent_response_times else 0.0,
            "config": {
                "failure_threshold": self.config.failure_threshold,
                "recovery_timeout": self.config.recovery_timeout,
                "success_threshold": self.config.success_threshold,
                "timeout_duration": self.config.timeout_duration,
                "error_rate_threshold": self.config.error_rate_threshold
            }
        }
    
    def reset(self):
        """Manually reset circuit breaker to closed state."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.state_change_time = time.time()
        
        audit_logger.log_event(
            event_type=AuditEventType.ADMIN_ACTION,
            action="circuit_breaker_manual_reset",
            result="success",
            details={
                "circuit_name": self.name,
                "reset_time": datetime.now(timezone.utc).isoformat()
            },
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="medium"
        )


class CircuitBreakerManager:
    """
    Manager for multiple circuit breakers across the application.
    """
    
    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.default_config = CircuitBreakerConfig()
    
    def get_circuit_breaker(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None
    ) -> CircuitBreaker:
        """
        Get or create circuit breaker by name.
        
        Args:
            name: Circuit breaker name
            config: Optional custom configuration
            
        Returns:
            CircuitBreaker instance
        """
        if name not in self.circuit_breakers:
            self.circuit_breakers[name] = CircuitBreaker(
                name=name,
                config=config or self.default_config
            )
        
        return self.circuit_breakers[name]
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get metrics for all circuit breakers."""
        return {
            "circuit_breakers": {
                name: cb.get_metrics()
                for name, cb in self.circuit_breakers.items()
            },
            "summary": {
                "total_circuits": len(self.circuit_breakers),
                "open_circuits": sum(1 for cb in self.circuit_breakers.values() if cb.state == CircuitState.OPEN),
                "half_open_circuits": sum(1 for cb in self.circuit_breakers.values() if cb.state == CircuitState.HALF_OPEN),
                "closed_circuits": sum(1 for cb in self.circuit_breakers.values() if cb.state == CircuitState.CLOSED),
                "total_requests": sum(cb.metrics.total_requests for cb in self.circuit_breakers.values()),
                "total_failures": sum(cb.metrics.failed_requests for cb in self.circuit_breakers.values())
            }
        }
    
    def reset_all(self):
        """Reset all circuit breakers."""
        for circuit_breaker in self.circuit_breakers.values():
            circuit_breaker.reset()
        
        audit_logger.log_event(
            event_type=AuditEventType.ADMIN_ACTION,
            action="circuit_breaker_reset_all",
            result="success",
            details={
                "reset_count": len(self.circuit_breakers),
                "reset_time": datetime.now(timezone.utc).isoformat()
            },
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="medium"
        )


# Global circuit breaker manager
circuit_breaker_manager = CircuitBreakerManager()


# Decorator for easy circuit breaker usage
def circuit_breaker(
    name: str,
    config: Optional[CircuitBreakerConfig] = None
):
    """
    Decorator to wrap functions with circuit breaker.
    
    Args:
        name: Circuit breaker name
        config: Optional configuration
        
    Returns:
        Decorated function
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cb = circuit_breaker_manager.get_circuit_breaker(name, config)
            return await cb.call(func, *args, **kwargs)
        return wrapper
    return decorator
