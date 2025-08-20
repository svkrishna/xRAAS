"""
API endpoints for Prometheus metrics.
"""

from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_fastapi_instrumentator import Instrumentator

from app.services.metrics_service import metrics_service

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/")
async def get_metrics() -> Response:
    """Get Prometheus metrics."""
    return Response(
        content=metrics_service.get_metrics(),
        media_type=metrics_service.get_metrics_content_type()
    )


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint with basic metrics."""
    return {
        "status": "healthy",
        "metrics_available": True,
        "endpoints": {
            "prometheus": "/metrics/",
            "health": "/metrics/health"
        }
    }


@router.get("/summary")
async def metrics_summary() -> dict:
    """Get a summary of current metrics."""
    # This would typically query the metrics and provide a summary
    # For now, return a basic structure
    return {
        "metrics_collected": True,
        "available_metrics": [
            "reasoning_requests_total",
            "reasoning_response_time_seconds",
            "reasoning_confidence_score",
            "reasoning_errors_total",
            "ruleset_executions_total",
            "graph_operations_total",
            "llm_requests_total",
            "prolog_queries_total",
            "active_reasoning_sessions",
            "active_reasoning_graphs"
        ],
        "labels": {
            "domains": ["reasoning", "rulesets", "graphs", "other"],
            "stages": ["llm_hypothesis", "rule_check", "knowledge_check", "total"],
            "models": ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
        }
    }


def setup_metrics_instrumentation(app):
    """Setup Prometheus instrumentation for the FastAPI app."""
    # Add standard FastAPI metrics
    Instrumentator().instrument(app).expose(app, include_in_schema=False, should_gzip=True)
    
    # Add custom metrics endpoint
    app.include_router(router, include_in_schema=False)
