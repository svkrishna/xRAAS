"""
Graph Persistence API
REST endpoints for saving and loading knowledge graphs.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import logging

from ..services.graph_persistence import create_persistence_service
from ..services.modern_reasoning_service import KnowledgeGraph

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/graphs", tags=["Graph Persistence"])


class GraphSaveRequest(BaseModel):
    """Request model for saving a graph."""
    filename: Optional[str] = None
    save_to_neo4j: bool = False
    neo4j_graph_name: str = "xreason_knowledge_graph"
    description: Optional[str] = None


class GraphLoadRequest(BaseModel):
    """Request model for loading a graph."""
    source: str = "json"  # "json" or "neo4j"
    filepath: Optional[str] = None
    neo4j_graph_name: str = "xreason_knowledge_graph"


class GraphInfo(BaseModel):
    """Graph information model."""
    filename: str
    filepath: str
    created_at: Optional[str] = None
    node_count: int
    edge_count: int
    size_bytes: Optional[int] = None
    description: Optional[str] = None


class GraphSaveResponse(BaseModel):
    """Response model for graph save operation."""
    success: bool
    results: Dict[str, str]
    message: str


class GraphLoadResponse(BaseModel):
    """Response model for graph load operation."""
    success: bool
    graph_info: Dict[str, Any]
    message: str


class GraphListResponse(BaseModel):
    """Response model for listing graphs."""
    success: bool
    graphs: Dict[str, List[GraphInfo]]
    total_count: int


# Initialize persistence service
persistence_service = create_persistence_service()


@router.post("/save", response_model=GraphSaveResponse)
async def save_graph(
    request: GraphSaveRequest,
    graph_data: Dict[str, Any] = None
) -> GraphSaveResponse:
    """
    Save a knowledge graph to JSON and optionally Neo4j.
    
    Args:
        request: Save configuration
        graph_data: Graph data to save (nodes and edges)
    
    Returns:
        Save operation results
    """
    try:
        # Create graph from data
        graph = KnowledgeGraph()
        
        # Clear default domain knowledge
        graph.nodes.clear()
        graph.edges.clear()
        graph.graph.clear()
        
        # Add nodes from data
        for node_data in graph_data.get("nodes", []):
            from ..services.modern_reasoning_service import GraphNode
            node = GraphNode(
                id=node_data["id"],
                label=node_data["label"],
                node_type=node_data["node_type"],
                properties=node_data.get("properties", {}),
                confidence=node_data.get("confidence", 1.0)
            )
            graph.add_node(node)
        
        # Add edges from data
        for edge_data in graph_data.get("edges", []):
            from ..services.modern_reasoning_service import GraphEdge
            edge = GraphEdge(
                source=edge_data["source"],
                target=edge_data["target"],
                relationship=edge_data["relationship"],
                properties=edge_data.get("properties", {}),
                confidence=edge_data.get("confidence", 1.0)
            )
            graph.add_edge(edge)
        
        # Save graph
        results = persistence_service.save_graph(
            graph=graph,
            filename=request.filename,
            save_to_neo4j=request.save_to_neo4j,
            neo4j_graph_name=request.neo4j_graph_name
        )
        
        return GraphSaveResponse(
            success=True,
            results=results,
            message=f"Graph saved successfully with {len(graph.nodes)} nodes and {len(graph.edges)} edges"
        )
        
    except Exception as e:
        logger.error(f"Error saving graph: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save graph: {str(e)}")


@router.post("/load", response_model=GraphLoadResponse)
async def load_graph(request: GraphLoadRequest) -> GraphLoadResponse:
    """
    Load a knowledge graph from JSON or Neo4j.
    
    Args:
        request: Load configuration
    
    Returns:
        Loaded graph information
    """
    try:
        # Load graph
        graph = persistence_service.load_graph(
            source=request.source,
            filepath=request.filepath,
            neo4j_graph_name=request.neo4j_graph_name
        )
        
        # Prepare graph info
        graph_info = {
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "nodes": [
                {
                    "id": node.id,
                    "label": node.label,
                    "node_type": node.node_type,
                    "confidence": node.confidence
                }
                for node in graph.nodes.values()
            ],
            "edges": [
                {
                    "source": edge.source,
                    "target": edge.target,
                    "relationship": edge.relationship,
                    "confidence": edge.confidence
                }
                for edge in graph.edges.values()
            ]
        }
        
        return GraphLoadResponse(
            success=True,
            graph_info=graph_info,
            message=f"Graph loaded successfully with {len(graph.nodes)} nodes and {len(graph.edges)} edges"
        )
        
    except Exception as e:
        logger.error(f"Error loading graph: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load graph: {str(e)}")


@router.get("/list", response_model=GraphListResponse)
async def list_graphs() -> GraphListResponse:
    """
    List all available graphs from both JSON and Neo4j sources.
    
    Returns:
        List of available graphs
    """
    try:
        graphs = persistence_service.list_available_graphs()
        
        # Convert to response format
        json_graphs = [
            GraphInfo(
                filename=g["filename"],
                filepath=g["filepath"],
                created_at=g["created_at"],
                node_count=g["node_count"],
                edge_count=g["edge_count"],
                size_bytes=g["size_bytes"]
            )
            for g in graphs["json"]
        ]
        
        neo4j_graphs = [
            GraphInfo(
                filename=g["graph_name"],
                filepath="neo4j://" + g["graph_name"],
                node_count=g["node_count"],
                edge_count=g["edge_count"]
            )
            for g in graphs["neo4j"]
        ]
        
        total_count = len(json_graphs) + len(neo4j_graphs)
        
        return GraphListResponse(
            success=True,
            graphs={
                "json": json_graphs,
                "neo4j": neo4j_graphs
            },
            total_count=total_count
        )
        
    except Exception as e:
        logger.error(f"Error listing graphs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list graphs: {str(e)}")


@router.delete("/{source}/{identifier}")
async def delete_graph(source: str, identifier: str) -> Dict[str, Any]:
    """
    Delete a graph from the specified source.
    
    Args:
        source: Source type ("json" or "neo4j")
        identifier: Graph identifier (filename or graph name)
    
    Returns:
        Delete operation result
    """
    try:
        success = persistence_service.delete_graph(source, identifier)
        
        if success:
            return {
                "success": True,
                "message": f"Graph '{identifier}' deleted successfully from {source}"
            }
        else:
            raise HTTPException(status_code=404, detail=f"Graph '{identifier}' not found in {source}")
        
    except Exception as e:
        logger.error(f"Error deleting graph: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete graph: {str(e)}")


@router.post("/upload")
async def upload_graph_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
) -> GraphSaveResponse:
    """
    Upload a graph file (JSON format) and save it.
    
    Args:
        file: Graph file to upload
        description: Optional description
    
    Returns:
        Upload operation result
    """
    try:
        # Read file content
        content = await file.read()
        graph_data = json.loads(content.decode('utf-8'))
        
        # Create save request
        request = GraphSaveRequest(
            filename=file.filename,
            description=description
        )
        
        # Save graph
        return await save_graph(request, graph_data)
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        logger.error(f"Error uploading graph file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload graph file: {str(e)}")


@router.get("/stats")
async def get_graph_statistics() -> Dict[str, Any]:
    """
    Get statistics about stored graphs.
    
    Returns:
        Graph statistics
    """
    try:
        graphs = persistence_service.list_available_graphs()
        
        # Calculate statistics
        total_graphs = len(graphs["json"]) + len(graphs["neo4j"])
        total_nodes = sum(g["node_count"] for g in graphs["json"]) + sum(g["node_count"] for g in graphs["neo4j"])
        total_edges = sum(g["edge_count"] for g in graphs["json"]) + sum(g["edge_count"] for g in graphs["neo4j"])
        
        return {
            "success": True,
            "statistics": {
                "total_graphs": total_graphs,
                "json_graphs": len(graphs["json"]),
                "neo4j_graphs": len(graphs["neo4j"]),
                "total_nodes": total_nodes,
                "total_edges": total_edges,
                "average_nodes_per_graph": total_nodes / total_graphs if total_graphs > 0 else 0,
                "average_edges_per_graph": total_edges / total_graphs if total_graphs > 0 else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting graph statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get graph statistics: {str(e)}")


# Import json for the upload endpoint
import json
