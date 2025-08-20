"""
Reasoning Graph Models for visualizing reasoning steps and persistence.
"""

from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField
from datetime import datetime
import json


class NodeType(str, Enum):
    """Types of nodes in the reasoning graph."""
    INPUT = "input"
    LLM_HYPOTHESIS = "llm_hypothesis"
    SYMBOLIC_RULE = "symbolic_rule"
    KNOWLEDGE_CHECK = "knowledge_check"
    PROLOG_RULE = "prolog_rule"
    PYTHON_RULE = "python_rule"
    REGEX_RULE = "regex_rule"
    KEYWORD_RULE = "keyword_rule"
    DECISION = "decision"
    OUTPUT = "output"


class EdgeType(str, Enum):
    """Types of edges in the reasoning graph."""
    GENERATES = "generates"
    VALIDATES = "validates"
    CONTRADICTS = "contradicts"
    SUPPORTS = "supports"
    REQUIRES = "requires"
    LEADS_TO = "leads_to"


class GraphNode(BaseModel):
    """A node in the reasoning graph."""
    id: str = Field(..., description="Unique node identifier")
    type: NodeType = Field(..., description="Type of reasoning node")
    label: str = Field(..., description="Human-readable label")
    content: Dict[str, Any] = Field(..., description="Node content/data")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Node creation timestamp")
    
    # Position for visualization
    x: Optional[float] = Field(default=None, description="X coordinate for visualization")
    y: Optional[float] = Field(default=None, description="Y coordinate for visualization")


class GraphEdge(BaseModel):
    """An edge in the reasoning graph."""
    id: str = Field(..., description="Unique edge identifier")
    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    type: EdgeType = Field(..., description="Type of relationship")
    label: str = Field(..., description="Edge label")
    weight: float = Field(default=1.0, ge=0.0, le=10.0, description="Edge weight")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ReasoningGraph(BaseModel):
    """Complete reasoning graph representation."""
    id: str = Field(..., description="Unique graph identifier")
    session_id: str = Field(..., description="Associated reasoning session ID")
    nodes: List[GraphNode] = Field(default_factory=list, description="Graph nodes")
    edges: List[GraphEdge] = Field(default_factory=list, description="Graph edges")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Graph metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Graph creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


# Database Models
class ReasoningGraphDB(SQLModel, table=True):
    """Database model for storing reasoning graphs."""
    __tablename__ = "reasoning_graphs"
    
    id: str = SQLField(primary_key=True, index=True)
    session_id: str = SQLField(foreign_key="reasoning_sessions.id", index=True)
    nodes_data: str = SQLField(description="JSON serialized nodes")
    edges_data: str = SQLField(description="JSON serialized edges")
    metadata: str = SQLField(description="JSON serialized metadata")
    created_at: datetime = SQLField(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = SQLField(default_factory=datetime.utcnow)
    
    # Tenant isolation
    tenant_id: Optional[str] = SQLField(default=None, index=True)


class GraphExecutionLog(SQLModel, table=True):
    """Database model for logging graph executions."""
    __tablename__ = "graph_execution_logs"
    
    id: int = SQLField(primary_key=True, autoincrement=True)
    graph_id: str = SQLField(foreign_key="reasoning_graphs.id", index=True)
    node_id: str = SQLField(index=True)
    execution_time_ms: float = SQLField(description="Execution time in milliseconds")
    success: bool = SQLField(index=True)
    error_message: Optional[str] = None
    input_data: str = SQLField(description="JSON serialized input data")
    output_data: str = SQLField(description="JSON serialized output data")
    
    created_at: datetime = SQLField(default_factory=datetime.utcnow, index=True)
    tenant_id: Optional[str] = SQLField(default=None, index=True)


# Response Models
class GraphVisualizationData(BaseModel):
    """Data for graph visualization."""
    nodes: List[Dict[str, Any]] = Field(..., description="Nodes with position data")
    edges: List[Dict[str, Any]] = Field(..., description="Edges with styling")
    layout: Dict[str, Any] = Field(default_factory=dict, description="Layout configuration")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Visualization metadata")


class GraphStatistics(BaseModel):
    """Statistics about a reasoning graph."""
    total_nodes: int
    total_edges: int
    node_types: Dict[str, int] = Field(..., description="Count by node type")
    edge_types: Dict[str, int] = Field(..., description="Count by edge type")
    average_confidence: float
    execution_time_ms: float
    critical_path: List[str] = Field(..., description="Critical path through the graph")
    bottlenecks: List[str] = Field(default_factory=list, description="Bottleneck nodes")


class GraphExportFormat(str, Enum):
    """Supported export formats for reasoning graphs."""
    JSON = "json"
    DOT = "dot"
    GEXF = "gexf"
    GRAPHML = "graphml"
    PNG = "png"
    SVG = "svg"
    PDF = "pdf"


class GraphExportRequest(BaseModel):
    """Request for exporting a reasoning graph."""
    graph_id: str
    format: GraphExportFormat
    include_metadata: bool = Field(default=True, description="Include metadata in export")
    include_positions: bool = Field(default=True, description="Include node positions")
    styling: Dict[str, Any] = Field(default_factory=dict, description="Custom styling options")
