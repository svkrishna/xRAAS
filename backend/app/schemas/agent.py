"""
Pydantic schemas for AI agents and related entities.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
from enum import Enum


class AgentType(str, Enum):
    """Types of AI agents."""
    REASONING_AGENT = "reasoning_agent"
    KNOWLEDGE_AGENT = "knowledge_agent"
    VALIDATION_AGENT = "validation_agent"
    COORDINATION_AGENT = "coordination_agent"
    SPECIALIST_AGENT = "specialist_agent"
    LEARNING_AGENT = "learning_agent"


class AgentState(str, Enum):
    """Agent states."""
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    LEARNING = "learning"
    ERROR = "error"


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    """Task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MemoryType(str, Enum):
    """Memory types."""
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    PATTERN = "pattern"


class KnowledgeType(str, Enum):
    """Knowledge types."""
    FACT = "fact"
    RULE = "rule"
    PATTERN = "pattern"
    RELATIONSHIP = "relationship"


class LearningType(str, Enum):
    """Learning types."""
    PATTERN = "pattern"
    BEHAVIOR = "behavior"
    STRATEGY = "strategy"


# Base Models
class AgentBase(BaseModel):
    """Base agent model."""
    agent_type: AgentType
    name: str
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    configuration: Optional[Dict[str, Any]] = None


class AgentCreate(AgentBase):
    """Create agent request."""
    pass


class AgentUpdate(BaseModel):
    """Update agent request."""
    name: Optional[str] = None
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    configuration: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class AgentResponse(AgentBase):
    """Agent response."""
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AgentSessionBase(BaseModel):
    """Base agent session model."""
    user_id: Optional[str] = None
    domain: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentSessionCreate(AgentSessionBase):
    """Create agent session request."""
    pass


class AgentSessionResponse(AgentSessionBase):
    """Agent session response."""
    id: str
    agent_id: str
    session_id: str
    status: str
    created_at: datetime
    last_activity: Optional[datetime] = None
    task_count: int
    
    class Config:
        from_attributes = True


class AgentTaskBase(BaseModel):
    """Base agent task model."""
    task_type: str
    priority: TaskPriority = TaskPriority.MEDIUM
    input_data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentTaskCreate(AgentTaskBase):
    """Create agent task request."""
    pass


class AgentTaskUpdate(BaseModel):
    """Update agent task request."""
    status: Optional[TaskStatus] = None
    output_data: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentTaskResponse(AgentTaskBase):
    """Agent task response."""
    id: str
    agent_id: str
    session_id: str
    status: TaskStatus
    output_data: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    processing_time: Optional[float] = None
    
    class Config:
        from_attributes = True


class AgentMemoryBase(BaseModel):
    """Base agent memory model."""
    memory_type: MemoryType
    key: str
    value: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None


class AgentMemoryCreate(AgentMemoryBase):
    """Create agent memory request."""
    pass


class AgentMemoryResponse(AgentMemoryBase):
    """Agent memory response."""
    id: str
    agent_id: str
    access_count: int
    created_at: datetime
    last_accessed: datetime
    
    class Config:
        from_attributes = True


class AgentKnowledgeBase(BaseModel):
    """Base agent knowledge model."""
    knowledge_type: KnowledgeType
    content: Dict[str, Any]
    source: Optional[str] = None
    confidence: float = 1.0


class AgentKnowledgeCreate(AgentKnowledgeBase):
    """Create agent knowledge request."""
    pass


class AgentKnowledgeResponse(AgentKnowledgeBase):
    """Agent knowledge response."""
    id: str
    agent_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class AgentLearningBase(BaseModel):
    """Base agent learning model."""
    learning_type: LearningType
    input_data: Optional[Dict[str, Any]] = None
    feedback: Optional[Dict[str, Any]] = None
    adaptation: Optional[Dict[str, Any]] = None
    success_rate: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentLearningCreate(AgentLearningBase):
    """Create agent learning request."""
    pass


class AgentLearningResponse(AgentLearningBase):
    """Agent learning response."""
    id: str
    agent_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Request/Response Models for API
class AgentProcessingRequest(BaseModel):
    """Request for agent processing."""
    session_id: str
    input_data: Dict[str, Any]
    agent_types: Optional[List[AgentType]] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    metadata: Optional[Dict[str, Any]] = None


class AgentProcessingResponse(BaseModel):
    """Response from agent processing."""
    success: bool
    session_id: str
    task_id: str
    result: Optional[Dict[str, Any]] = None
    confidence: float
    reasoning: str
    processing_time: float
    agent_used: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentStatusResponse(BaseModel):
    """Agent status response."""
    agent_id: str
    agent_type: AgentType
    state: AgentState
    capabilities: List[str]
    performance_metrics: Dict[str, Any]
    last_activity: Optional[datetime] = None


class AgentSessionRequest(BaseModel):
    """Create agent session request."""
    user_id: Optional[str] = None
    domain: Optional[str] = None
    agent_type: Optional[AgentType] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentSessionInfoResponse(BaseModel):
    """Agent session information response."""
    session_id: str
    user_id: Optional[str] = None
    domain: Optional[str] = None
    created_at: datetime
    last_activity: Optional[datetime] = None
    status: str
    task_count: int
    agent_status: List[AgentStatusResponse]


class AgentMemoryRequest(BaseModel):
    """Agent memory operation request."""
    session_id: str
    memory_type: MemoryType
    key: str
    value: Optional[Dict[str, Any]] = None
    operation: str = "get"  # get, set, delete


class AgentMemoryResponse(BaseModel):
    """Agent memory operation response."""
    success: bool
    session_id: str
    memory_type: MemoryType
    key: str
    value: Optional[Dict[str, Any]] = None
    access_count: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentLearningRequest(BaseModel):
    """Agent learning request."""
    session_id: str
    learning_type: LearningType
    input_data: Dict[str, Any]
    feedback: Optional[Dict[str, Any]] = None
    adaptation_target: Optional[str] = None


class AgentLearningResponse(BaseModel):
    """Agent learning response."""
    success: bool
    session_id: str
    learning_type: LearningType
    adaptation_applied: bool
    success_rate: Optional[float] = None
    reasoning: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentKnowledgeRequest(BaseModel):
    """Agent knowledge integration request."""
    session_id: str
    knowledge_type: KnowledgeType
    content: Dict[str, Any]
    source: Optional[str] = None
    confidence: float = 1.0
    operation: str = "add"  # add, query, update, delete


class AgentKnowledgeResponse(BaseModel):
    """Agent knowledge integration response."""
    success: bool
    session_id: str
    knowledge_type: KnowledgeType
    content: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None
    source: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentPerformanceMetrics(BaseModel):
    """Agent performance metrics."""
    agent_id: str
    agent_type: AgentType
    tasks_completed: int
    success_rate: float
    avg_response_time: float
    total_response_time: float
    last_activity: Optional[datetime] = None


class AgentSystemStatus(BaseModel):
    """Overall agent system status."""
    total_agents: int
    active_agents: int
    total_sessions: int
    active_sessions: int
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    avg_processing_time: float
    system_health: str
    agent_statuses: List[AgentStatusResponse]
    performance_metrics: List[AgentPerformanceMetrics]
