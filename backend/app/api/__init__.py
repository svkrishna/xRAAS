"""
API endpoints for the XReason application.
"""

from .reasoning import router as reasoning_router
from .health import router as health_router
from .rulesets import router as rulesets_router
from .reasoning_graphs import router as reasoning_graphs_router
from .metrics import router as metrics_router, setup_metrics_instrumentation
from .pilots import router as pilots_router
from .agents import router as agents_router
from .financial_analysis import router as financial_analysis_router
from .commercial import router as commercial_router
