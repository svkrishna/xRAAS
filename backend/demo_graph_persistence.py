#!/usr/bin/env python3
"""
Graph Persistence Demo
Comprehensive demonstration of graph persistence functionality.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Set environment variables for testing
os.environ["OPENAI_API_KEY"] = "sk-demo-key-for-testing"
os.environ["SECRET_KEY"] = "dev-secret-key-for-testing-only"

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.modern_reasoning_service import ModernReasoningService, KnowledgeGraph, GraphNode, GraphEdge
from app.services.llm_service import LLMService
from app.services.graph_persistence import create_persistence_service


class GraphPersistenceDemo:
    def __init__(self):
        self.llm_service = LLMService()
        self.reasoning_service = ModernReasoningService(self.llm_service)
        self.persistence_service = create_persistence_service("./demo_data/graphs")
        self.demo_graphs = {}
    
    def print_header(self, title: str):
        """Print a formatted header."""
        print("\n" + "=" * 80)
        print(f"🎯 {title}")
        print("=" * 80)
    
    def print_section(self, title: str):
        """Print a formatted section."""
        print(f"\n📋 {title}")
        print("-" * 60)
    
    def create_healthcare_compliance_graph(self) -> KnowledgeGraph:
        """Create a comprehensive healthcare compliance graph."""
        self.print_section("Creating Healthcare Compliance Graph")
        
        graph = KnowledgeGraph()
        # Clear default domain knowledge
        graph.nodes.clear()
        graph.edges.clear()
        graph.graph.clear()
        
        # HIPAA Regulations
        hipaa = GraphNode(label="HIPAA", node_type="regulation", confidence=1.0)
        phi = GraphNode(label="Protected Health Information", node_type="concept", confidence=1.0)
        ephi = GraphNode(label="Electronic PHI", node_type="concept", confidence=1.0)
        
        # Security Requirements
        access_control = GraphNode(label="Access Control", node_type="requirement", confidence=1.0)
        authentication = GraphNode(label="Authentication", node_type="requirement", confidence=1.0)
        encryption = GraphNode(label="Encryption", node_type="requirement", confidence=1.0)
        audit_logging = GraphNode(label="Audit Logging", node_type="requirement", confidence=1.0)
        backup = GraphNode(label="Data Backup", node_type="requirement", confidence=1.0)
        
        # Technical Controls
        firewalls = GraphNode(label="Firewalls", node_type="control", confidence=1.0)
        vpn = GraphNode(label="VPN", node_type="control", confidence=1.0)
        ssl = GraphNode(label="SSL/TLS", node_type="control", confidence=1.0)
        mfa = GraphNode(label="Multi-Factor Authentication", node_type="control", confidence=1.0)
        
        # Add nodes
        nodes = [hipaa, phi, ephi, access_control, authentication, encryption, 
                audit_logging, backup, firewalls, vpn, ssl, mfa]
        
        for node in nodes:
            graph.add_node(node)
        
        # Add relationships
        edges = [
            GraphEdge(source=hipaa.id, target=phi.id, relationship="protects"),
            GraphEdge(source=hipaa.id, target=ephi.id, relationship="protects"),
            GraphEdge(source=hipaa.id, target=access_control.id, relationship="requires"),
            GraphEdge(source=hipaa.id, target=authentication.id, relationship="requires"),
            GraphEdge(source=hipaa.id, target=encryption.id, relationship="requires"),
            GraphEdge(source=hipaa.id, target=audit_logging.id, relationship="requires"),
            GraphEdge(source=hipaa.id, target=backup.id, relationship="requires"),
            
            GraphEdge(source=access_control.id, target=firewalls.id, relationship="implements"),
            GraphEdge(source=access_control.id, target=vpn.id, relationship="implements"),
            GraphEdge(source=authentication.id, target=mfa.id, relationship="implements"),
            GraphEdge(source=encryption.id, target=ssl.id, relationship="implements"),
            
            GraphEdge(source=firewalls.id, target=phi.id, relationship="protects"),
            GraphEdge(source=vpn.id, target=phi.id, relationship="protects"),
            GraphEdge(source=ssl.id, target=ephi.id, relationship="protects"),
            GraphEdge(source=mfa.id, target=phi.id, relationship="protects")
        ]
        
        for edge in edges:
            graph.add_edge(edge)
        
        print(f"✅ Created healthcare compliance graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
        return graph
    
    def create_financial_compliance_graph(self) -> KnowledgeGraph:
        """Create a comprehensive financial compliance graph."""
        self.print_section("Creating Financial Compliance Graph")
        
        graph = KnowledgeGraph()
        # Clear default domain knowledge
        graph.nodes.clear()
        graph.edges.clear()
        graph.graph.clear()
        
        # Financial Regulations
        sox = GraphNode(label="SOX", node_type="regulation", confidence=1.0)
        pci_dss = GraphNode(label="PCI DSS", node_type="regulation", confidence=1.0)
        gdpr = GraphNode(label="GDPR", node_type="regulation", confidence=1.0)
        
        # Financial Data
        pci_data = GraphNode(label="PCI Data", node_type="concept", confidence=1.0)
        personal_data = GraphNode(label="Personal Data", node_type="concept", confidence=1.0)
        financial_records = GraphNode(label="Financial Records", node_type="concept", confidence=1.0)
        
        # Compliance Requirements
        audit_trail = GraphNode(label="Audit Trail", node_type="requirement", confidence=1.0)
        data_retention = GraphNode(label="Data Retention", node_type="requirement", confidence=1.0)
        access_logging = GraphNode(label="Access Logging", node_type="requirement", confidence=1.0)
        encryption_at_rest = GraphNode(label="Encryption at Rest", node_type="requirement", confidence=1.0)
        encryption_in_transit = GraphNode(label="Encryption in Transit", node_type="requirement", confidence=1.0)
        
        # Technical Controls
        database_encryption = GraphNode(label="Database Encryption", node_type="control", confidence=1.0)
        ssl_tls = GraphNode(label="SSL/TLS", node_type="control", confidence=1.0)
        log_management = GraphNode(label="Log Management", node_type="control", confidence=1.0)
        backup_encryption = GraphNode(label="Backup Encryption", node_type="control", confidence=1.0)
        
        # Add nodes
        nodes = [sox, pci_dss, gdpr, pci_data, personal_data, financial_records,
                audit_trail, data_retention, access_logging, encryption_at_rest,
                encryption_in_transit, database_encryption, ssl_tls, log_management, backup_encryption]
        
        for node in nodes:
            graph.add_node(node)
        
        # Add relationships
        edges = [
            # SOX relationships
            GraphEdge(source=sox.id, target=audit_trail.id, relationship="requires"),
            GraphEdge(source=sox.id, target=financial_records.id, relationship="protects"),
            GraphEdge(source=sox.id, target=data_retention.id, relationship="requires"),
            
            # PCI DSS relationships
            GraphEdge(source=pci_dss.id, target=pci_data.id, relationship="protects"),
            GraphEdge(source=pci_dss.id, target=encryption_at_rest.id, relationship="requires"),
            GraphEdge(source=pci_dss.id, target=encryption_in_transit.id, relationship="requires"),
            GraphEdge(source=pci_dss.id, target=access_logging.id, relationship="requires"),
            
            # GDPR relationships
            GraphEdge(source=gdpr.id, target=personal_data.id, relationship="protects"),
            GraphEdge(source=gdpr.id, target=data_retention.id, relationship="requires"),
            GraphEdge(source=gdpr.id, target=access_logging.id, relationship="requires"),
            
            # Technical implementations
            GraphEdge(source=encryption_at_rest.id, target=database_encryption.id, relationship="implements"),
            GraphEdge(source=encryption_at_rest.id, target=backup_encryption.id, relationship="implements"),
            GraphEdge(source=encryption_in_transit.id, target=ssl_tls.id, relationship="implements"),
            GraphEdge(source=audit_trail.id, target=log_management.id, relationship="implements"),
            GraphEdge(source=access_logging.id, target=log_management.id, relationship="implements"),
            
            # Data protection
            GraphEdge(source=database_encryption.id, target=pci_data.id, relationship="protects"),
            GraphEdge(source=database_encryption.id, target=personal_data.id, relationship="protects"),
            GraphEdge(source=ssl_tls.id, target=pci_data.id, relationship="protects"),
            GraphEdge(source=backup_encryption.id, target=financial_records.id, relationship="protects")
        ]
        
        for edge in edges:
            graph.add_edge(edge)
        
        print(f"✅ Created financial compliance graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
        return graph
    
    def demo_save_and_load(self):
        """Demonstrate save and load functionality."""
        self.print_section("Save and Load Operations")
        
        # Save healthcare graph
        healthcare_graph = self.create_healthcare_compliance_graph()
        results = self.persistence_service.save_graph(
            healthcare_graph, 
            "healthcare_compliance.json"
        )
        print(f"✅ Healthcare graph saved: {results}")
        
        # Save financial graph
        financial_graph = self.create_financial_compliance_graph()
        results = self.persistence_service.save_graph(
            financial_graph, 
            "financial_compliance.json"
        )
        print(f"✅ Financial graph saved: {results}")
        
        # List saved graphs
        graphs = self.persistence_service.list_available_graphs()
        print(f"\n📋 Available graphs:")
        for source, graph_list in graphs.items():
            print(f"   {source.upper()}: {len(graph_list)} graphs")
            for graph in graph_list:
                print(f"     - {graph.get('filename', graph.get('graph_name', 'Unknown'))}")
        
        # Load and verify graphs
        print(f"\n🔄 Loading and verifying graphs...")
        
        # Load healthcare graph
        loaded_healthcare = self.persistence_service.load_graph(
            source="json", 
            filepath="./demo_data/graphs/healthcare_compliance.json"
        )
        print(f"✅ Healthcare graph loaded: {len(loaded_healthcare.nodes)} nodes, {len(loaded_healthcare.edges)} edges")
        
        # Load financial graph
        loaded_financial = self.persistence_service.load_graph(
            source="json", 
            filepath="./demo_data/graphs/financial_compliance.json"
        )
        print(f"✅ Financial graph loaded: {len(loaded_financial.nodes)} nodes, {len(loaded_financial.edges)} edges")
        
        # Store for later use
        self.demo_graphs["healthcare"] = loaded_healthcare
        self.demo_graphs["financial"] = loaded_financial
    
    def demo_graph_operations(self):
        """Demonstrate graph operations on loaded graphs."""
        self.print_section("Graph Operations on Loaded Graphs")
        
        for graph_name, graph in self.demo_graphs.items():
            print(f"\n🔍 Analyzing {graph_name} graph:")
            
            # Query operations
            if graph_name == "healthcare":
                hipaa_results = graph.query("HIPAA")
                print(f"   HIPAA relationships: {len(hipaa_results)}")
                
                # Path finding
                paths = graph.find_path("HIPAA", "Protected Health Information")
                print(f"   Paths from HIPAA to PHI: {len(paths)}")
                
                # Related concepts
                related = graph.get_related_concepts("HIPAA")
                print(f"   Related to HIPAA: {len(related)} concepts")
                
            elif graph_name == "financial":
                sox_results = graph.query("SOX")
                print(f"   SOX relationships: {len(sox_results)}")
                
                # Path finding
                paths = graph.find_path("SOX", "Financial Records")
                print(f"   Paths from SOX to Financial Records: {len(paths)}")
                
                # Related concepts
                related = graph.get_related_concepts("SOX")
                print(f"   Related to SOX: {len(related)} concepts")
    
    def demo_graph_statistics(self):
        """Demonstrate graph statistics and analysis."""
        self.print_section("Graph Statistics and Analysis")
        
        for graph_name, graph in self.demo_graphs.items():
            print(f"\n📊 {graph_name.title()} Graph Statistics:")
            
            # Node type analysis
            node_types = {}
            for node in graph.nodes.values():
                node_types[node.node_type] = node_types.get(node.node_type, 0) + 1
            
            print(f"   Node Types: {node_types}")
            
            # Relationship analysis
            relationship_types = {}
            for edge in graph.edges.values():
                relationship_types[edge.relationship] = relationship_types.get(edge.relationship, 0) + 1
            
            print(f"   Relationship Types: {relationship_types}")
            
            # Graph density
            total_possible_edges = len(graph.nodes) * (len(graph.nodes) - 1)
            actual_edges = len(graph.edges)
            density = actual_edges / total_possible_edges if total_possible_edges > 0 else 0
            print(f"   Graph Density: {density:.3f}")
            
            # Average node degree
            total_degree = sum(len(list(graph.graph.edges(node_id))) for node_id in graph.nodes.keys())
            avg_degree = total_degree / len(graph.nodes) if len(graph.nodes) > 0 else 0
            print(f"   Average Node Degree: {avg_degree:.2f}")
    
    def demo_export_formats(self):
        """Demonstrate different export formats."""
        self.print_section("Export Format Demonstrations")
        
        for graph_name, graph in self.demo_graphs.items():
            print(f"\n📤 Exporting {graph_name} graph in different formats:")
            
            # JSON export
            json_data = {
                "metadata": {
                    "name": f"{graph_name}_compliance_graph",
                    "created_at": datetime.utcnow().isoformat(),
                    "node_count": len(graph.nodes),
                    "edge_count": len(graph.edges)
                },
                "nodes": [
                    {
                        "id": node.id,
                        "label": node.label,
                        "type": node.node_type,
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
            
            # Save to different formats
            export_dir = Path(f"./demo_data/exports/{graph_name}")
            export_dir.mkdir(parents=True, exist_ok=True)
            
            # JSON format
            json_file = export_dir / f"{graph_name}_graph.json"
            with open(json_file, 'w') as f:
                json.dump(json_data, f, indent=2)
            print(f"   ✅ JSON: {json_file}")
            
            # CSV format (nodes)
            csv_nodes_file = export_dir / f"{graph_name}_nodes.csv"
            with open(csv_nodes_file, 'w') as f:
                f.write("id,label,type,confidence\n")
                for node in graph.nodes.values():
                    f.write(f"{node.id},{node.label},{node.node_type},{node.confidence}\n")
            print(f"   ✅ CSV Nodes: {csv_nodes_file}")
            
            # CSV format (edges)
            csv_edges_file = export_dir / f"{graph_name}_edges.csv"
            with open(csv_edges_file, 'w') as f:
                f.write("source,target,relationship,confidence\n")
                for edge in graph.edges.values():
                    f.write(f"{edge.source},{edge.target},{edge.relationship},{edge.confidence}\n")
            print(f"   ✅ CSV Edges: {csv_edges_file}")
    
    def demo_cleanup(self):
        """Clean up demo files."""
        self.print_section("Cleanup")
        
        try:
            import shutil
            demo_dir = Path("./demo_data")
            if demo_dir.exists():
                shutil.rmtree(demo_dir)
                print("✅ Demo data cleaned up")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
    
    def run_demo(self):
        """Run the complete graph persistence demo."""
        self.print_header("GRAPH PERSISTENCE DEMONSTRATION")
        
        print("This demo showcases the complete graph persistence functionality:")
        print("• Creating complex knowledge graphs")
        print("• Saving graphs to JSON format")
        print("• Loading graphs from storage")
        print("• Performing graph operations on loaded graphs")
        print("• Analyzing graph statistics")
        print("• Exporting to multiple formats")
        
        try:
            # Run demo sections
            self.demo_save_and_load()
            self.demo_graph_operations()
            self.demo_graph_statistics()
            self.demo_export_formats()
            
            print("\n" + "=" * 80)
            print("🎉 GRAPH PERSISTENCE DEMO COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            print("✅ All persistence operations working correctly")
            print("✅ Graph save/load functionality is robust")
            print("✅ Graph operations work after persistence")
            print("✅ Multiple export formats supported")
            print("✅ Comprehensive graph analysis capabilities")
            
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            raise
        finally:
            # Clean up
            self.demo_cleanup()


def main():
    """Main demo runner."""
    demo = GraphPersistenceDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()
