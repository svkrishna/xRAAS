"""
FastAPI endpoints for AI agents.
"""

import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.services.ai_agent_service import ai_agent_service
from app.schemas.agent import (
    AgentProcessingRequest, AgentProcessingResponse,
    AgentStatusResponse, AgentSystemStatus,
    AgentSessionRequest, AgentSessionInfoResponse,
    AgentMemoryRequest, AgentMemoryResponse,
    AgentLearningRequest, AgentLearningResponse,
    AgentKnowledgeRequest, AgentKnowledgeResponse,
    AgentType, TaskPriority, MemoryType, LearningType, KnowledgeType
)
from app.services.metrics_service import metrics_service

router = APIRouter(prefix="/api/v1/agents", tags=["AI Agents"])


@router.post("/sessions", response_model=Dict[str, str])
async def create_session(request: AgentSessionRequest):
    """Create a new agent session."""
    try:
        session_id = await ai_agent_service.create_session(
            user_id=request.user_id,
            domain=request.domain
        )
        
        metrics_service.record_agent_session_created(
            session_id=session_id,
            user_id=request.user_id,
            domain=request.domain
        )
        
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.get("/sessions/{session_id}", response_model=AgentSessionInfoResponse)
async def get_session_info(session_id: str):
    """Get information about a session."""
    try:
        session_info = await ai_agent_service.get_session_info(session_id)
        agent_statuses = await ai_agent_service.get_all_agents_status()
        
        return AgentSessionInfoResponse(
            session_id=session_info["session_id"],
            user_id=session_info.get("user_id"),
            domain=session_info.get("domain"),
            created_at=session_info["created_at"],
            last_activity=session_info.get("last_activity"),
            status=session_info["status"],
            task_count=session_info["task_count"],
            agent_status=agent_statuses
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session info: {str(e)}")


@router.post("/process", response_model=AgentProcessingResponse)
async def process_with_agents(request: AgentProcessingRequest):
    """Process input using AI agents."""
    try:
        # Process with agents
        result = await ai_agent_service.process_with_agents(
            session_id=request.session_id,
            input_data=request.input_data,
            agent_types=request.agent_types,
            priority=request.priority
        )
        
        # Record metrics
        metrics_service.record_agent_processing(
            session_id=request.session_id,
            agent_types=[agent.value for agent in (request.agent_types or [])],
            success=result.success,
            confidence=result.confidence,
            processing_time=result.metadata.get("response_time", 0.0)
        )
        
        return AgentProcessingResponse(
            success=result.success,
            session_id=request.session_id,
            task_id=str(uuid.uuid4()),  # Generate task ID
            result=result.data,
            confidence=result.confidence,
            reasoning=result.reasoning,
            processing_time=result.metadata.get("response_time", 0.0),
            agent_used=result.metadata.get("agent_used", "unknown"),
            metadata=result.metadata
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/status", response_model=AgentSystemStatus)
async def get_system_status():
    """Get overall agent system status."""
    try:
        return await ai_agent_service.get_system_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")


@router.get("/agents", response_model=List[AgentStatusResponse])
async def get_all_agents_status():
    """Get status of all agents."""
    try:
        return await ai_agent_service.get_all_agents_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent statuses: {str(e)}")


@router.get("/agents/{agent_id}", response_model=AgentStatusResponse)
async def get_agent_status(agent_id: str):
    """Get status of a specific agent."""
    try:
        return await ai_agent_service.get_agent_status(agent_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent status: {str(e)}")


@router.post("/memory", response_model=AgentMemoryResponse)
async def memory_operation(request: AgentMemoryRequest):
    """Perform memory operations (get, set, delete)."""
    try:
        # Get agent from session
        session_info = await ai_agent_service.get_session_info(request.session_id)
        
        # For now, use reasoning agent's memory
        reasoning_agent = ai_agent_service.agents.get("reasoning_001")
        if not reasoning_agent:
            raise HTTPException(status_code=500, detail="Reasoning agent not available")
        
        if request.operation == "get":
            value = reasoning_agent.memory.get_memory(
                request.key, 
                request.memory_type.value
            )
            access_count = 0  # TODO: Track access count
            
        elif request.operation == "set":
            reasoning_agent.memory.add_memory(
                request.key,
                request.value,
                request.memory_type.value
            )
            value = request.value
            access_count = 0
            
        elif request.operation == "delete":
            # TODO: Implement delete operation
            value = None
            access_count = 0
            
        else:
            raise HTTPException(status_code=400, detail=f"Invalid operation: {request.operation}")
        
        return AgentMemoryResponse(
            success=True,
            session_id=request.session_id,
            memory_type=request.memory_type,
            key=request.key,
            value=value,
            access_count=access_count
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Memory operation failed: {str(e)}")


@router.post("/learning", response_model=AgentLearningResponse)
async def learning_operation(request: AgentLearningRequest):
    """Perform learning operations."""
    try:
        # Get agent from session
        session_info = await ai_agent_service.get_session_info(request.session_id)
        
        # For now, use reasoning agent for learning
        reasoning_agent = ai_agent_service.agents.get("reasoning_001")
        if not reasoning_agent:
            raise HTTPException(status_code=500, detail="Reasoning agent not available")
        
        # Update patterns in memory
        if request.learning_type == LearningType.PATTERN:
            pattern_key = f"pattern_{request.input_data.get('pattern', 'unknown')}"
            reasoning_agent.memory.update_patterns(pattern_key)
            adaptation_applied = True
            success_rate = 0.8  # TODO: Calculate actual success rate
            reasoning = f"Pattern {pattern_key} updated in memory"
            
        elif request.learning_type == LearningType.BEHAVIOR:
            # TODO: Implement behavior learning
            adaptation_applied = False
            success_rate = None
            reasoning = "Behavior learning not yet implemented"
            
        elif request.learning_type == LearningType.STRATEGY:
            # TODO: Implement strategy learning
            adaptation_applied = False
            success_rate = None
            reasoning = "Strategy learning not yet implemented"
            
        else:
            raise HTTPException(status_code=400, detail=f"Invalid learning type: {request.learning_type}")
        
        return AgentLearningResponse(
            success=True,
            session_id=request.session_id,
            learning_type=request.learning_type,
            adaptation_applied=adaptation_applied,
            success_rate=success_rate,
            reasoning=reasoning
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning operation failed: {str(e)}")


@router.post("/knowledge", response_model=AgentKnowledgeResponse)
async def knowledge_operation(request: AgentKnowledgeRequest):
    """Perform knowledge integration operations."""
    try:
        # Get agent from session
        session_info = await ai_agent_service.get_session_info(request.session_id)
        
        # Use knowledge agent for knowledge operations
        knowledge_agent = ai_agent_service.agents.get("knowledge_001")
        if not knowledge_agent:
            raise HTTPException(status_code=500, detail="Knowledge agent not available")
        
        if request.operation == "add":
            # Add knowledge to agent's memory
            knowledge_key = f"knowledge_{request.knowledge_type.value}_{request.content.get('id', 'unknown')}"
            knowledge_agent.memory.add_memory(
                knowledge_key,
                request.content,
                "long_term"
            )
            content = request.content
            confidence = request.confidence
            source = request.source
            reasoning = f"Knowledge {knowledge_key} added to agent memory"
            
        elif request.operation == "query":
            # Query knowledge from agent's memory
            knowledge_key = f"knowledge_{request.knowledge_type.value}_{request.content.get('id', 'unknown')}"
            content = knowledge_agent.memory.get_memory(knowledge_key, "long_term")
            confidence = request.confidence if content else 0.0
            source = request.source
            reasoning = f"Knowledge {knowledge_key} queried from agent memory"
            
        elif request.operation == "update":
            # Update existing knowledge
            knowledge_key = f"knowledge_{request.knowledge_type.value}_{request.content.get('id', 'unknown')}"
            knowledge_agent.memory.add_memory(
                knowledge_key,
                request.content,
                "long_term"
            )
            content = request.content
            confidence = request.confidence
            source = request.source
            reasoning = f"Knowledge {knowledge_key} updated in agent memory"
            
        elif request.operation == "delete":
            # TODO: Implement delete operation
            content = None
            confidence = 0.0
            source = None
            reasoning = f"Knowledge deletion not yet implemented"
            
        else:
            raise HTTPException(status_code=400, detail=f"Invalid operation: {request.operation}")
        
        return AgentKnowledgeResponse(
            success=True,
            session_id=request.session_id,
            knowledge_type=request.knowledge_type,
            content=content,
            confidence=confidence,
            source=source
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge operation failed: {str(e)}")


@router.post("/reasoning", response_model=AgentProcessingResponse)
async def reasoning_agent_processing(request: AgentProcessingRequest):
    """Process with reasoning agent specifically."""
    try:
        # Process with reasoning agent
        result = await ai_agent_service.process_with_agents(
            session_id=request.session_id,
            input_data=request.input_data,
            agent_types=[AgentType.REASONING_AGENT],
            priority=request.priority
        )
        
        return AgentProcessingResponse(
            success=result.success,
            session_id=request.session_id,
            task_id=str(uuid.uuid4()),
            result=result.data,
            confidence=result.confidence,
            reasoning=result.reasoning,
            processing_time=result.metadata.get("response_time", 0.0),
            agent_used="reasoning_001",
            metadata=result.metadata
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reasoning processing failed: {str(e)}")


@router.post("/knowledge-integration", response_model=AgentProcessingResponse)
async def knowledge_agent_processing(request: AgentProcessingRequest):
    """Process with knowledge agent specifically."""
    try:
        # Process with knowledge agent
        result = await ai_agent_service.process_with_agents(
            session_id=request.session_id,
            input_data=request.input_data,
            agent_types=[AgentType.KNOWLEDGE_AGENT],
            priority=request.priority
        )
        
        return AgentProcessingResponse(
            success=result.success,
            session_id=request.session_id,
            task_id=str(uuid.uuid4()),
            result=result.data,
            confidence=result.confidence,
            reasoning=result.reasoning,
            processing_time=result.metadata.get("response_time", 0.0),
            agent_used="knowledge_001",
            metadata=result.metadata
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge integration failed: {str(e)}")


@router.post("/validation", response_model=AgentProcessingResponse)
async def validation_agent_processing(request: AgentProcessingRequest):
    """Process with validation agent specifically."""
    try:
        # Process with validation agent
        result = await ai_agent_service.process_with_agents(
            session_id=request.session_id,
            input_data=request.input_data,
            agent_types=[AgentType.VALIDATION_AGENT],
            priority=request.priority
        )
        
        return AgentProcessingResponse(
            success=result.success,
            session_id=request.session_id,
            task_id=str(uuid.uuid4()),
            result=result.data,
            confidence=result.confidence,
            reasoning=result.reasoning,
            processing_time=result.metadata.get("response_time", 0.0),
            agent_used="validation_001",
            metadata=result.metadata
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation processing failed: {str(e)}")


@router.get("/health")
async def agent_health_check():
    """Health check for agent system."""
    try:
        system_status = await ai_agent_service.get_system_status()
        
        health_status = {
            "status": "healthy" if system_status.system_health == "healthy" else "degraded",
            "agents": {
                "total": system_status.total_agents,
                "active": system_status.active_agents
            },
            "sessions": {
                "total": system_status.total_sessions,
                "active": system_status.active_sessions
            },
            "performance": {
                "avg_processing_time": system_status.avg_processing_time,
                "total_tasks": system_status.total_tasks
            }
        }
        
        return JSONResponse(
            content=health_status,
            status_code=200 if health_status["status"] == "healthy" else 503
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "unhealthy", "error": str(e)},
            status_code=503
        )
