"""
API endpoints for reasoning graph visualization and management.
"""

from typing import List, Optional, Union
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import Response, JSONResponse
import json

from app.models.reasoning_graph import (
    ReasoningGraph, GraphVisualizationData, GraphStatistics, 
    GraphExportFormat, GraphExportRequest
)
from app.models.base import BaseResponse, ErrorResponse
from app.services.reasoning_graph_service import ReasoningGraphService

router = APIRouter(prefix="/api/v1/graphs", tags=["reasoning-graphs"])


@router.get("/", response_model=List[ReasoningGraph])
async def list_graphs(
    session_id: Optional[str] = None,
    graph_service: ReasoningGraphService = Depends(lambda: ReasoningGraphService())
) -> List[ReasoningGraph]:
    """List all reasoning graphs with optional filtering by session."""
    try:
        if session_id:
            # Filter by session ID
            graphs = [g for g in graph_service.graphs.values() if g.session_id == session_id]
        else:
            graphs = list(graph_service.graphs.values())
        
        return graphs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list graphs: {str(e)}")


@router.get("/{graph_id}", response_model=ReasoningGraph)
async def get_graph(
    graph_id: str,
    graph_service: ReasoningGraphService = Depends(lambda: ReasoningGraphService())
) -> ReasoningGraph:
    """Get a specific reasoning graph by ID."""
    try:
        graph = graph_service.graphs.get(graph_id)
        if not graph:
            raise HTTPException(status_code=404, detail=f"Graph not found: {graph_id}")
        return graph
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get graph: {str(e)}")


@router.get("/{graph_id}/visualization", response_model=GraphVisualizationData)
async def get_graph_visualization(
    graph_id: str,
    layout_type: str = Query("hierarchical", description="Layout type: hierarchical, circular, force_directed, kamada_kawai"),
    graph_service: ReasoningGraphService = Depends(lambda: ReasoningGraphService())
) -> GraphVisualizationData:
    """Get visualization data for a reasoning graph with custom layouts."""
    try:
        return graph_service.generate_visualization_data(graph_id, layout_type)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate visualization: {str(e)}")


@router.get("/{graph_id}/plotly")
async def get_plotly_visualization(
    graph_id: str,
    graph_service: ReasoningGraphService = Depends(lambda: ReasoningGraphService())
):
    """Get an interactive Plotly visualization of the reasoning graph."""
    try:
        fig = graph_service.generate_plotly_visualization(graph_id)
        return JSONResponse(content=fig.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate Plotly visualization: {str(e)}")


@router.get("/{graph_id}/statistics", response_model=GraphStatistics)
async def get_graph_statistics(
    graph_id: str,
    graph_service: ReasoningGraphService = Depends(lambda: ReasoningGraphService())
) -> GraphStatistics:
    """Get statistics about a reasoning graph."""
    try:
        return graph_service.calculate_statistics(graph_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate statistics: {str(e)}")


@router.post("/{graph_id}/export")
async def export_graph(
    graph_id: str,
    export_request: GraphExportRequest,
    graph_service: ReasoningGraphService = Depends(lambda: ReasoningGraphService())
):
    """Export a reasoning graph in various formats."""
    try:
        result = graph_service.export_graph(
            graph_id=graph_id,
            format=export_request.format,
            include_metadata=export_request.include_metadata,
            include_positions=export_request.include_positions,
            styling=export_request.styling
        )
        
        # Set appropriate content type based on format
        content_type_map = {
            GraphExportFormat.JSON: "application/json",
            GraphExportFormat.DOT: "text/plain",
            GraphExportFormat.GEXF: "application/xml",
            GraphExportFormat.GRAPHML: "application/xml",
            GraphExportFormat.PNG: "image/png",
            GraphExportFormat.SVG: "image/svg+xml",
            GraphExportFormat.PDF: "application/pdf"
        }
        
        content_type = content_type_map.get(export_request.format, "text/plain")
        
        if isinstance(result, str):
            return Response(content=result, media_type=content_type)
        else:
            return Response(content=result, media_type=content_type)
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export graph: {str(e)}")


@router.get("/{graph_id}/export/{format}")
async def export_graph_simple(
    graph_id: str,
    format: GraphExportFormat,
    graph_service: ReasoningGraphService = Depends(lambda: ReasoningGraphService())
):
    """Export a reasoning graph with simple format specification."""
    try:
        result = graph_service.export_graph(graph_id=graph_id, format=format)
        
        # Set appropriate content type
        content_type_map = {
            GraphExportFormat.JSON: "application/json",
            GraphExportFormat.DOT: "text/plain",
            GraphExportFormat.GEXF: "application/xml",
            GraphExportFormat.GRAPHML: "application/xml",
            GraphExportFormat.PNG: "image/png",
            GraphExportFormat.SVG: "image/svg+xml",
            GraphExportFormat.PDF: "application/pdf"
        }
        
        content_type = content_type_map.get(format, "text/plain")
        
        if isinstance(result, str):
            return Response(content=result, media_type=content_type)
        else:
            return Response(content=result, media_type=content_type)
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export graph: {str(e)}")


@router.delete("/{graph_id}")
async def delete_graph(
    graph_id: str,
    graph_service: ReasoningGraphService = Depends(lambda: ReasoningGraphService())
) -> BaseResponse:
    """Delete a reasoning graph."""
    try:
        if graph_id not in graph_service.graphs:
            raise HTTPException(status_code=404, detail=f"Graph not found: {graph_id}")
        
        del graph_service.graphs[graph_id]
        
        return BaseResponse(
            success=True,
            message=f"Graph {graph_id} deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete graph: {str(e)}")


@router.get("/stats/summary")
async def get_graph_stats_summary(
    graph_service: ReasoningGraphService = Depends(lambda: ReasoningGraphService())
) -> dict:
    """Get summary statistics for all graphs."""
    try:
        graphs = list(graph_service.graphs.values())
        
        total_graphs = len(graphs)
        total_nodes = sum(len(graph.nodes) for graph in graphs)
        total_edges = sum(len(graph.edges) for graph in graphs)
        
        # Count by session
        session_counts = {}
        for graph in graphs:
            session_counts[graph.session_id] = session_counts.get(graph.session_id, 0) + 1
        
        # Average nodes and edges per graph
        avg_nodes = total_nodes / total_graphs if total_graphs > 0 else 0
        avg_edges = total_edges / total_graphs if total_graphs > 0 else 0
        
        return {
            "total_graphs": total_graphs,
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "average_nodes_per_graph": round(avg_nodes, 2),
            "average_edges_per_graph": round(avg_edges, 2),
            "sessions": session_counts,
            "unique_sessions": len(session_counts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.get("/formats/supported")
async def get_supported_formats() -> dict:
    """Get list of supported export formats."""
    return {
        "formats": [
            {"value": format.value, "name": format.name, "description": f"Export as {format.value.upper()}"}
            for format in GraphExportFormat
        ],
        "recommendations": {
            "interactive": GraphExportFormat.JSON.value,
            "documentation": GraphExportFormat.DOT.value,
            "images": [GraphExportFormat.PNG.value, GraphExportFormat.SVG.value],
            "publication": GraphExportFormat.PDF.value
        }
    }


@router.post("/create-from-session", response_model=ReasoningGraph)
async def create_graph_from_session(
    session_id: str,
    layout_type: str = "hierarchical",
    graph_service: ReasoningGraphService = Depends(lambda: ReasoningGraphService())
) -> ReasoningGraph:
    """Create a reasoning graph from a reasoning session."""
    try:
        # This would typically load the session and its traces from the database
        # For now, we'll create a mock graph
        graph = graph_service.create_graph(session_id)
        
        # Add some sample nodes and edges
        input_node = graph_service.add_input_node(
            graph_id=graph.id,
            question="Sample question",
            context={"domain": "legal"}
        )
        
        llm_node = graph_service.add_llm_hypothesis_node(
            graph_id=graph.id,
            hypothesis="Sample hypothesis",
            confidence=0.85
        )
        
        rule_node = graph_service.add_rule_node(
            graph_id=graph.id,
            rule_name="Sample Rule",
            rule_type="keyword_rule",
            result={"passed": True},
            confidence=0.9
        )
        
        # Add edges
        graph_service.add_edge(
            graph_id=graph.id,
            source_id=input_node.id,
            target_id=llm_node.id,
            edge_type="generates",
            label="Generates Hypothesis"
        )
        
        graph_service.add_edge(
            graph_id=graph.id,
            source_id=llm_node.id,
            target_id=rule_node.id,
            edge_type="validates",
            label="Validates Hypothesis"
        )
        
        # Calculate layout
        graph_service.calculate_layout(graph, layout_type)
        
        return graph
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create graph: {str(e)}")
