"""
Graph Persistence Service
Save and load knowledge graphs to/from JSON and Neo4j.
"""

import json
import os
import uuid
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import logging
from pathlib import Path

# Optional Neo4j import
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

from .modern_reasoning_service import KnowledgeGraph, GraphNode, GraphEdge

logger = logging.getLogger(__name__)


class GraphPersistenceManager:
    """Manages persistence operations for knowledge graphs."""
    
    def __init__(self, storage_dir: str = "./data/graphs"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def save_graph_to_json(self, graph: KnowledgeGraph, filename: str = None) -> str:
        """Save knowledge graph to JSON file."""
        try:
            if not filename:
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                filename = f"knowledge_graph_{timestamp}.json"
            
            filepath = self.storage_dir / filename
            
            # Convert graph to serializable format
            graph_data = {
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "version": "1.0",
                    "node_count": len(graph.nodes),
                    "edge_count": len(graph.edges),
                    "description": "XReason Knowledge Graph"
                },
                "nodes": [],
                "edges": []
            }
            
            # Serialize nodes
            for node_id, node in graph.nodes.items():
                node_data = {
                    "id": node_id,
                    "label": node.label,
                    "node_type": node.node_type,
                    "properties": node.properties,
                    "confidence": node.confidence
                }
                graph_data["nodes"].append(node_data)
            
            # Serialize edges
            for edge_id, edge in graph.edges.items():
                edge_data = {
                    "id": edge_id,
                    "source": edge.source,
                    "target": edge.target,
                    "relationship": edge.relationship,
                    "properties": edge.properties,
                    "confidence": edge.confidence
                }
                graph_data["edges"].append(edge_data)
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(graph_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Graph saved to {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error saving graph to JSON: {e}")
            raise
    
    def load_graph_from_json(self, filepath: str) -> KnowledgeGraph:
        """Load knowledge graph from JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                graph_data = json.load(f)
            
            # Create new graph without initializing domain knowledge
            graph = KnowledgeGraph()
            # Clear the automatically added domain knowledge
            graph.nodes.clear()
            graph.edges.clear()
            graph.graph.clear()
            
            # Load nodes
            for node_data in graph_data.get("nodes", []):
                node = GraphNode(
                    id=node_data["id"],
                    label=node_data["label"],
                    node_type=node_data["node_type"],
                    properties=node_data.get("properties", {}),
                    confidence=node_data.get("confidence", 1.0)
                )
                graph.nodes[node.id] = node
                graph.graph.add_node(node.id, **node.properties)
            
            # Load edges
            for edge_data in graph_data.get("edges", []):
                edge = GraphEdge(
                    source=edge_data["source"],
                    target=edge_data["target"],
                    relationship=edge_data["relationship"],
                    properties=edge_data.get("properties", {}),
                    confidence=edge_data.get("confidence", 1.0)
                )
                edge_id = f"{edge.source}->{edge.target}:{edge.relationship}"
                graph.edges[edge_id] = edge
                graph.graph.add_edge(edge.source, edge.target, 
                                   relationship=edge.relationship, **edge.properties)
            
            self.logger.info(f"Graph loaded from {filepath}")
            return graph
            
        except Exception as e:
            self.logger.error(f"Error loading graph from JSON: {e}")
            raise
    
    def list_saved_graphs(self) -> List[Dict[str, Any]]:
        """List all saved graph files with metadata."""
        graphs = []
        
        for filepath in self.storage_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    graph_data = json.load(f)
                
                graphs.append({
                    "filename": filepath.name,
                    "filepath": str(filepath),
                    "created_at": graph_data.get("metadata", {}).get("created_at"),
                    "node_count": graph_data.get("metadata", {}).get("node_count", 0),
                    "edge_count": graph_data.get("metadata", {}).get("edge_count", 0),
                    "size_bytes": filepath.stat().st_size
                })
            except Exception as e:
                self.logger.warning(f"Error reading graph file {filepath}: {e}")
        
        return sorted(graphs, key=lambda x: x["created_at"] or "", reverse=True)
    
    def delete_graph(self, filename: str) -> bool:
        """Delete a saved graph file."""
        try:
            filepath = self.storage_dir / filename
            if filepath.exists():
                filepath.unlink()
                self.logger.info(f"Graph file deleted: {filename}")
                return True
            else:
                self.logger.warning(f"Graph file not found: {filename}")
                return False
        except Exception as e:
            self.logger.error(f"Error deleting graph file {filename}: {e}")
            return False


class Neo4jPersistenceManager:
    """Manages persistence operations for Neo4j database."""
    
    def __init__(self, uri: str, username: str, password: str):
        if not NEO4J_AVAILABLE:
            raise ImportError("Neo4j driver not available. Install with: pip install neo4j")
        
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.logger = logging.getLogger(__name__)
    
    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()
    
    def save_graph_to_neo4j(self, graph: KnowledgeGraph, graph_name: str = "xreason_knowledge_graph") -> bool:
        """Save knowledge graph to Neo4j database."""
        try:
            with self.driver.session() as session:
                # Clear existing graph with same name
                session.run("MATCH (n) WHERE n.graph_name = $name DETACH DELETE n", name=graph_name)
                
                # Create nodes
                for node_id, node in graph.nodes.items():
                    session.run("""
                        CREATE (n:KnowledgeNode {
                            id: $id,
                            label: $label,
                            node_type: $node_type,
                            confidence: $confidence,
                            graph_name: $graph_name
                        })
                    """, id=node_id, label=node.label, node_type=node.node_type,
                         confidence=node.confidence, graph_name=graph_name)
                
                # Create relationships
                for edge_id, edge in graph.edges.items():
                    session.run("""
                        MATCH (source:KnowledgeNode {id: $source_id, graph_name: $graph_name})
                        MATCH (target:KnowledgeNode {id: $target_id, graph_name: $graph_name})
                        CREATE (source)-[r:RELATES_TO {
                            relationship: $relationship,
                            confidence: $confidence,
                            graph_name: $graph_name
                        }]->(target)
                    """, source_id=edge.source, target_id=edge.target,
                         relationship=edge.relationship, confidence=edge.confidence,
                         graph_name=graph_name)
                
                self.logger.info(f"Graph saved to Neo4j with name: {graph_name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving graph to Neo4j: {e}")
            return False
    
    def load_graph_from_neo4j(self, graph_name: str = "xreason_knowledge_graph") -> KnowledgeGraph:
        """Load knowledge graph from Neo4j database."""
        try:
            graph = KnowledgeGraph()
            
            with self.driver.session() as session:
                # Load nodes
                result = session.run("""
                    MATCH (n:KnowledgeNode {graph_name: $graph_name})
                    RETURN n.id as id, n.label as label, n.node_type as node_type,
                           n.confidence as confidence
                """, graph_name=graph_name)
                
                for record in result:
                    node = GraphNode(
                        id=record["id"],
                        label=record["label"],
                        node_type=record["node_type"],
                        confidence=record["confidence"]
                    )
                    graph.nodes[node.id] = node
                    graph.graph.add_node(node.id)
                
                # Load relationships
                result = session.run("""
                    MATCH (source:KnowledgeNode {graph_name: $graph_name})-[r:RELATES_TO {graph_name: $graph_name}]->(target:KnowledgeNode {graph_name: $graph_name})
                    RETURN source.id as source_id, target.id as target_id,
                           r.relationship as relationship, r.confidence as confidence
                """, graph_name=graph_name)
                
                for record in result:
                    edge = GraphEdge(
                        source=record["source_id"],
                        target=record["target_id"],
                        relationship=record["relationship"],
                        confidence=record["confidence"]
                    )
                    edge_id = f"{edge.source}->{edge.target}:{edge.relationship}"
                    graph.edges[edge_id] = edge
                    graph.graph.add_edge(edge.source, edge.target, 
                                       relationship=edge.relationship)
                
                self.logger.info(f"Graph loaded from Neo4j with name: {graph_name}")
                return graph
                
        except Exception as e:
            self.logger.error(f"Error loading graph from Neo4j: {e}")
            raise
    
    def list_graphs_in_neo4j(self) -> List[Dict[str, Any]]:
        """List all graphs stored in Neo4j."""
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (n:KnowledgeNode)
                    RETURN DISTINCT n.graph_name as graph_name,
                           count(n) as node_count
                """)
                
                graphs = []
                for record in result:
                    graph_name = record["graph_name"]
                    
                    # Get edge count for this graph
                    edge_result = session.run("""
                        MATCH ()-[r:RELATES_TO {graph_name: $graph_name}]->()
                        RETURN count(r) as edge_count
                    """, graph_name=graph_name)
                    
                    edge_count = edge_result.single()["edge_count"]
                    
                    graphs.append({
                        "graph_name": graph_name,
                        "node_count": record["node_count"],
                        "edge_count": edge_count
                    })
                
                return graphs
                
        except Exception as e:
            self.logger.error(f"Error listing graphs in Neo4j: {e}")
            return []
    
    def delete_graph_from_neo4j(self, graph_name: str) -> bool:
        """Delete a graph from Neo4j database."""
        try:
            with self.driver.session() as session:
                session.run("""
                    MATCH (n:KnowledgeNode {graph_name: $graph_name})
                    DETACH DELETE n
                """, graph_name=graph_name)
                
                session.run("""
                    MATCH ()-[r:RELATES_TO {graph_name: $graph_name}]->()
                    DELETE r
                """, graph_name=graph_name)
                
                self.logger.info(f"Graph deleted from Neo4j: {graph_name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error deleting graph from Neo4j: {e}")
            return False
    
    def query_neo4j_graph(self, cypher_query: str, graph_name: str = "xreason_knowledge_graph") -> List[Dict[str, Any]]:
        """Execute a Cypher query on the Neo4j graph."""
        try:
            with self.driver.session() as session:
                result = session.run(cypher_query, graph_name=graph_name)
                return [dict(record) for record in result]
                
        except Exception as e:
            self.logger.error(f"Error executing Cypher query: {e}")
            return []


class GraphPersistenceService:
    """High-level service for graph persistence operations."""
    
    def __init__(self, json_storage_dir: str = "./data/graphs", 
                 neo4j_uri: str = None, neo4j_username: str = None, neo4j_password: str = None):
        self.json_manager = GraphPersistenceManager(json_storage_dir)
        self.neo4j_manager = None
        
        if neo4j_uri and neo4j_username and neo4j_password:
            try:
                self.neo4j_manager = Neo4jPersistenceManager(neo4j_uri, neo4j_username, neo4j_password)
                self.logger.info("Neo4j persistence manager initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Neo4j: {e}")
        
        self.logger = logging.getLogger(__name__)
    
    def save_graph(self, graph: KnowledgeGraph, filename: str = None, 
                  save_to_neo4j: bool = False, neo4j_graph_name: str = "xreason_knowledge_graph") -> Dict[str, str]:
        """Save graph to both JSON and optionally Neo4j."""
        results = {}
        
        # Save to JSON
        try:
            json_path = self.json_manager.save_graph_to_json(graph, filename)
            results["json"] = json_path
        except Exception as e:
            self.logger.error(f"Failed to save to JSON: {e}")
            results["json"] = f"Error: {str(e)}"
        
        # Save to Neo4j if available
        if save_to_neo4j and self.neo4j_manager:
            try:
                success = self.neo4j_manager.save_graph_to_neo4j(graph, neo4j_graph_name)
                results["neo4j"] = "Success" if success else "Failed"
            except Exception as e:
                self.logger.error(f"Failed to save to Neo4j: {e}")
                results["neo4j"] = f"Error: {str(e)}"
        
        return results
    
    def load_graph(self, source: str = "json", filepath: str = None, 
                  neo4j_graph_name: str = "xreason_knowledge_graph") -> KnowledgeGraph:
        """Load graph from JSON or Neo4j."""
        if source.lower() == "json":
            if not filepath:
                # Load the most recent graph
                graphs = self.json_manager.list_saved_graphs()
                if not graphs:
                    raise ValueError("No saved graphs found")
                filepath = graphs[0]["filepath"]
            
            return self.json_manager.load_graph_from_json(filepath)
        
        elif source.lower() == "neo4j":
            if not self.neo4j_manager:
                raise ValueError("Neo4j manager not available")
            
            return self.neo4j_manager.load_graph_from_neo4j(neo4j_graph_name)
        
        else:
            raise ValueError("Source must be 'json' or 'neo4j'")
    
    def list_available_graphs(self) -> Dict[str, List[Dict[str, Any]]]:
        """List available graphs from both sources."""
        results = {"json": [], "neo4j": []}
        
        # List JSON graphs
        try:
            results["json"] = self.json_manager.list_saved_graphs()
        except Exception as e:
            self.logger.error(f"Error listing JSON graphs: {e}")
        
        # List Neo4j graphs
        if self.neo4j_manager:
            try:
                results["neo4j"] = self.neo4j_manager.list_graphs_in_neo4j()
            except Exception as e:
                self.logger.error(f"Error listing Neo4j graphs: {e}")
        
        return results
    
    def delete_graph(self, source: str, identifier: str) -> bool:
        """Delete a graph from the specified source."""
        if source.lower() == "json":
            return self.json_manager.delete_graph(identifier)
        
        elif source.lower() == "neo4j":
            if not self.neo4j_manager:
                return False
            return self.neo4j_manager.delete_graph_from_neo4j(identifier)
        
        else:
            raise ValueError("Source must be 'json' or 'neo4j'")
    
    def close(self):
        """Close any open connections."""
        if self.neo4j_manager:
            self.neo4j_manager.close()


# Factory function for easy initialization
def create_persistence_service(json_storage_dir: str = "./data/graphs",
                             neo4j_uri: str = None, neo4j_username: str = None, 
                             neo4j_password: str = None) -> GraphPersistenceService:
    """Create a graph persistence service with the specified configuration."""
    return GraphPersistenceService(json_storage_dir, neo4j_uri, neo4j_username, neo4j_password)


class GraphPersistenceService:
    """High-level service for graph persistence operations."""
    
    def __init__(self, json_storage_dir: str = "./data/graphs", 
                 neo4j_uri: str = None, neo4j_username: str = None, neo4j_password: str = None):
        self.json_manager = GraphPersistenceManager(json_storage_dir)
        self.neo4j_manager = None
        
        if neo4j_uri and neo4j_username and neo4j_password:
            try:
                self.neo4j_manager = Neo4jPersistenceManager(neo4j_uri, neo4j_username, neo4j_password)
                self.logger.info("Neo4j persistence manager initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Neo4j: {e}")
        
        self.logger = logging.getLogger(__name__)
    
    def save_graph(self, graph: KnowledgeGraph, filename: str = None, 
                  save_to_neo4j: bool = False, neo4j_graph_name: str = "xreason_knowledge_graph") -> Dict[str, str]:
        """Save graph to both JSON and optionally Neo4j."""
        results = {}
        
        # Save to JSON
        try:
            json_path = self.json_manager.save_graph_to_json(graph, filename)
            results["json"] = json_path
        except Exception as e:
            self.logger.error(f"Failed to save to JSON: {e}")
            results["json"] = f"Error: {str(e)}"
        
        # Save to Neo4j if available
        if save_to_neo4j and self.neo4j_manager:
            try:
                success = self.neo4j_manager.save_graph_to_neo4j(graph, neo4j_graph_name)
                results["neo4j"] = "Success" if success else "Failed"
            except Exception as e:
                self.logger.error(f"Failed to save to Neo4j: {e}")
                results["neo4j"] = f"Error: {str(e)}"
        
        return results
    
    def load_graph(self, source: str = "json", filepath: str = None, 
                  neo4j_graph_name: str = "xreason_knowledge_graph") -> KnowledgeGraph:
        """Load graph from JSON or Neo4j."""
        if source.lower() == "json":
            if not filepath:
                # Load the most recent graph
                graphs = self.json_manager.list_saved_graphs()
                if not graphs:
                    raise ValueError("No saved graphs found")
                filepath = graphs[0]["filepath"]
            
            return self.json_manager.load_graph_from_json(filepath)
        
        elif source.lower() == "neo4j":
            if not self.neo4j_manager:
                raise ValueError("Neo4j manager not available")
            
            return self.neo4j_manager.load_graph_from_neo4j(neo4j_graph_name)
        
        else:
            raise ValueError("Source must be 'json' or 'neo4j'")
    
    def list_available_graphs(self) -> Dict[str, List[Dict[str, Any]]]:
        """List available graphs from both sources."""
        results = {"json": [], "neo4j": []}
        
        # List JSON graphs
        try:
            results["json"] = self.json_manager.list_saved_graphs()
        except Exception as e:
            self.logger.error(f"Error listing JSON graphs: {e}")
        
        # List Neo4j graphs
        if self.neo4j_manager:
            try:
                results["neo4j"] = self.neo4j_manager.list_graphs_in_neo4j()
            except Exception as e:
                self.logger.error(f"Error listing Neo4j graphs: {e}")
        
        return results
    
    def delete_graph(self, source: str, identifier: str) -> bool:
        """Delete a graph from the specified source."""
        if source.lower() == "json":
            return self.json_manager.delete_graph(identifier)
        
        elif source.lower() == "neo4j":
            if not self.neo4j_manager:
                return False
            return self.neo4j_manager.delete_graph_from_neo4j(identifier)
        
        else:
            raise ValueError("Source must be 'json' or 'neo4j'")
    
    def close(self):
        """Close any open connections."""
        if self.neo4j_manager:
            self.neo4j_manager.close()


# Factory functions for easy initialization
def create_persistence_manager(storage_dir: str = "./data/graphs") -> GraphPersistenceManager:
    """Create a graph persistence manager."""
    return GraphPersistenceManager(storage_dir)


def create_persistence_service(json_storage_dir: str = "./data/graphs",
                             neo4j_uri: str = None, neo4j_username: str = None, 
                             neo4j_password: str = None) -> GraphPersistenceService:
    """Create a graph persistence service with the specified configuration."""
    return GraphPersistenceService(json_storage_dir, neo4j_uri, neo4j_username, neo4j_password)
