"""
API endpoints for extensible ruleset management.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse

from app.models.rulesets import (
    RulesetDefinition, RulesetExecutionResult, RulesetValidationResult,
    RuleExecutionResult
)
from app.models.base import BaseResponse, ErrorResponse
from app.services.ruleset_service import RulesetService

router = APIRouter(prefix="/api/v1/rulesets", tags=["rulesets"])


@router.get("/", response_model=List[RulesetDefinition])
async def list_rulesets(
    domain: Optional[str] = None,
    enabled: Optional[bool] = None,
    ruleset_service: RulesetService = Depends(lambda: RulesetService())
) -> List[RulesetDefinition]:
    """List all available rulesets with optional filtering."""
    try:
        if domain:
            return ruleset_service.get_rulesets_by_domain(domain)
        elif enabled is not None:
            rulesets = ruleset_service.get_all_rulesets()
            return [r for r in rulesets if r.enabled == enabled]
        else:
            return ruleset_service.get_all_rulesets()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list rulesets: {str(e)}")


@router.get("/{ruleset_id}", response_model=RulesetDefinition)
async def get_ruleset(
    ruleset_id: str,
    ruleset_service: RulesetService = Depends(lambda: RulesetService())
) -> RulesetDefinition:
    """Get a specific ruleset by ID."""
    try:
        ruleset = ruleset_service.get_ruleset(ruleset_id)
        if not ruleset:
            raise HTTPException(status_code=404, detail=f"Ruleset not found: {ruleset_id}")
        return ruleset
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get ruleset: {str(e)}")


@router.post("/", response_model=RulesetDefinition)
async def create_ruleset(
    ruleset: RulesetDefinition,
    ruleset_service: RulesetService = Depends(lambda: RulesetService())
) -> RulesetDefinition:
    """Create a new ruleset."""
    try:
        # Validate the ruleset
        validation = ruleset_service.validate_ruleset(ruleset)
        if not validation.valid:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid ruleset: {'; '.join(validation.errors)}"
            )
        
        # Load the ruleset
        created_ruleset = ruleset_service.load_ruleset_from_dict(ruleset.dict())
        return created_ruleset
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create ruleset: {str(e)}")


@router.post("/upload", response_model=RulesetDefinition)
async def upload_ruleset(
    file: UploadFile = File(...),
    ruleset_service: RulesetService = Depends(lambda: RulesetService())
) -> RulesetDefinition:
    """Upload a ruleset from YAML or JSON file."""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content
        content = await file.read()
        file_content = content.decode('utf-8')
        
        # Determine file type and load
        if file.filename.lower().endswith(('.yaml', '.yml')):
            import yaml
            data = yaml.safe_load(file_content)
        elif file.filename.lower().endswith('.json'):
            import json
            data = json.loads(file_content)
        else:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file format. Use YAML (.yaml/.yml) or JSON (.json)"
            )
        
        # Validate and load ruleset
        ruleset = RulesetDefinition(**data)
        validation = ruleset_service.validate_ruleset(ruleset)
        if not validation.valid:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid ruleset: {'; '.join(validation.errors)}"
            )
        
        created_ruleset = ruleset_service.load_ruleset_from_dict(data)
        return created_ruleset
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload ruleset: {str(e)}")


@router.post("/{ruleset_id}/validate", response_model=RulesetValidationResult)
async def validate_ruleset(
    ruleset_id: str,
    ruleset_service: RulesetService = Depends(lambda: RulesetService())
) -> RulesetValidationResult:
    """Validate a ruleset."""
    try:
        ruleset = ruleset_service.get_ruleset(ruleset_id)
        if not ruleset:
            raise HTTPException(status_code=404, detail=f"Ruleset not found: {ruleset_id}")
        
        return ruleset_service.validate_ruleset(ruleset)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate ruleset: {str(e)}")


@router.post("/{ruleset_id}/execute", response_model=RulesetExecutionResult)
async def execute_ruleset(
    ruleset_id: str,
    question: str,
    hypothesis: str,
    context: Optional[dict] = None,
    ruleset_service: RulesetService = Depends(lambda: RulesetService())
) -> RulesetExecutionResult:
    """Execute a ruleset against given input."""
    try:
        return await ruleset_service.execute_ruleset(
            ruleset_id=ruleset_id,
            question=question,
            hypothesis=hypothesis,
            context=context
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute ruleset: {str(e)}")


@router.delete("/{ruleset_id}")
async def delete_ruleset(
    ruleset_id: str,
    ruleset_service: RulesetService = Depends(lambda: RulesetService())
) -> BaseResponse:
    """Delete a ruleset."""
    try:
        ruleset = ruleset_service.get_ruleset(ruleset_id)
        if not ruleset:
            raise HTTPException(status_code=404, detail=f"Ruleset not found: {ruleset_id}")
        
        # Remove from service (in a real implementation, this would persist to DB)
        if ruleset_id in ruleset_service.rulesets:
            del ruleset_service.rulesets[ruleset_id]
        
        return BaseResponse(
            success=True,
            message=f"Ruleset {ruleset_id} deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete ruleset: {str(e)}")


@router.get("/domains/list")
async def list_domains(
    ruleset_service: RulesetService = Depends(lambda: RulesetService())
) -> dict:
    """List all available domains."""
    try:
        rulesets = ruleset_service.get_all_rulesets()
        domains = list(set(ruleset.domain for ruleset in rulesets))
        return {
            "domains": domains,
            "count": len(domains)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list domains: {str(e)}")


@router.get("/stats/summary")
async def get_ruleset_stats(
    ruleset_service: RulesetService = Depends(lambda: RulesetService())
) -> dict:
    """Get statistics about rulesets."""
    try:
        rulesets = ruleset_service.get_all_rulesets()
        
        # Calculate statistics
        total_rulesets = len(rulesets)
        enabled_rulesets = len([r for r in rulesets if r.enabled])
        total_rules = sum(len(ruleset.rules) for ruleset in rulesets)
        
        # Count by domain
        domain_counts = {}
        for ruleset in rulesets:
            domain = ruleset.domain
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        # Count by rule type
        rule_type_counts = {}
        for ruleset in rulesets:
            for rule in ruleset.rules:
                rule_type = rule.type.value
                rule_type_counts[rule_type] = rule_type_counts.get(rule_type, 0) + 1
        
        return {
            "total_rulesets": total_rulesets,
            "enabled_rulesets": enabled_rulesets,
            "total_rules": total_rules,
            "domains": domain_counts,
            "rule_types": rule_type_counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")
