#!/usr/bin/env python3
"""
Test Graph Persistence API Endpoints
Simple test to verify the REST API is working.
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

from app.services.modern_reasoning_service import KnowledgeGraph, GraphNode, GraphEdge
from app.services.graph_persistence import create_persistence_service


class GraphAPITester:
    def __init__(self):
        self.persistence_service = create_persistence_service("./test_api_data/graphs")
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
    
    def test_create_simple_graph(self):
        """Test creating a simple test graph."""
        try:
            # Create a simple graph
            graph = KnowledgeGraph()
            # Clear default domain knowledge
            graph.nodes.clear()
            graph.edges.clear()
            graph.graph.clear()
            
            # Add test nodes
            node1 = GraphNode(label="Test Node 1", node_type="test")
            node2 = GraphNode(label="Test Node 2", node_type="test")
            
            graph.add_node(node1)
            graph.add_node(node2)
            
            # Add test edge
            edge = GraphEdge(
                source=node1.id,
                target=node2.id,
                relationship="connects_to"
            )
            graph.add_edge(edge)
            
            self.test_graph = graph
            self.add_result("Create Simple Graph", True, f"Created graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
            return True
            
        except Exception as e:
            self.add_result("Create Simple Graph", False, str(e))
            return False
    
    def test_save_graph(self):
        """Test saving the graph."""
        try:
            if not hasattr(self, 'test_graph'):
                self.add_result("Save Graph", False, "No test graph available")
                return False
            
            # Save graph
            results = self.persistence_service.save_graph(
                self.test_graph, 
                "api_test_graph.json"
            )
            
            self.add_result("Save Graph", True, f"Saved graph: {results}")
            return True
            
        except Exception as e:
            self.add_result("Save Graph", False, str(e))
            return False
    
    def test_list_graphs(self):
        """Test listing available graphs."""
        try:
            graphs = self.persistence_service.list_available_graphs()
            
            # Should have our test graph
            json_graphs = graphs.get("json", [])
            test_graph_found = any("api_test_graph" in g.get("filename", "") for g in json_graphs)
            
            if test_graph_found:
                self.add_result("List Graphs", True, f"Found {len(json_graphs)} JSON graphs")
                return True
            else:
                self.add_result("List Graphs", False, "Test graph not found in list")
                return False
            
        except Exception as e:
            self.add_result("List Graphs", False, str(e))
            return False
    
    def test_load_graph(self):
        """Test loading the graph."""
        try:
            # Load graph
            loaded_graph = self.persistence_service.load_graph(
                source="json",
                filepath="./test_api_data/graphs/api_test_graph.json"
            )
            
            # Verify structure
            assert len(loaded_graph.nodes) == len(self.test_graph.nodes), "Node count mismatch"
            assert len(loaded_graph.edges) == len(self.test_graph.edges), "Edge count mismatch"
            
            self.add_result("Load Graph", True, f"Loaded graph with {len(loaded_graph.nodes)} nodes")
            return True
            
        except Exception as e:
            self.add_result("Load Graph", False, str(e))
            return False
    
    def test_graph_operations(self):
        """Test graph operations on loaded graph."""
        try:
            # Load graph
            loaded_graph = self.persistence_service.load_graph(
                source="json",
                filepath="./test_api_data/graphs/api_test_graph.json"
            )
            
            # Test query
            results = loaded_graph.query("Test Node 1")
            assert len(results) > 0, "No relationships found"
            
            # Test related concepts
            related = loaded_graph.get_related_concepts("Test Node 1")
            assert len(related) > 0, "No related concepts found"
            
            self.add_result("Graph Operations", True, f"Found {len(results)} relationships and {len(related)} related concepts")
            return True
            
        except Exception as e:
            self.add_result("Graph Operations", False, str(e))
            return False
    
    def test_cleanup(self):
        """Clean up test files."""
        try:
            import os
            test_file = "./test_api_data/graphs/api_test_graph.json"
            if os.path.exists(test_file):
                os.remove(test_file)
                print(f"   Cleaned up: {test_file}")
            
            # Remove test directory if empty
            test_dir = "./test_api_data"
            if os.path.exists(test_dir):
                import shutil
                shutil.rmtree(test_dir)
            
            self.add_result("Cleanup", True, "Test files cleaned up")
            return True
            
        except Exception as e:
            self.add_result("Cleanup", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run all API tests."""
        print("🚀 Testing Graph Persistence API Functionality")
        print("=" * 60)
        
        test_methods = [
            self.test_create_simple_graph,
            self.test_save_graph,
            self.test_list_graphs,
            self.test_load_graph,
            self.test_graph_operations,
            self.test_cleanup
        ]
        
        for test_method in test_methods:
            test_method()
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["passed"])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "=" * 60)
        print("📊 API TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 ALL API TESTS PASSED!")
            print("✅ Graph persistence API is working correctly.")
            print("✅ Save/load operations are functional.")
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
    tester = GraphAPITester()
    summary = tester.run_all_tests()
    
    # Exit with appropriate code
    if summary["failed_tests"] == 0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
