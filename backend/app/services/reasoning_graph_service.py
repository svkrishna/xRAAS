"""
Reasoning Graph Service for visualizing and persisting reasoning steps.
"""

import json
import uuid
import time
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app.models.reasoning_graph import (
    ReasoningGraph, GraphNode, GraphEdge, NodeType, EdgeType,
    GraphVisualizationData, GraphStatistics, GraphExportFormat,
    ReasoningGraphDB, GraphExecutionLog
)
from app.models.reasoning import ReasoningTrace, ReasoningStage


class ReasoningGraphService:
    """Service for managing reasoning graphs with visualization and persistence."""
    
    def __init__(self):
        self.graphs: Dict[str, ReasoningGraph] = {}
        self.node_colors = {
            NodeType.INPUT: "#E3F2FD",  # Light blue
            NodeType.LLM_HYPOTHESIS: "#FFF3E0",  # Light orange
            NodeType.SYMBOLIC_RULE: "#E8F5E8",  # Light green
            NodeType.KNOWLEDGE_CHECK: "#F3E5F5",  # Light purple
            NodeType.PROLOG_RULE: "#E0F2F1",  # Light teal
            NodeType.PYTHON_RULE: "#FFF8E1",  # Light yellow
            NodeType.REGEX_RULE: "#FCE4EC",  # Light pink
            NodeType.KEYWORD_RULE: "#F1F8E9",  # Light lime
            NodeType.DECISION: "#FFEBEE",  # Light red
            NodeType.OUTPUT: "#FAFAFA",  # Light gray
        }
        
        self.edge_colors = {
            EdgeType.GENERATES: "#2196F3",  # Blue
            EdgeType.VALIDATES: "#4CAF50",  # Green
            EdgeType.CONTRADICTS: "#F44336",  # Red
            EdgeType.SUPPORTS: "#8BC34A",  # Light green
            EdgeType.REQUIRES: "#FF9800",  # Orange
            EdgeType.LEADS_TO: "#9C27B0",  # Purple
        }
    
    def create_graph(self, session_id: str) -> ReasoningGraph:
        """Create a new reasoning graph for a session."""
        graph_id = str(uuid.uuid4())
        graph = ReasoningGraph(
            id=graph_id,
            session_id=session_id,
            nodes=[],
            edges=[],
            metadata={
                "created_by": "reasoning_graph_service",
                "version": "1.0.0"
            }
        )
        self.graphs[graph_id] = graph
        return graph
    
    def add_input_node(self, graph_id: str, question: str, context: Optional[Dict[str, Any]] = None) -> GraphNode:
        """Add an input node to the graph."""
        graph = self.graphs.get(graph_id)
        if not graph:
            raise ValueError(f"Graph not found: {graph_id}")
        
        node_id = f"input_{len(graph.nodes)}"
        node = GraphNode(
            id=node_id,
            type=NodeType.INPUT,
            label="Input Question",
            content={
                "question": question,
                "context": context or {},
                "timestamp": datetime.utcnow().isoformat()
            },
            confidence=1.0,
            metadata={"stage": "input"}
        )
        
        graph.nodes.append(node)
        return node
    
    def add_llm_hypothesis_node(self, graph_id: str, hypothesis: str, confidence: float, metadata: Optional[Dict[str, Any]] = None) -> GraphNode:
        """Add an LLM hypothesis node to the graph."""
        graph = self.graphs.get(graph_id)
        if not graph:
            raise ValueError(f"Graph not found: {graph_id}")
        
        node_id = f"llm_hypothesis_{len(graph.nodes)}"
        node = GraphNode(
            id=node_id,
            type=NodeType.LLM_HYPOTHESIS,
            label="LLM Hypothesis",
            content={
                "hypothesis": hypothesis,
                "confidence": confidence,
                "timestamp": datetime.utcnow().isoformat()
            },
            confidence=confidence,
            metadata=metadata or {}
        )
        
        graph.nodes.append(node)
        return node
    
    def add_rule_node(self, graph_id: str, rule_name: str, rule_type: NodeType, result: Dict[str, Any], confidence: float) -> GraphNode:
        """Add a rule execution node to the graph."""
        graph = self.graphs.get(graph_id)
        if not graph:
            raise ValueError(f"Graph not found: {graph_id}")
        
        node_id = f"rule_{rule_type.value}_{len(graph.nodes)}"
        node = GraphNode(
            id=node_id,
            type=rule_type,
            label=f"{rule_type.value.replace('_', ' ').title()}: {rule_name}",
            content={
                "rule_name": rule_name,
                "rule_type": rule_type.value,
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            },
            confidence=confidence,
            metadata={"rule_execution": True}
        )
        
        graph.nodes.append(node)
        return node
    
    def add_edge(self, graph_id: str, source_id: str, target_id: str, edge_type: EdgeType, label: str, weight: float = 1.0) -> GraphEdge:
        """Add an edge between nodes."""
        graph = self.graphs.get(graph_id)
        if not graph:
            raise ValueError(f"Graph not found: {graph_id}")
        
        edge_id = f"edge_{len(graph.edges)}"
        edge = GraphEdge(
            id=edge_id,
            source=source_id,
            target=target_id,
            type=edge_type,
            label=label,
            weight=weight
        )
        
        graph.edges.append(edge)
        return edge
    
    def build_graph_from_traces(self, session_id: str, traces: List[ReasoningTrace]) -> ReasoningGraph:
        """Build a reasoning graph from reasoning traces."""
        graph = self.create_graph(session_id)
        
        # Add input node (assuming first trace has the question)
        if traces:
            first_trace = traces[0]
            input_node = self.add_input_node(
                graph_id=graph.id,
                question=first_trace.metadata.get("question", "Unknown question"),
                context=first_trace.metadata
            )
        
        previous_node = input_node
        
        for i, trace in enumerate(traces):
            # Create node based on trace stage
            if trace.stage == ReasoningStage.LLM_HYPOTHESIS:
                node = self.add_llm_hypothesis_node(
                    graph_id=graph.id,
                    hypothesis=trace.output,
                    confidence=trace.confidence,
                    metadata=trace.metadata
                )
                edge_type = EdgeType.GENERATES
                edge_label = "Generates Hypothesis"
                
            elif trace.stage == ReasoningStage.RULE_CHECK:
                node = self.add_rule_node(
                    graph_id=graph.id,
                    rule_name="Symbolic Rule Check",
                    rule_type=NodeType.SYMBOLIC_RULE,
                    result={"output": trace.output, "metadata": trace.metadata},
                    confidence=trace.confidence
                )
                edge_type = EdgeType.VALIDATES
                edge_label = "Validates Hypothesis"
                
            elif trace.stage == ReasoningStage.KNOWLEDGE_CHECK:
                node = self.add_rule_node(
                    graph_id=graph.id,
                    rule_name="Knowledge Graph Check",
                    rule_type=NodeType.KNOWLEDGE_CHECK,
                    result={"output": trace.output, "metadata": trace.metadata},
                    confidence=trace.confidence
                )
                edge_type = EdgeType.SUPPORTS
                edge_label = "Supports with Knowledge"
                
            else:
                # Generic node for other stages
                node = GraphNode(
                    id=f"stage_{trace.stage.value}_{i}",
                    type=NodeType.DECISION,
                    label=f"{trace.stage.value.replace('_', ' ').title()}",
                    content={"output": trace.output, "metadata": trace.metadata},
                    confidence=trace.confidence,
                    metadata={"stage": trace.stage.value}
                )
                graph.nodes.append(node)
                edge_type = EdgeType.LEADS_TO
                edge_label = "Leads to Next Stage"
            
            # Add edge from previous node
            if previous_node:
                self.add_edge(
                    graph_id=graph.id,
                    source_id=previous_node.id,
                    target_id=node.id,
                    edge_type=edge_type,
                    label=edge_label,
                    weight=trace.confidence
                )
            
            previous_node = node
        
        # Add output node
        if traces:
            final_trace = traces[-1]
            output_node = GraphNode(
                id="output_final",
                type=NodeType.OUTPUT,
                label="Final Answer",
                content={
                    "answer": final_trace.output,
                    "confidence": final_trace.confidence,
                    "timestamp": datetime.utcnow().isoformat()
                },
                confidence=final_trace.confidence,
                metadata={"final_output": True}
            )
            graph.nodes.append(output_node)
            
            if previous_node:
                self.add_edge(
                    graph_id=graph.id,
                    source_id=previous_node.id,
                    target_id=output_node.id,
                    edge_type=EdgeType.LEADS_TO,
                    label="Final Result",
                    weight=final_trace.confidence
                )
        
        return graph
    
    def calculate_layout(self, graph: ReasoningGraph, layout_type: str = "hierarchical") -> ReasoningGraph:
        """Calculate node positions for visualization with custom layouts."""
        if not graph.nodes:
            return graph
        
        # Create NetworkX graph for layout calculation
        nx_graph = nx.DiGraph()
        
        # Add nodes
        for node in graph.nodes:
            nx_graph.add_node(node.id, pos=(0, 0))
        
        # Add edges
        for edge in graph.edges:
            nx_graph.add_edge(edge.source, edge.target)
        
        # Calculate layout based on type
        if layout_type == "hierarchical":
            pos = self._hierarchical_layout(nx_graph, graph)
        elif layout_type == "circular":
            pos = self._circular_layout(nx_graph, graph)
        elif layout_type == "force_directed":
            pos = self._force_directed_layout(nx_graph, graph)
        elif layout_type == "kamada_kawai":
            pos = self._kamada_kawai_layout(nx_graph, graph)
        else:
            pos = self._spring_layout(nx_graph, graph)
        
        # Update node positions
        for node in graph.nodes:
            if node.id in pos:
                node.x, node.y = pos[node.id]
        
        return graph
    
    def _hierarchical_layout(self, nx_graph, graph: ReasoningGraph) -> dict:
        """Hierarchical layout based on reasoning stages."""
        pos = {}
        
        # Group nodes by type for hierarchical positioning
        type_order = [
            NodeType.INPUT,
            NodeType.LLM_HYPOTHESIS,
            NodeType.SYMBOLIC_RULE,
            NodeType.KNOWLEDGE_CHECK,
            NodeType.PROLOG_RULE,
            NodeType.PYTHON_RULE,
            NodeType.REGEX_RULE,
            NodeType.KEYWORD_RULE,
            NodeType.DECISION,
            NodeType.OUTPUT
        ]
        
        # Calculate positions
        for i, node_type in enumerate(type_order):
            type_nodes = [n for n in graph.nodes if n.type == node_type]
            if type_nodes:
                y_pos = i * 2
                for j, node in enumerate(type_nodes):
                    x_pos = (j - len(type_nodes) / 2) * 3
                    pos[node.id] = (x_pos, y_pos)
        
        return pos
    
    def _circular_layout(self, nx_graph, graph: ReasoningGraph) -> dict:
        """Circular layout for compact visualization."""
        try:
            return nx.circular_layout(nx_graph, scale=5)
        except:
            return self._fallback_layout(graph)
    
    def _force_directed_layout(self, nx_graph, graph: ReasoningGraph) -> dict:
        """Force-directed layout for natural node distribution."""
        try:
            return nx.spring_layout(nx_graph, k=3, iterations=100, scale=5)
        except:
            return self._fallback_layout(graph)
    
    def _kamada_kawai_layout(self, nx_graph, graph: ReasoningGraph) -> dict:
        """Kamada-Kawai layout for optimal node spacing."""
        try:
            return nx.kamada_kawai_layout(nx_graph, scale=5)
        except:
            return self._fallback_layout(graph)
    
    def _spring_layout(self, nx_graph, graph: ReasoningGraph) -> dict:
        """Spring layout with custom parameters."""
        try:
            return nx.spring_layout(nx_graph, k=2, iterations=50, scale=4)
        except:
            return self._fallback_layout(graph)
    
    def _fallback_layout(self, graph: ReasoningGraph) -> dict:
        """Fallback layout when other layouts fail."""
        pos = {}
        for i, node in enumerate(graph.nodes):
            pos[node.id] = (i * 2, i % 3)
        return pos
    
    def generate_visualization_data(self, graph_id: str, layout_type: str = "hierarchical") -> GraphVisualizationData:
        """Generate visualization data for the graph with custom layouts."""
        graph = self.graphs.get(graph_id)
        if not graph:
            raise ValueError(f"Graph not found: {graph_id}")
        
        # Calculate layout if not already done or if layout type changed
        if not any(node.x is not None for node in graph.nodes):
            graph = self.calculate_layout(graph, layout_type)
        
        # Prepare nodes for visualization
        nodes_data = []
        for node in graph.nodes:
            node_data = {
                "id": node.id,
                "label": node.label,
                "type": node.type.value,
                "x": node.x or 0,
                "y": node.y or 0,
                "confidence": node.confidence,
                "color": self.node_colors.get(node.type, "#FFFFFF"),
                "size": 20 + (node.confidence * 30),  # Size based on confidence
                "content": node.content,
                "metadata": node.metadata
            }
            nodes_data.append(node_data)
        
        # Prepare edges for visualization
        edges_data = []
        for edge in graph.edges:
            edge_data = {
                "id": edge.id,
                "source": edge.source,
                "target": edge.target,
                "label": edge.label,
                "type": edge.type.value,
                "weight": edge.weight,
                "color": self.edge_colors.get(edge.type, "#000000"),
                "width": 1 + (edge.weight * 2),  # Width based on weight
                "metadata": edge.metadata
            }
            edges_data.append(edge_data)
        
        return GraphVisualizationData(
            nodes=nodes_data,
            edges=edges_data,
            layout={
                "type": "force",
                "gravity": 0.1,
                "repulsion": 100,
                "attraction": 0.1
            },
            metadata={
                "total_nodes": len(graph.nodes),
                "total_edges": len(graph.edges),
                "created_at": graph.created_at.isoformat()
            }
        )
    
    def generate_plotly_visualization(self, graph_id: str) -> go.Figure:
        """Generate an interactive Plotly visualization."""
        vis_data = self.generate_visualization_data(graph_id)
        
        # Create scatter plot for nodes
        node_x = [node["x"] for node in vis_data.nodes]
        node_y = [node["y"] for node in vis_data.nodes]
        node_text = [f"{node['label']}<br>Confidence: {node['confidence']:.2f}" for node in vis_data.nodes]
        node_colors = [node["color"] for node in vis_data.nodes]
        node_sizes = [node["size"] for node in vis_data.nodes]
        
        # Create figure
        fig = go.Figure()
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            text=[node["label"] for node in vis_data.nodes],
            textposition="top center",
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color='black')
            ),
            hovertemplate='<b>%{text}</b><br>Confidence: %{customdata:.2f}<extra></extra>',
            customdata=[node["confidence"] for node in vis_data.nodes],
            name="Nodes"
        ))
        
        # Add edges
        for edge in vis_data.edges:
            source_node = next(n for n in vis_data.nodes if n["id"] == edge["source"])
            target_node = next(n for n in vis_data.nodes if n["id"] == edge["target"])
            
            fig.add_trace(go.Scatter(
                x=[source_node["x"], target_node["x"]],
                y=[source_node["y"], target_node["y"]],
                mode='lines',
                line=dict(width=edge["width"], color=edge["color"]),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Update layout
        fig.update_layout(
            title="Reasoning Graph Visualization",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white'
        )
        
        return fig
    
    def calculate_statistics(self, graph_id: str) -> GraphStatistics:
        """Calculate advanced statistics about the graph."""
        graph = self.graphs.get(graph_id)
        if not graph:
            raise ValueError(f"Graph not found: {graph_id}")
        
        # Count node types
        node_types = {}
        for node in graph.nodes:
            node_type = node.type.value
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        # Count edge types
        edge_types = {}
        for edge in graph.edges:
            edge_type = edge.type.value
            edge_types[edge_type] = edge_types.get(edge_type, 0) + 1
        
        # Calculate confidence statistics
        confidences = [node.confidence for node in graph.nodes]
        average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        min_confidence = min(confidences) if confidences else 0.0
        max_confidence = max(confidences) if confidences else 0.0
        
        # Find critical path using graph analysis
        critical_path = self._find_critical_path(graph)
        
        # Find bottlenecks and weak points
        bottlenecks = self._find_bottlenecks(graph)
        
        # Calculate graph complexity metrics
        complexity_metrics = self._calculate_complexity_metrics(graph)
        
        # Find reasoning chains
        reasoning_chains = self._find_reasoning_chains(graph)
        
        return GraphStatistics(
            total_nodes=len(graph.nodes),
            total_edges=len(graph.edges),
            node_types=node_types,
            edge_types=edge_types,
            average_confidence=average_confidence,
            execution_time_ms=0.0,  # Would be calculated from actual execution
            critical_path=critical_path,
            bottlenecks=bottlenecks
        )
    
    def _find_critical_path(self, graph: ReasoningGraph) -> List[str]:
        """Find the critical path through the reasoning graph."""
        if not graph.nodes or not graph.edges:
            return []
        
        # Create NetworkX graph for path analysis
        nx_graph = nx.DiGraph()
        
        # Add nodes with confidence as weight
        for node in graph.nodes:
            nx_graph.add_node(node.id, confidence=node.confidence)
        
        # Add edges with confidence as weight
        for edge in graph.edges:
            nx_graph.add_edge(edge.source, edge.target, weight=edge.weight)
        
        # Find all paths from input to output nodes
        input_nodes = [n.id for n in graph.nodes if n.type == NodeType.INPUT]
        output_nodes = [n.id for n in graph.nodes if n.type == NodeType.OUTPUT]
        
        if not input_nodes or not output_nodes:
            return []
        
        # Find shortest path (highest confidence path)
        try:
            path = nx.shortest_path(nx_graph, input_nodes[0], output_nodes[0], weight='weight')
            return path
        except nx.NetworkXNoPath:
            # Fallback: return nodes with highest confidence
            return [node.id for node in sorted(graph.nodes, key=lambda x: x.confidence, reverse=True)[:3]]
    
    def _find_bottlenecks(self, graph: ReasoningGraph) -> List[str]:
        """Find bottlenecks and weak points in the reasoning graph."""
        bottlenecks = []
        
        # Nodes with low confidence
        low_confidence_nodes = [node.id for node in graph.nodes if node.confidence < 0.5]
        bottlenecks.extend(low_confidence_nodes)
        
        # Nodes with high in-degree but low confidence (potential bottlenecks)
        in_degree = {}
        for edge in graph.edges:
            in_degree[edge.target] = in_degree.get(edge.target, 0) + 1
        
        for node in graph.nodes:
            if in_degree.get(node.id, 0) > 2 and node.confidence < 0.7:
                bottlenecks.append(node.id)
        
        return list(set(bottlenecks))  # Remove duplicates
    
    def _calculate_complexity_metrics(self, graph: ReasoningGraph) -> Dict[str, float]:
        """Calculate complexity metrics for the graph."""
        if not graph.nodes:
            return {}
        
        # Create NetworkX graph
        nx_graph = nx.DiGraph()
        for edge in graph.edges:
            nx_graph.add_edge(edge.source, edge.target)
        
        metrics = {}
        
        # Density
        metrics['density'] = nx.density(nx_graph) if graph.edges else 0.0
        
        # Average degree
        if graph.nodes:
            total_degree = sum(nx_graph.degree(node.id) for node in graph.nodes)
            metrics['average_degree'] = total_degree / len(graph.nodes)
        else:
            metrics['average_degree'] = 0.0
        
        # Diameter (longest shortest path)
        try:
            metrics['diameter'] = nx.diameter(nx_graph)
        except:
            metrics['diameter'] = 0.0
        
        # Average clustering coefficient
        try:
            metrics['clustering_coefficient'] = nx.average_clustering(nx_graph)
        except:
            metrics['clustering_coefficient'] = 0.0
        
        return metrics
    
    def _find_reasoning_chains(self, graph: ReasoningGraph) -> List[List[str]]:
        """Find reasoning chains in the graph."""
        if not graph.edges:
            return []
        
        # Create NetworkX graph
        nx_graph = nx.DiGraph()
        for edge in graph.edges:
            nx_graph.add_edge(edge.source, edge.target)
        
        # Find all simple paths
        input_nodes = [n.id for n in graph.nodes if n.type == NodeType.INPUT]
        output_nodes = [n.id for n in graph.nodes if n.type == NodeType.OUTPUT]
        
        chains = []
        for input_node in input_nodes:
            for output_node in output_nodes:
                try:
                    paths = list(nx.all_simple_paths(nx_graph, input_node, output_node))
                    chains.extend(paths)
                except:
                    continue
        
        return chains[:5]  # Limit to top 5 chains
    
    def export_graph(self, graph_id: str, format: GraphExportFormat, **kwargs) -> Union[str, bytes]:
        """Export the graph in various formats."""
        graph = self.graphs.get(graph_id)
        if not graph:
            raise ValueError(f"Graph not found: {graph_id}")
        
        if format == GraphExportFormat.JSON:
            return json.dumps(graph.dict(), indent=2, default=str)
        
        elif format == GraphExportFormat.DOT:
            return self._export_dot(graph)
        
        elif format == GraphExportFormat.PNG:
            return self._export_image(graph, "png")
        
        elif format == GraphExportFormat.SVG:
            return self._export_image(graph, "svg")
        
        elif format == GraphExportFormat.PDF:
            return self._export_image(graph, "pdf")
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_dot(self, graph: ReasoningGraph) -> str:
        """Export graph as DOT format."""
        dot_lines = ["digraph ReasoningGraph {"]
        dot_lines.append("  rankdir=LR;")
        dot_lines.append("  node [shape=box, style=filled];")
        
        # Add nodes
        for node in graph.nodes:
            color = self.node_colors.get(node.type, "#FFFFFF")
            dot_lines.append(f'  "{node.id}" [label="{node.label}", fillcolor="{color}"];')
        
        # Add edges
        for edge in graph.edges:
            color = self.edge_colors.get(edge.type, "#000000")
            dot_lines.append(f'  "{edge.source}" -> "{edge.target}" [label="{edge.label}", color="{color}"];')
        
        dot_lines.append("}")
        return "\n".join(dot_lines)
    
    def _export_image(self, graph: ReasoningGraph, format: str) -> bytes:
        """Export graph as image."""
        # Create NetworkX graph
        nx_graph = nx.DiGraph()
        
        # Add nodes and edges
        for node in graph.nodes:
            nx_graph.add_node(node.id, label=node.label, color=self.node_colors.get(node.type, "#FFFFFF"))
        
        for edge in graph.edges:
            nx_graph.add_edge(edge.source, edge.target, label=edge.label)
        
        # Create matplotlib figure
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(nx_graph, k=3, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(nx_graph, pos, node_color=[nx_graph.nodes[node]["color"] for node in nx_graph.nodes()])
        
        # Draw edges
        nx.draw_networkx_edges(nx_graph, pos, edge_color='gray', arrows=True)
        
        # Draw labels
        nx.draw_networkx_labels(nx_graph, pos, labels={node: nx_graph.nodes[node]["label"] for node in nx_graph.nodes()})
        
        plt.title("Reasoning Graph")
        plt.axis('off')
        
        # Save to bytes
        import io
        buf = io.BytesIO()
        plt.savefig(buf, format=format, bbox_inches='tight')
        plt.close()
        return buf.getvalue()
