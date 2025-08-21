#!/usr/bin/env python3
"""
Comprehensive Test Suite for XReason Hybrid System
Tests LLM validation, graph reasoning, and integration.
"""

import asyncio
import json
import time
from typing import Dict, Any
import sys
import os

# Set environment variables for testing
os.environ["OPENAI_API_KEY"] = "sk-demo-key-for-testing"
os.environ["SECRET_KEY"] = "dev-secret-key-for-testing-only"

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.modern_reasoning_service import ModernReasoningService, ValidationResult
from app.services.llm_service import LLMService


class TestResult:
    def __init__(self, test_name: str, passed: bool, details: str = "", execution_time: float = 0.0):
        self.test_name = test_name
        self.passed = passed
        self.details = details
        self.execution_time = execution_time


class HybridSystemTester:
    def __init__(self):
        self.llm_service = LLMService()
        self.reasoning_service = ModernReasoningService(self.llm_service)
        self.test_results = []
        
    def add_result(self, result: TestResult):
        self.test_results.append(result)
        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"{status} {result.test_name} ({result.execution_time:.2f}s)")
        if not result.passed and result.details:
            print(f"   Details: {result.details}")
    
    async def test_llm_service_initialization(self) -> TestResult:
        """Test LLM service initialization."""
        start_time = time.time()
        try:
            # Test basic initialization
            assert self.llm_service is not None
            assert hasattr(self.llm_service, 'generate')
            
            execution_time = time.time() - start_time
            return TestResult("LLM Service Initialization", True, "", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("LLM Service Initialization", False, str(e), execution_time)
    
    async def test_reasoning_service_initialization(self) -> TestResult:
        """Test reasoning service initialization."""
        start_time = time.time()
        try:
            assert self.reasoning_service is not None
            assert hasattr(self.reasoning_service, 'reason_about_text')
            assert hasattr(self.reasoning_service, 'validate_compliance')
            assert self.reasoning_service.knowledge_graph is not None
            
            execution_time = time.time() - start_time
            return TestResult("Reasoning Service Initialization", True, "", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("Reasoning Service Initialization", False, str(e), execution_time)
    
    async def test_knowledge_graph_operations(self) -> TestResult:
        """Test knowledge graph operations."""
        start_time = time.time()
        try:
            graph = self.reasoning_service.knowledge_graph
            
            # Test node operations
            assert len(graph.nodes) > 0, "Knowledge graph should have initial nodes"
            
            # Test edge operations
            assert len(graph.edges) > 0, "Knowledge graph should have initial edges"
            
            # Test query operations
            results = graph.query("HIPAA")
            assert isinstance(results, list), "Query should return a list"
            
            # Test path finding
            paths = graph.find_path("HIPAA", "Access Control")
            assert isinstance(paths, list), "Path finding should return a list"
            
            execution_time = time.time() - start_time
            return TestResult("Knowledge Graph Operations", True, "", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("Knowledge Graph Operations", False, str(e), execution_time)
    
    async def test_hipaa_validation(self) -> TestResult:
        """Test HIPAA compliance validation."""
        start_time = time.time()
        try:
            test_text = """
            Our healthcare system implements comprehensive access controls for electronic 
            protected health information (PHI). All users must authenticate using multi-factor 
            authentication before accessing patient data. We use encryption for data transmission 
            and implement audit logs for all access attempts.
            """
            
            result = await self.reasoning_service.llm_validator.validate_hipaa_compliance(test_text)
            
            assert isinstance(result, ValidationResult), "Should return ValidationResult"
            assert hasattr(result, 'is_valid'), "Should have is_valid attribute"
            assert hasattr(result, 'confidence'), "Should have confidence attribute"
            assert hasattr(result, 'reasoning'), "Should have reasoning attribute"
            
            execution_time = time.time() - start_time
            return TestResult("HIPAA Validation", True, f"Confidence: {result.confidence}", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("HIPAA Validation", False, str(e), execution_time)
    
    async def test_financial_validation(self) -> TestResult:
        """Test financial calculation validation."""
        start_time = time.time()
        try:
            test_text = """
            The company has total debt of $500,000 and total equity of $1,000,000. 
            The debt-to-equity ratio is calculated as 0.5, which indicates a healthy 
            financial position with moderate leverage.
            """
            
            result = await self.reasoning_service.llm_validator.validate_financial_calculations(test_text)
            
            assert isinstance(result, ValidationResult), "Should return ValidationResult"
            assert hasattr(result, 'is_valid'), "Should have is_valid attribute"
            assert hasattr(result, 'confidence'), "Should have confidence attribute"
            
            execution_time = time.time() - start_time
            return TestResult("Financial Validation", True, f"Confidence: {result.confidence}", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("Financial Validation", False, str(e), execution_time)
    
    async def test_logical_consistency(self) -> TestResult:
        """Test logical consistency validation."""
        start_time = time.time()
        try:
            test_statements = [
                "The system is compliant with HIPAA requirements.",
                "All access controls are properly implemented.",
                "The system is not compliant with HIPAA requirements."
            ]
            
            result = await self.reasoning_service.llm_validator.validate_logical_consistency(test_statements)
            
            assert isinstance(result, ValidationResult), "Should return ValidationResult"
            assert hasattr(result, 'is_valid'), "Should have is_valid attribute"
            
            execution_time = time.time() - start_time
            return TestResult("Logical Consistency", True, f"Consistent: {result.is_valid}", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("Logical Consistency", False, str(e), execution_time)
    
    async def test_hybrid_reasoning(self) -> TestResult:
        """Test combined LLM and graph reasoning."""
        start_time = time.time()
        try:
            test_text = """
            Our healthcare application implements HIPAA-compliant access controls 
            for electronic protected health information. Users authenticate through 
            multi-factor authentication and all data transmissions are encrypted.
            """
            
            result = await self.reasoning_service.reason_about_text(test_text, "healthcare")
            
            assert isinstance(result, dict), "Should return a dictionary"
            assert "validation_results" in result, "Should have validation_results"
            assert "graph_insights" in result, "Should have graph_insights"
            assert "overall_confidence" in result, "Should have overall_confidence"
            assert "recommendations" in result, "Should have recommendations"
            
            execution_time = time.time() - start_time
            return TestResult("Hybrid Reasoning", True, f"Confidence: {result['overall_confidence']:.2f}", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("Hybrid Reasoning", False, str(e), execution_time)
    
    async def test_knowledge_graph_insights(self) -> TestResult:
        """Test knowledge graph insight extraction."""
        start_time = time.time()
        try:
            test_text = "HIPAA compliance requires access control and authentication for electronic PHI."
            
            insights = self.reasoning_service._extract_graph_insights(test_text, "healthcare")
            
            assert isinstance(insights, dict), "Should return a dictionary"
            assert "related_concepts" in insights, "Should have related_concepts"
            assert "compliance_paths" in insights, "Should have compliance_paths"
            assert "knowledge_gaps" in insights, "Should have knowledge_gaps"
            
            execution_time = time.time() - start_time
            return TestResult("Knowledge Graph Insights", True, f"Concepts: {len(insights['related_concepts'])}", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("Knowledge Graph Insights", False, str(e), execution_time)
    
    async def test_performance_benchmark(self) -> TestResult:
        """Test system performance with multiple operations."""
        start_time = time.time()
        try:
            test_texts = [
                "HIPAA compliance requires access controls for electronic PHI.",
                "The debt-to-equity ratio is 0.5 with $500K debt and $1M equity.",
                "Multi-factor authentication is implemented for all user access.",
                "Data encryption is used for all electronic transmissions.",
                "Audit logs are maintained for compliance monitoring."
            ]
            
            total_time = 0
            for text in test_texts:
                op_start = time.time()
                await self.reasoning_service.reason_about_text(text, "healthcare")
                total_time += time.time() - op_start
            
            avg_time = total_time / len(test_texts)
            execution_time = time.time() - start_time
            
            # Performance threshold: average operation should be under 2 seconds
            passed = avg_time < 2.0
            
            return TestResult("Performance Benchmark", passed, 
                            f"Avg: {avg_time:.2f}s per operation", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("Performance Benchmark", False, str(e), execution_time)
    
    async def test_error_handling(self) -> TestResult:
        """Test error handling with invalid inputs."""
        start_time = time.time()
        try:
            # Test with empty text
            result1 = await self.reasoning_service.reason_about_text("", "healthcare")
            assert isinstance(result1, dict), "Should handle empty text gracefully"
            
            # Test with invalid domain
            result3 = await self.reasoning_service.reason_about_text("test", "invalid_domain")
            assert isinstance(result3, dict), "Should handle invalid domain gracefully"
            
            execution_time = time.time() - start_time
            return TestResult("Error Handling", True, "All error cases handled", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("Error Handling", False, str(e), execution_time)
    
    async def test_concurrent_operations(self) -> TestResult:
        """Test concurrent operations for scalability."""
        start_time = time.time()
        try:
            test_text = "HIPAA compliance requires access controls and authentication."
            
            # Run multiple concurrent operations
            tasks = []
            for i in range(5):
                task = self.reasoning_service.reason_about_text(f"{test_text} Test {i}", "healthcare")
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check that all operations completed
            successful_results = [r for r in results if isinstance(r, dict)]
            failed_results = [r for r in results if isinstance(r, Exception)]
            
            success_rate = len(successful_results) / len(results)
            passed = success_rate >= 0.8  # 80% success rate threshold
            
            execution_time = time.time() - start_time
            return TestResult("Concurrent Operations", passed, 
                            f"Success rate: {success_rate:.2f}", execution_time)
        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult("Concurrent Operations", False, str(e), execution_time)
    
    async def run_all_tests(self):
        """Run all tests and generate report."""
        print("🚀 Starting XReason Hybrid System Tests")
        print("=" * 60)
        
        test_methods = [
            self.test_llm_service_initialization,
            self.test_reasoning_service_initialization,
            self.test_knowledge_graph_operations,
            self.test_hipaa_validation,
            self.test_financial_validation,
            self.test_logical_consistency,
            self.test_hybrid_reasoning,
            self.test_knowledge_graph_insights,
            self.test_performance_benchmark,
            self.test_error_handling,
            self.test_concurrent_operations
        ]
        
        for test_method in test_methods:
            result = await test_method()
            self.add_result(result)
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.passed)
        failed_tests = total_tests - passed_tests
        total_time = sum(r.execution_time for r in self.test_results)
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Total Execution Time: {total_time:.2f}s")
        
        if failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! Hybrid system is robust and ready.")
        else:
            print(f"\n⚠️  {failed_tests} tests failed. Review and fix issues.")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": passed_tests / total_tests,
            "total_time": total_time,
            "results": self.test_results
        }


async def main():
    """Main test runner."""
    tester = HybridSystemTester()
    summary = await tester.run_all_tests()
    
    # Exit with appropriate code
    if summary["failed_tests"] == 0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
