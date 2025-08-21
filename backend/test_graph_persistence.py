#!/usr/bin/env python3
"""
Test Graph Persistence Functionality
Demonstrates saving and loading knowledge graphs.
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Set environment variables for testing
os.environ["OPENAI_API_KEY"] = "sk-demo-key-for-testing"
os.environ["SECRET_KEY"] = "dev-secret-key-for-testing-only"

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.modern_reasoning_service import ModernReasoningService, KnowledgeGraph, GraphNode, GraphEdge
from app.services.llm_service import LLMService
from app.services.graph_persistence import create_persistence_manager


class GraphPersistenceTester:
    def __init__(self):
        self.llm_service = LLMService()
        self.reasoning_service = ModernReasoningService(self.llm_service)
        self.persistence_manager = create_persistence_manager("./test_data/graphs")
        self.test_results = []
    
    def add_result(self, test_name: str, passed: bool, details: str = ""):
        self.test_results.append({
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_create_custom_graph(self):
        """Test creating a custom knowledge graph."""
        try:
            # Create a custom graph
            custom_graph = KnowledgeGraph()
            
            # Add healthcare nodes
            hipaa = GraphNode(label="HIPAA", node_type="regulation")
            access_control = GraphNode(label="Access Control", node_type="requirement")
            authentication = GraphNode(label="Authentication", node_type="requirement")
            encryption = GraphNode(label="Encryption", node_type="requirement")
            phi = GraphNode(label="Protected Health Information", node_type="concept")
            
            custom_graph.add_node(hipaa)
            custom_graph.add_node(access_control)
            custom_graph.add_node(authentication)
            custom_graph.add_node(encryption)
            custom_graph.add_node(phi)
            
            # Add relationships
            custom_graph.add_edge(GraphEdge(
                source=hipaa.id,
                target=access_control.id,
                relationship="requires"
            ))
            
            custom_graph.add_edge(GraphEdge(
                source=hipaa.id,
                target=authentication.id,
                relationship="requires"
            ))
            
            custom_graph.add_edge(GraphEdge(
                source=hipaa.id,
                target=encryption.id,
                relationship="requires"
            ))
            
            custom_graph.add_edge(GraphEdge(
                source=access_control.id,
                target=phi.id,
                relationship="protects"
            ))
            
            # Add financial nodes
            financial = GraphNode(label="Financial Compliance", node_type="regulation")
            sox = GraphNode(label="SOX", node_type="regulation")
            audit = GraphNode(label="Audit Trail", node_type="requirement")
            
            custom_graph.add_node(financial)
            custom_graph.add_node(sox)
            custom_graph.add_node(audit)
            
            custom_graph.add_edge(GraphEdge(
                source=financial.id,
                target=audit.id,
                relationship="requires"
            ))
            
            custom_graph.add_edge(GraphEdge(
                source=sox.id,
                target=audit.id,
                relationship="requires"
            ))
            
            self.custom_graph = custom_graph
            self.add_result("Create Custom Graph", True, f"Created graph with {len(custom_graph.nodes)} nodes and {len(custom_graph.edges)} edges")
            return True
            
        except Exception as e:
            self.add_result("Create Custom Graph", False, str(e))
            return False
    
    def test_save_graph_to_json(self):
        """Test saving graph to JSON."""
        try:
            if not hasattr(self, 'custom_graph'):
                self.add_result("Save Graph to JSON", False, "No custom graph available")
                return False
            
            # Save graph
            filepath = self.persistence_manager.save_graph_to_json(
                self.custom_graph, 
                "test_custom_graph.json"
            )
            
            self.saved_filepath = filepath
            self.add_result("Save Graph to JSON", True, f"Saved to {filepath}")
            return True
            
        except Exception as e:
            self.add_result("Save Graph to JSON", False, str(e))
            return False
    
    def test_load_graph_from_json(self):
        """Test loading graph from JSON."""
        try:
            if not hasattr(self, 'saved_filepath'):
                self.add_result("Load Graph from JSON", False, "No saved file available")
                return False
            
            # Load graph
            loaded_graph = self.persistence_manager.load_graph_from_json(self.saved_filepath)
            
            # Verify graph structure
            assert len(loaded_graph.nodes) == len(self.custom_graph.nodes), "Node count mismatch"
            assert len(loaded_graph.edges) == len(self.custom_graph.edges), "Edge count mismatch"
            
            # Verify some key nodes exist
            hipaa_found = any(node.label == "HIPAA" for node in loaded_graph.nodes.values())
            financial_found = any(node.label == "Financial Compliance" for node in loaded_graph.nodes.values())
            
            assert hipaa_found, "HIPAA node not found in loaded graph"
            assert financial_found, "Financial Compliance node not found in loaded graph"
            
            self.loaded_graph = loaded_graph
            self.add_result("Load Graph from JSON", True, f"Loaded graph with {len(loaded_graph.nodes)} nodes")
            return True
            
        except Exception as e:
            self.add_result("Load Graph from JSON", False, str(e))
            return False
    
    def test_graph_operations_after_load(self):
        """Test that loaded graph operations work correctly."""
        try:
            if not hasattr(self, 'loaded_graph'):
                self.add_result("Graph Operations After Load", False, "No loaded graph available")
                return False
            
            # Test query operations
            hipaa_results = self.loaded_graph.query("HIPAA")
            assert len(hipaa_results) > 0, "No relationships found for HIPAA"
            
            # Test path finding
            paths = self.loaded_graph.find_path("HIPAA", "Protected Health Information")
            assert len(paths) > 0, "No path found from HIPAA to PHI"
            
            # Test related concepts
            related = self.loaded_graph.get_related_concepts("HIPAA")
            assert len(related) > 0, "No related concepts found for HIPAA"
            
            self.add_result("Graph Operations After Load", True, f"Found {len(hipaa_results)} relationships, {len(paths)} paths")
            return True
            
        except Exception as e:
            self.add_result("Graph Operations After Load", False, str(e))
            return False
    
    def test_list_saved_graphs(self):
        """Test listing saved graphs."""
        try:
            graphs = self.persistence_manager.list_saved_graphs()
            
            # Should have at least our test graph
            assert len(graphs) > 0, "No saved graphs found"
            
            # Find our test graph
            test_graph = next((g for g in graphs if "test_custom_graph" in g["filename"]), None)
            assert test_graph is not None, "Test graph not found in list"
            
            self.add_result("List Saved Graphs", True, f"Found {len(graphs)} saved graphs")
            return True
            
        except Exception as e:
            self.add_result("List Saved Graphs", False, str(e))
            return False
    
    def test_graph_metadata(self):
        """Test graph metadata and statistics."""
        try:
            if not hasattr(self, 'loaded_graph'):
                self.add_result("Graph Metadata", False, "No loaded graph available")
                return False
            
            # Analyze graph structure
            node_types = {}
            relationship_types = {}
            
            for node in self.loaded_graph.nodes.values():
                node_types[node.node_type] = node_types.get(node.node_type, 0) + 1
            
            for edge in self.loaded_graph.edges.values():
                relationship_types[edge.relationship] = relationship_types.get(edge.relationship, 0) + 1
            
            # Print statistics
            print(f"\n📊 Graph Statistics:")
            print(f"   Total Nodes: {len(self.loaded_graph.nodes)}")
            print(f"   Total Edges: {len(self.loaded_graph.edges)}")
            print(f"   Node Types: {node_types}")
            print(f"   Relationship Types: {relationship_types}")
            
            self.add_result("Graph Metadata", True, f"Analyzed graph with {len(node_types)} node types, {len(relationship_types)} relationship types")
            return True
            
        except Exception as e:
            self.add_result("Graph Metadata", False, str(e))
            return False
    
    def test_cleanup(self):
        """Clean up test files."""
        try:
            if hasattr(self, 'saved_filepath'):
                import os
                if os.path.exists(self.saved_filepath):
                    os.remove(self.saved_filepath)
                    print(f"   Cleaned up: {self.saved_filepath}")
            
            self.add_result("Cleanup", True, "Test files cleaned up")
            return True
            
        except Exception as e:
            self.add_result("Cleanup", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run all persistence tests."""
        print("🚀 Testing Graph Persistence Functionality")
        print("=" * 60)
        
        test_methods = [
            self.test_create_custom_graph,
            self.test_save_graph_to_json,
            self.test_load_graph_from_json,
            self.test_graph_operations_after_load,
            self.test_list_saved_graphs,
            self.test_graph_metadata,
            self.test_cleanup
        ]
        
        for test_method in test_methods:
            test_method()
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["passed"])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "=" * 60)
        print("📊 PERSISTENCE TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 ALL PERSISTENCE TESTS PASSED!")
            print("✅ Graph persistence is working correctly.")
            print("✅ JSON save/load functionality is robust.")
            print("✅ Graph operations work after persistence.")
        else:
            print(f"\n⚠️  {failed_tests} tests failed. Review issues.")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": passed_tests / total_tests,
            "results": self.test_results
        }


def main():
    """Main test runner."""
    tester = GraphPersistenceTester()
    summary = tester.run_all_tests()
    
    # Exit with appropriate code
    if summary["failed_tests"] == 0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
