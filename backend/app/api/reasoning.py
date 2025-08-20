"""
Reasoning endpoints for the XReason API.
"""

from fastapi import APIRouter, HTTPException, Depends
from app.models.reasoning import ReasoningRequest, ReasoningResponse
from app.models.base import BaseResponse
from app.services.orchestration_service import OrchestrationService
from app.services.symbolic_service import SymbolicService
from app.services.knowledge_service import KnowledgeService
from app.core.config import settings

router = APIRouter(prefix="/reason", tags=["reasoning"])


# Dependency injection
def get_orchestration_service() -> OrchestrationService:
    return OrchestrationService()


def get_symbolic_service() -> SymbolicService:
    return SymbolicService()


def get_knowledge_service() -> KnowledgeService:
    return KnowledgeService()


@router.post("/", response_model=ReasoningResponse)
async def reason(
    request: ReasoningRequest,
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Main reasoning endpoint that orchestrates the complete reasoning pipeline.
    
    This endpoint combines:
    - LLM hypothesis generation (System 1)
    - Symbolic rule checking (System 2)
    - Knowledge base verification
    - Final answer synthesis
    
    Args:
        request: Reasoning request with question and optional context
        
    Returns:
        ReasoningResponse with answer, trace, and confidence
    """
    
    try:
        # Validate request
        validation = await orchestration_service.validate_request(request)
        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid request: {', '.join(validation['issues'])}"
            )
        
        # Execute reasoning pipeline
        response = await orchestration_service.reason(request)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/rules", response_model=BaseResponse)
async def get_rules(
    domain: str = None,
    symbolic_service: SymbolicService = Depends(get_symbolic_service)
):
    """
    Get available rule sets.
    
    Args:
        domain: Optional domain filter (healthcare, finance, general)
        
    Returns:
        List of available rule sets
    """
    
    try:
        if domain:
            if domain not in symbolic_service.rule_sets:
                raise HTTPException(
                    status_code=404,
                    detail=f"Domain '{domain}' not found"
                )
            rule_sets = {domain: symbolic_service.rule_sets[domain]}
        else:
            rule_sets = symbolic_service.rule_sets
        
        return BaseResponse(
            success=True,
            message="Rule sets retrieved successfully",
            data={
                "rule_sets": rule_sets,
                "available_domains": list(symbolic_service.rule_sets.keys())
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving rule sets: {str(e)}"
        )


@router.get("/knowledge", response_model=BaseResponse)
async def get_knowledge_summary(
    domain: str = None,
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """
    Get knowledge base summary.
    
    Args:
        domain: Optional domain filter
        
    Returns:
        Knowledge base summary
    """
    
    try:
        summary = knowledge_service.get_knowledge_summary(domain)
        
        return BaseResponse(
            success=True,
            message="Knowledge summary retrieved successfully",
            data=summary
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving knowledge summary: {str(e)}"
        )


@router.get("/capabilities", response_model=BaseResponse)
async def get_capabilities(
    domain: str = None,
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Get reasoning capabilities summary.
    
    Args:
        domain: Optional domain filter
        
    Returns:
        Summary of reasoning capabilities
    """
    
    try:
        capabilities = await orchestration_service.get_reasoning_summary(domain)
        
        return BaseResponse(
            success=True,
            message="Capabilities retrieved successfully",
            data=capabilities
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving capabilities: {str(e)}"
        )


@router.post("/validate", response_model=BaseResponse)
async def validate_request(
    request: ReasoningRequest,
    orchestration_service: OrchestrationService = Depends(get_orchestration_service)
):
    """
    Validate a reasoning request without executing it.
    
    Args:
        request: Reasoning request to validate
        
    Returns:
        Validation results
    """
    
    try:
        validation = await orchestration_service.validate_request(request)
        
        return BaseResponse(
            success=validation["valid"],
            message="Request validation completed",
            data=validation
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error validating request: {str(e)}"
        )
