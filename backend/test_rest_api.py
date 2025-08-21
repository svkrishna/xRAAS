#!/usr/bin/env python3
"""
REST API Test Script for Graph Persistence
Tests all graph persistence endpoints via HTTP requests.
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000/api/v1/graphs"

class GraphPersistenceAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.created_graphs = []
    
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
    
    def wait_for_server(self, max_retries=30):
        """Wait for the server to be ready."""
        print("🔄 Waiting for server to start...")
        for i in range(max_retries):
            try:
                response = self.session.get("http://localhost:8000/health")
                if response.status_code == 200:
                    print("✅ Server is ready!")
                    return True
            except requests.exceptions.ConnectionError:
                pass
            time.sleep(1)
            if i % 5 == 0:
                print(f"   Still waiting... ({i+1}/{max_retries})")
        
        print("❌ Server failed to start")
        return False
    
    def create_test_graph_data(self):
        """Create test graph data for API testing."""
        return {
            "nodes": [
                {
                    "id": "hipaa-001",
                    "label": "HIPAA",
                    "node_type": "regulation",
                    "properties": {"version": "2023", "jurisdiction": "US"},
                    "confidence": 1.0
                },
                {
                    "id": "phi-001",
                    "label": "Protected Health Information",
                    "node_type": "concept",
                    "properties": {"sensitivity": "high"},
                    "confidence": 1.0
                },
                {
                    "id": "encryption-001",
                    "label": "Encryption",
                    "node_type": "requirement",
                    "properties": {"algorithm": "AES-256"},
                    "confidence": 1.0
                },
                {
                    "id": "ssl-001",
                    "label": "SSL/TLS",
                    "node_type": "control",
                    "properties": {"version": "1.3"},
                    "confidence": 1.0
                }
            ],
            "edges": [
                {
                    "source": "hipaa-001",
                    "target": "phi-001",
                    "relationship": "protects",
                    "properties": {"mandatory": True},
                    "confidence": 1.0
                },
                {
                    "source": "hipaa-001",
                    "target": "encryption-001",
                    "relationship": "requires",
                    "properties": {"mandatory": True},
                    "confidence": 1.0
                },
                {
                    "source": "encryption-001",
                    "target": "ssl-001",
                    "relationship": "implements",
                    "properties": {"method": "transport"},
                    "confidence": 1.0
                },
                {
                    "source": "ssl-001",
                    "target": "phi-001",
                    "relationship": "protects",
                    "properties": {"scope": "transit"},
                    "confidence": 1.0
                }
            ]
        }
    
    def test_health_endpoint(self):
        """Test the health endpoint."""
        try:
            response = self.session.get("http://localhost:8000/health")
            if response.status_code == 200:
                self.add_result("Health Endpoint", True, f"Status: {response.status_code}")
                return True
            else:
                self.add_result("Health Endpoint", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.add_result("Health Endpoint", False, str(e))
            return False
    
    def test_save_graph(self):
        """Test saving a graph via REST API."""
        try:
            graph_data = self.create_test_graph_data()
            
            payload = {
                "filename": "test_compliance_graph.json",
                "save_to_neo4j": False,
                "description": "Test compliance graph for API testing"
            }
            
            # Combine payload with graph data
            full_payload = {**payload, "graph_data": graph_data}
            
            response = self.session.post(
                f"{BASE_URL}/save",
                json=full_payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.add_result("Save Graph", True, f"Saved: {result.get('results', {})}")
                    self.created_graphs.append("test_compliance_graph.json")
                    return True
                else:
                    self.add_result("Save Graph", False, f"API returned success=False")
                    return False
            else:
                self.add_result("Save Graph", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.add_result("Save Graph", False, str(e))
            return False
    
    def test_list_graphs(self):
        """Test listing available graphs."""
        try:
            response = self.session.get(f"{BASE_URL}/list")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    graphs = result.get("graphs", {})
                    json_graphs = graphs.get("json", [])
                    neo4j_graphs = graphs.get("neo4j", [])
                    
                    # Check if our test graph is in the list
                    test_graph_found = any(
                        "test_compliance_graph" in g.get("filename", "") 
                        for g in json_graphs
                    )
                    
                    if test_graph_found:
                        self.add_result("List Graphs", True, f"Found {len(json_graphs)} JSON graphs, {len(neo4j_graphs)} Neo4j graphs")
                        return True
                    else:
                        self.add_result("List Graphs", False, "Test graph not found in list")
                        return False
                else:
                    self.add_result("List Graphs", False, "API returned success=False")
                    return False
            else:
                self.add_result("List Graphs", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.add_result("List Graphs", False, str(e))
            return False
    
    def test_load_graph(self):
        """Test loading a graph via REST API."""
        try:
            payload = {
                "source": "json",
                "filepath": "test_compliance_graph.json"
            }
            
            response = self.session.post(
                f"{BASE_URL}/load",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    graph_info = result.get("graph_info", {})
                    node_count = graph_info.get("node_count", 0)
                    edge_count = graph_info.get("edge_count", 0)
                    
                    if node_count == 4 and edge_count == 4:  # Our test graph
                        self.add_result("Load Graph", True, f"Loaded graph with {node_count} nodes, {edge_count} edges")
                        return True
                    else:
                        self.add_result("Load Graph", False, f"Unexpected graph size: {node_count} nodes, {edge_count} edges")
                        return False
                else:
                    self.add_result("Load Graph", False, "API returned success=False")
                    return False
            else:
                self.add_result("Load Graph", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.add_result("Load Graph", False, str(e))
            return False
    
    def test_graph_statistics(self):
        """Test getting graph statistics."""
        try:
            response = self.session.get(f"{BASE_URL}/stats")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    stats = result.get("statistics", {})
                    total_graphs = stats.get("total_graphs", 0)
                    
                    if total_graphs > 0:
                        self.add_result("Graph Statistics", True, f"Found {total_graphs} total graphs")
                        return True
                    else:
                        self.add_result("Graph Statistics", False, "No graphs found in statistics")
                        return False
                else:
                    self.add_result("Graph Statistics", False, "API returned success=False")
                    return False
            else:
                self.add_result("Graph Statistics", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.add_result("Graph Statistics", False, str(e))
            return False
    
    def test_upload_graph_file(self):
        """Test uploading a graph file."""
        try:
            # Create a test graph file
            graph_data = self.create_test_graph_data()
            test_file_content = {
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "version": "1.0",
                    "node_count": len(graph_data["nodes"]),
                    "edge_count": len(graph_data["edges"]),
                    "description": "Uploaded test graph"
                },
                "nodes": graph_data["nodes"],
                "edges": graph_data["edges"]
            }
            
            # Save to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(test_file_content, f)
                temp_file_path = f.name
            
            # Upload the file
            with open(temp_file_path, 'rb') as f:
                files = {'file': ('upload_test_graph.json', f, 'application/json')}
                data = {'description': 'Uploaded via API test'}
                
                response = self.session.post(
                    f"{BASE_URL}/upload",
                    files=files,
                    data=data
                )
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.add_result("Upload Graph File", True, "File uploaded successfully")
                    return True
                else:
                    self.add_result("Upload Graph File", False, "API returned success=False")
                    return False
            else:
                self.add_result("Upload Graph File", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.add_result("Upload Graph File", False, str(e))
            return False
    
    def test_delete_graph(self):
        """Test deleting a graph."""
        try:
            # Delete the test graph we created
            response = self.session.delete(f"{BASE_URL}/json/test_compliance_graph.json")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.add_result("Delete Graph", True, "Graph deleted successfully")
                    return True
                else:
                    self.add_result("Delete Graph", False, "API returned success=False")
                    return False
            else:
                self.add_result("Delete Graph", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.add_result("Delete Graph", False, str(e))
            return False
    
    def test_error_handling(self):
        """Test error handling for invalid requests."""
        try:
            # Test invalid save request (missing graph_data)
            payload = {
                "filename": "invalid_graph.json"
            }
            
            response = self.session.post(
                f"{BASE_URL}/save",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            # Should return an error
            if response.status_code in [400, 422, 500]:
                self.add_result("Error Handling", True, f"Properly handled invalid request: {response.status_code}")
                return True
            else:
                self.add_result("Error Handling", False, f"Expected error but got: {response.status_code}")
                return False
                
        except Exception as e:
            self.add_result("Error Handling", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run all REST API tests."""
        print("🚀 Testing Graph Persistence REST API")
        print("=" * 60)
        
        # Wait for server to start
        if not self.wait_for_server():
            print("❌ Cannot proceed without server")
            return
        
        test_methods = [
            self.test_health_endpoint,
            self.test_save_graph,
            self.test_list_graphs,
            self.test_load_graph,
            self.test_graph_statistics,
            self.test_upload_graph_file,
            self.test_error_handling,
            self.test_delete_graph
        ]
        
        for test_method in test_methods:
            test_method()
            time.sleep(0.5)  # Small delay between tests
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["passed"])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "=" * 60)
        print("📊 REST API TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            print("\n🎉 ALL REST API TESTS PASSED!")
            print("✅ Graph persistence REST API is working correctly.")
            print("✅ All endpoints are functional.")
            print("✅ Error handling is robust.")
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
    tester = GraphPersistenceAPITester()
    summary = tester.run_all_tests()
    
    # Exit with appropriate code
    if summary["failed_tests"] == 0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
