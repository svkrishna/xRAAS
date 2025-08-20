"""
Metrics Service for Prometheus monitoring of reasoning operations.
"""

import time
from typing import Dict, Any, Optional
from prometheus_client import (
    Counter, Histogram, Gauge, Summary, 
    generate_latest, CONTENT_TYPE_LATEST,
    CollectorRegistry
)
from prometheus_client.metrics import CounterMetricFamily, HistogramMetricFamily, GaugeMetricFamily


class ReasoningMetricsService:
    """Service for tracking reasoning-specific metrics."""
    
    def __init__(self):
        # Create a custom registry for reasoning metrics
        self.registry = CollectorRegistry()
        
        # Request metrics
        self.reasoning_requests_total = Counter(
            'reasoning_requests_total',
            'Total number of reasoning requests',
            ['domain', 'status', 'model'],
            registry=self.registry
        )
        
        # Response time metrics
        self.reasoning_response_time = Histogram(
            'reasoning_response_time_seconds',
            'Reasoning response time in seconds',
            ['domain', 'stage'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0],
            registry=self.registry
        )
        
        # Confidence metrics
        self.reasoning_confidence = Histogram(
            'reasoning_confidence_score',
            'Confidence scores for reasoning results',
            ['domain', 'stage'],
            buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            registry=self.registry
        )
        
        # Error metrics
        self.reasoning_errors_total = Counter(
            'reasoning_errors_total',
            'Total number of reasoning errors',
            ['domain', 'error_type', 'stage'],
            registry=self.registry
        )
        
        # Ruleset metrics
        self.ruleset_executions_total = Counter(
            'ruleset_executions_total',
            'Total number of ruleset executions',
            ['ruleset_id', 'domain', 'status'],
            registry=self.registry
        )
        
        self.ruleset_execution_time = Histogram(
            'ruleset_execution_time_seconds',
            'Ruleset execution time in seconds',
            ['ruleset_id', 'domain'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0],
            registry=self.registry
        )
        
        # Graph metrics
        self.graph_operations_total = Counter(
            'graph_operations_total',
            'Total number of graph operations',
            ['operation_type', 'status'],
            registry=self.registry
        )
        
        self.graph_size = Gauge(
            'graph_size',
            'Number of nodes and edges in graphs',
            ['graph_id', 'metric_type'],
            registry=self.registry
        )
        
        # LLM metrics
        self.llm_requests_total = Counter(
            'llm_requests_total',
            'Total number of LLM API requests',
            ['model', 'status'],
            registry=self.registry
        )
        
        self.llm_response_time = Histogram(
            'llm_response_time_seconds',
            'LLM API response time in seconds',
            ['model'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0],
            registry=self.registry
        )
        
        self.llm_tokens_used = Counter(
            'llm_tokens_used_total',
            'Total number of tokens used in LLM requests',
            ['model', 'token_type'],
            registry=self.registry
        )
        
        # Prolog metrics
        self.prolog_queries_total = Counter(
            'prolog_queries_total',
            'Total number of Prolog queries',
            ['query_type', 'status'],
            registry=self.registry
        )
        
        self.prolog_execution_time = Histogram(
            'prolog_execution_time_seconds',
            'Prolog query execution time in seconds',
            ['query_type'],
            buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.25, 0.5],
            registry=self.registry
        )
        
        # System health metrics
        self.active_sessions = Gauge(
            'active_reasoning_sessions',
            'Number of active reasoning sessions',
            registry=self.registry
        )
        
        self.active_graphs = Gauge(
            'active_reasoning_graphs',
            'Number of active reasoning graphs',
            registry=self.registry
        )
        
        # Custom metrics for business KPIs
        self.successful_reasoning_rate = Gauge(
            'successful_reasoning_rate',
            'Rate of successful reasoning operations',
            ['domain'],
            registry=self.registry
        )
        
        self.average_confidence_by_domain = Gauge(
            'average_confidence_by_domain',
            'Average confidence score by domain',
            ['domain'],
            registry=self.registry
        )
    
    def record_reasoning_request(self, domain: str, status: str, model: str = "gpt-4o"):
        """Record a reasoning request."""
        self.reasoning_requests_total.labels(domain=domain, status=status, model=model).inc()
    
    def record_reasoning_response_time(self, domain: str, stage: str, duration: float):
        """Record reasoning response time."""
        self.reasoning_response_time.labels(domain=domain, stage=stage).observe(duration)
    
    def record_reasoning_confidence(self, domain: str, stage: str, confidence: float):
        """Record confidence score."""
        self.reasoning_confidence.labels(domain=domain, stage=stage).observe(confidence)
    
    def record_reasoning_error(self, domain: str, error_type: str, stage: str):
        """Record a reasoning error."""
        self.reasoning_errors_total.labels(domain=domain, error_type=error_type, stage=stage).inc()
    
    def record_ruleset_execution(self, ruleset_id: str, domain: str, status: str, duration: float):
        """Record ruleset execution metrics."""
        self.ruleset_executions_total.labels(ruleset_id=ruleset_id, domain=domain, status=status).inc()
        self.ruleset_execution_time.labels(ruleset_id=ruleset_id, domain=domain).observe(duration)
    
    def record_graph_operation(self, operation_type: str, status: str):
        """Record graph operation metrics."""
        self.graph_operations_total.labels(operation_type=operation_type, status=status).inc()
    
    def update_graph_size(self, graph_id: str, node_count: int, edge_count: int):
        """Update graph size metrics."""
        self.graph_size.labels(graph_id=graph_id, metric_type="nodes").set(node_count)
        self.graph_size.labels(graph_id=graph_id, metric_type="edges").set(edge_count)
    
    def record_llm_request(self, model: str, status: str, duration: float, 
                          prompt_tokens: int = 0, completion_tokens: int = 0):
        """Record LLM request metrics."""
        self.llm_requests_total.labels(model=model, status=status).inc()
        self.llm_response_time.labels(model=model).observe(duration)
        
        if prompt_tokens > 0:
            self.llm_tokens_used.labels(model=model, token_type="prompt").inc(prompt_tokens)
        if completion_tokens > 0:
            self.llm_tokens_used.labels(model=model, token_type="completion").inc(completion_tokens)
    
    def record_prolog_query(self, query_type: str, status: str, duration: float):
        """Record Prolog query metrics."""
        self.prolog_queries_total.labels(query_type=query_type, status=status).inc()
        self.prolog_execution_time.labels(query_type=query_type).observe(duration)
    
    def update_active_sessions(self, count: int):
        """Update active sessions count."""
        self.active_sessions.set(count)
    
    def update_active_graphs(self, count: int):
        """Update active graphs count."""
        self.active_graphs.set(count)
    
    def update_success_rate(self, domain: str, success_rate: float):
        """Update success rate for a domain."""
        self.successful_reasoning_rate.labels(domain=domain).set(success_rate)
    
    def update_average_confidence(self, domain: str, avg_confidence: float):
        """Update average confidence for a domain."""
        self.average_confidence_by_domain.labels(domain=domain).set(avg_confidence)
    
    def get_metrics(self) -> str:
        """Get metrics in Prometheus format."""
        return generate_latest(self.registry)
    
    def get_metrics_content_type(self) -> str:
        """Get the content type for metrics."""
        return CONTENT_TYPE_LATEST


# Global metrics service instance
metrics_service = ReasoningMetricsService()


class MetricsMiddleware:
    """Middleware for automatically collecting metrics."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            
            # Extract domain from path or headers
            domain = self._extract_domain(scope)
            
            try:
                await self.app(scope, receive, send)
                
                # Record successful request
                duration = time.time() - start_time
                metrics_service.record_reasoning_request(domain, "success")
                metrics_service.record_reasoning_response_time(domain, "total", duration)
                
            except Exception as e:
                # Record failed request
                duration = time.time() - start_time
                metrics_service.record_reasoning_request(domain, "error")
                metrics_service.record_reasoning_error(domain, type(e).__name__, "request")
                metrics_service.record_reasoning_response_time(domain, "error", duration)
                raise
        else:
            await self.app(scope, receive, send)
    
    def _extract_domain(self, scope) -> str:
        """Extract domain from request."""
        path = scope.get("path", "")
        
        if "/api/v1/reason" in path:
            return "reasoning"
        elif "/api/v1/rulesets" in path:
            return "rulesets"
        elif "/api/v1/graphs" in path:
            return "graphs"
        else:
            return "other"


class MetricsDecorator:
    """Decorator for adding metrics to functions."""
    
    def __init__(self, operation_type: str, domain: str = "general"):
        self.operation_type = operation_type
        self.domain = domain
    
    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                
                # Record success metrics
                duration = time.time() - start_time
                metrics_service.record_reasoning_response_time(self.domain, self.operation_type, duration)
                
                # Record confidence if available
                if hasattr(result, 'confidence'):
                    metrics_service.record_reasoning_confidence(self.domain, self.operation_type, result.confidence)
                
                return result
                
            except Exception as e:
                # Record error metrics
                duration = time.time() - start_time
                metrics_service.record_reasoning_error(self.domain, type(e).__name__, self.operation_type)
                metrics_service.record_reasoning_response_time(self.domain, f"{self.operation_type}_error", duration)
                raise
        
        return wrapper
