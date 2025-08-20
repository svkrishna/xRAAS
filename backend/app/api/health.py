"""
Health check endpoints.
"""

from fastapi import APIRouter, HTTPException
from app.models.base import BaseResponse
from app.core.config import settings
import time

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=BaseResponse)
async def health_check():
    """Basic health check endpoint."""
    return BaseResponse(
        success=True,
        message="XReason API is healthy",
        data={
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.app_version,
            "app_name": settings.app_name
        }
    )


@router.get("/detailed", response_model=BaseResponse)
async def detailed_health_check():
    """Detailed health check with component status."""
    try:
        # Check OpenAI connection (basic check)
        from app.services.llm_service import LLMService
        llm_service = LLMService()
        
        # Check symbolic service
        from app.services.symbolic_service import SymbolicService
        symbolic_service = SymbolicService()
        
        # Check knowledge service
        from app.services.knowledge_service import KnowledgeService
        knowledge_service = KnowledgeService()
        
        components = {
            "llm_service": {
                "status": "healthy",
                "model": llm_service.model
            },
            "symbolic_service": {
                "status": "healthy",
                "rule_sets": list(symbolic_service.rule_sets.keys())
            },
            "knowledge_service": {
                "status": "healthy",
                "facts_count": len(knowledge_service.facts)
            }
        }
        
        return BaseResponse(
            success=True,
            message="All components are healthy",
            data={
                "status": "healthy",
                "timestamp": time.time(),
                "version": settings.app_version,
                "components": components
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )
