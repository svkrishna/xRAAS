"""
Main FastAPI application for XReason.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging

from app.core.config import settings
from app.api import reasoning_router, health_router, rulesets_router, reasoning_graphs_router, setup_metrics_instrumentation, pilots_router, agents_router, financial_analysis_router, commercial_router
from app.api.auth import router as auth_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting XReason API...")
    logger.info(f"App Name: {settings.app_name}")
    logger.info(f"Version: {settings.app_version}")
    logger.info(f"Debug Mode: {settings.debug}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down XReason API...")


# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    description="Reasoning as a Service (RaaS) - A modular reasoning pipeline combining LLM intuition with symbolic/rule-based checks",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


# Setup metrics instrumentation
setup_metrics_instrumentation(app)

# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(reasoning_router, prefix="/api/v1", tags=["reasoning"])
app.include_router(rulesets_router, tags=["rulesets"])
app.include_router(reasoning_graphs_router, tags=["reasoning-graphs"])
app.include_router(pilots_router, prefix="/api/v1", tags=["pilots"])
app.include_router(agents_router, tags=["agents"])
app.include_router(financial_analysis_router, tags=["financial_analysis"])
app.include_router(commercial_router, tags=["commercial"])
app.include_router(auth_router, tags=["authentication"])


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "description": "Reasoning as a Service (RaaS) API",
        "docs": "/docs",
        "health": "/health",
        "api": "/api/v1"
    }


@app.get("/info", tags=["info"])
async def info():
    """API information endpoint."""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "description": "A modular reasoning pipeline combining LLM intuition (System 1) with symbolic/rule-based checks (System 2)",
        "features": [
            "LLM-based hypothesis generation",
            "Symbolic rule verification",
            "Knowledge graph validation",
            "Explainable reasoning traces",
            "Domain-specific rule sets (Healthcare, Finance)",
            "Confidence scoring",
            "OpenAPI documentation"
        ],
        "endpoints": {
            "health": "/health",
            "reasoning": "/api/v1/reason",
            "rules": "/api/v1/reason/rules",
            "knowledge": "/api/v1/reason/knowledge",
            "capabilities": "/api/v1/reason/capabilities",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
