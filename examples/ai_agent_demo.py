#!/usr/bin/env python3
"""
Advanced AI Agent Demo for XReason
Demonstrates intelligent agents with knowledge integration and learning capabilities.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# Import the SDK
try:
    import httpx
except ImportError:
    print("❌ httpx not found. Please install it first:")
    print("   pip install httpx")
    exit(1)


class AIAgentDemo:
    """Comprehensive demo of XReason AI agents."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
        self.results = {}
    
    async def run_demo(self):
        """Run the comprehensive AI agent demo."""
        print("🤖 XReason Advanced AI Agent Demo")
        print("=" * 50)
        
        # Test health check first
        try:
            async with httpx.AsyncClient() as client:
                health_response = await client.get(f"{self.base_url}/api/v1/agents/health")
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    print(f"✅ Agent system health: {health_data.get('status', 'unknown')}")
                    print(f"   Active agents: {health_data.get('agents', {}).get('active', 0)}")
                    print(f"   Active sessions: {health_data.get('sessions', {}).get('active', 0)}")
                else:
                    print(f"❌ Health check failed: {health_response.status_code}")
                    print("Make sure the XReason backend is running on http://localhost:8000")
                    return
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            print("Make sure the XReason backend is running on http://localhost:8000")
            return
        
        print("\n" + "=" * 50)
        
        # Run all agent demos
        await self.demo_session_management()
        await self.demo_reasoning_agent()
        await self.demo_knowledge_agent()
        await self.demo_validation_agent()
        await self.demo_memory_operations()
        await self.demo_learning_operations()
        await self.demo_knowledge_integration()
        await self.demo_system_status()
        
        # Generate summary report
        self.generate_summary_report()
    
    async def demo_session_management(self):
        """Demo session management."""
        print("\n📋 Session Management")
        print("-" * 30)
        
        async with httpx.AsyncClient() as client:
            # Create session
            session_request = {
                "user_id": "demo_user_001",
                "domain": "general",
                "agent_type": "reasoning_agent",
                "metadata": {"demo": True}
            }
            
            print("📋 Creating agent session...")
            response = await client.post(
                f"{self.base_url}/api/v1/agents/sessions",
                json=session_request
            )
            
            if response.status_code == 200:
                session_data = response.json()
                self.session_id = session_data["session_id"]
                print(f"   ✅ Session created: {self.session_id}")
                
                # Get session info
                session_info_response = await client.get(
                    f"{self.base_url}/api/v1/agents/sessions/{self.session_id}"
                )
                
                if session_info_response.status_code == 200:
                    session_info = session_info_response.json()
                    print(f"   📊 Session info:")
                    print(f"      User ID: {session_info.get('user_id')}")
                    print(f"      Domain: {session_info.get('domain')}")
                    print(f"      Status: {session_info.get('status')}")
                    print(f"      Task Count: {session_info.get('task_count')}")
                else:
                    print(f"   ❌ Failed to get session info: {session_info_response.status_code}")
            else:
                print(f"   ❌ Failed to create session: {response.status_code}")
                print(f"   Error: {response.text}")
    
    async def demo_reasoning_agent(self):
        """Demo reasoning agent capabilities."""
        print("\n🧠 Reasoning Agent Demo")
        print("-" * 30)
        
        if not self.session_id:
            print("   ❌ No session available")
            return
        
        async with httpx.AsyncClient() as client:
            # Complex reasoning task
            reasoning_request = {
                "session_id": self.session_id,
                "input_data": {
                    "question": "If a company has $1M revenue, $500K costs, and $200K in debt, what is their profit margin and debt-to-equity ratio?",
                    "context": "Financial analysis for business decision making"
                },
                "agent_types": ["reasoning_agent"],
                "priority": "high",
                "metadata": {"task_type": "financial_analysis"}
            }
            
            print("🧠 Processing with reasoning agent...")
            response = await client.post(
                f"{self.base_url}/api/v1/agents/reasoning",
                json=reasoning_request
            )
            
            if response.status_code == 200:
                result = response.json()
                self.results['reasoning'] = result
                print(f"   ✅ Success: {result.get('success')}")
                print(f"   🎯 Confidence: {result.get('confidence', 0):.2f}")
                print(f"   ⏱️  Processing time: {result.get('processing_time', 0):.2f}s")
                print(f"   🤖 Agent used: {result.get('agent_used')}")
                
                # Show reasoning
                reasoning = result.get('reasoning', '')
                if reasoning:
                    print(f"   💭 Reasoning: {reasoning[:200]}...")
            else:
                print(f"   ❌ Reasoning failed: {response.status_code}")
                print(f"   Error: {response.text}")
    
    async def demo_knowledge_agent(self):
        """Demo knowledge agent capabilities."""
        print("\n📚 Knowledge Agent Demo")
        print("-" * 30)
        
        if not self.session_id:
            print("   ❌ No session available")
            return
        
        async with httpx.AsyncClient() as client:
            # Knowledge integration task
            knowledge_request = {
                "session_id": self.session_id,
                "input_data": {
                    "topic": "machine learning algorithms",
                    "query": "What are the key differences between supervised and unsupervised learning?",
                    "context": "Educational content for AI beginners"
                },
                "agent_types": ["knowledge_agent"],
                "priority": "medium",
                "metadata": {"task_type": "knowledge_integration"}
            }
            
            print("📚 Processing with knowledge agent...")
            response = await client.post(
                f"{self.base_url}/api/v1/agents/knowledge-integration",
                json=knowledge_request
            )
            
            if response.status_code == 200:
                result = response.json()
                self.results['knowledge'] = result
                print(f"   ✅ Success: {result.get('success')}")
                print(f"   🎯 Confidence: {result.get('confidence', 0):.2f}")
                print(f"   ⏱️  Processing time: {result.get('processing_time', 0):.2f}s")
                print(f"   🤖 Agent used: {result.get('agent_used')}")
                
                # Show knowledge integration
                reasoning = result.get('reasoning', '')
                if reasoning:
                    print(f"   📖 Knowledge: {reasoning[:200]}...")
            else:
                print(f"   ❌ Knowledge integration failed: {response.status_code}")
                print(f"   Error: {response.text}")
    
    async def demo_validation_agent(self):
        """Demo validation agent capabilities."""
        print("\n✅ Validation Agent Demo")
        print("-" * 30)
        
        if not self.session_id:
            print("   ❌ No session available")
            return
        
        async with httpx.AsyncClient() as client:
            # Validation task
            validation_request = {
                "session_id": self.session_id,
                "input_data": {
                    "statement": "The Earth is flat and the moon landing was faked",
                    "context": "Fact checking and validation"
                },
                "agent_types": ["validation_agent"],
                "priority": "high",
                "metadata": {"task_type": "fact_validation"}
            }
            
            print("✅ Processing with validation agent...")
            response = await client.post(
                f"{self.base_url}/api/v1/agents/validation",
                json=validation_request
            )
            
            if response.status_code == 200:
                result = response.json()
                self.results['validation'] = result
                print(f"   ✅ Success: {result.get('success')}")
                print(f"   🎯 Confidence: {result.get('confidence', 0):.2f}")
                print(f"   ⏱️  Processing time: {result.get('processing_time', 0):.2f}s")
                print(f"   🤖 Agent used: {result.get('agent_used')}")
                
                # Show validation result
                reasoning = result.get('reasoning', '')
                if reasoning:
                    print(f"   🔍 Validation: {reasoning[:200]}...")
            else:
                print(f"   ❌ Validation failed: {response.status_code}")
                print(f"   Error: {response.text}")
    
    async def demo_memory_operations(self):
        """Demo memory operations."""
        print("\n🧠 Memory Operations Demo")
        print("-" * 30)
        
        if not self.session_id:
            print("   ❌ No session available")
            return
        
        async with httpx.AsyncClient() as client:
            # Store memory
            memory_request = {
                "session_id": self.session_id,
                "memory_type": "long_term",
                "key": "demo_pattern_001",
                "value": {
                    "pattern": "financial_analysis",
                    "frequency": 1,
                    "success_rate": 0.85,
                    "created_at": datetime.now().isoformat()
                },
                "operation": "set"
            }
            
            print("🧠 Storing memory...")
            response = await client.post(
                f"{self.base_url}/api/v1/agents/memory",
                json=memory_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Memory stored: {result.get('success')}")
                print(f"   🔑 Key: {result.get('key')}")
                print(f"   📊 Type: {result.get('memory_type')}")
                
                # Retrieve memory
                retrieve_request = {
                    "session_id": self.session_id,
                    "memory_type": "long_term",
                    "key": "demo_pattern_001",
                    "operation": "get"
                }
                
                print("🧠 Retrieving memory...")
                retrieve_response = await client.post(
                    f"{self.base_url}/api/v1/agents/memory",
                    json=retrieve_request
                )
                
                if retrieve_response.status_code == 200:
                    retrieve_result = retrieve_response.json()
                    print(f"   ✅ Memory retrieved: {retrieve_result.get('success')}")
                    print(f"   📊 Value: {retrieve_result.get('value')}")
                else:
                    print(f"   ❌ Memory retrieval failed: {retrieve_response.status_code}")
            else:
                print(f"   ❌ Memory storage failed: {response.status_code}")
    
    async def demo_learning_operations(self):
        """Demo learning operations."""
        print("\n🎓 Learning Operations Demo")
        print("-" * 30)
        
        if not self.session_id:
            print("   ❌ No session available")
            return
        
        async with httpx.AsyncClient() as client:
            # Pattern learning
            learning_request = {
                "session_id": self.session_id,
                "learning_type": "pattern",
                "input_data": {
                    "pattern": "financial_calculation",
                    "input": "revenue and costs",
                    "output": "profit margin",
                    "success": True
                },
                "feedback": {
                    "accuracy": 0.9,
                    "usefulness": 0.85,
                    "improvement": "good"
                },
                "adaptation_target": "improve_calculation_accuracy"
            }
            
            print("🎓 Learning pattern...")
            response = await client.post(
                f"{self.base_url}/api/v1/agents/learning",
                json=learning_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Learning successful: {result.get('success')}")
                print(f"   🎯 Adaptation applied: {result.get('adaptation_applied')}")
                print(f"   📊 Success rate: {result.get('success_rate', 0):.2f}")
                print(f"   💭 Reasoning: {result.get('reasoning', '')}")
            else:
                print(f"   ❌ Learning failed: {response.status_code}")
                print(f"   Error: {response.text}")
    
    async def demo_knowledge_integration(self):
        """Demo knowledge integration operations."""
        print("\n📚 Knowledge Integration Demo")
        print("-" * 30)
        
        if not self.session_id:
            print("   ❌ No session available")
            return
        
        async with httpx.AsyncClient() as client:
            # Add knowledge
            knowledge_request = {
                "session_id": self.session_id,
                "knowledge_type": "fact",
                "content": {
                    "id": "fact_001",
                    "subject": "artificial intelligence",
                    "predicate": "is",
                    "object": "a branch of computer science",
                    "confidence": 0.95,
                    "source": "academic"
                },
                "source": "demo",
                "confidence": 0.95,
                "operation": "add"
            }
            
            print("📚 Adding knowledge...")
            response = await client.post(
                f"{self.base_url}/api/v1/agents/knowledge",
                json=knowledge_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Knowledge added: {result.get('success')}")
                print(f"   📊 Type: {result.get('knowledge_type')}")
                print(f"   🎯 Confidence: {result.get('confidence', 0):.2f}")
                print(f"   📖 Content: {result.get('content')}")
            else:
                print(f"   ❌ Knowledge addition failed: {response.status_code}")
                print(f"   Error: {response.text}")
    
    async def demo_system_status(self):
        """Demo system status monitoring."""
        print("\n📊 System Status Demo")
        print("-" * 30)
        
        async with httpx.AsyncClient() as client:
            # Get system status
            print("📊 Getting system status...")
            response = await client.get(f"{self.base_url}/api/v1/agents/status")
            
            if response.status_code == 200:
                status = response.json()
                self.results['system_status'] = status
                
                print(f"   🏥 System health: {status.get('system_health')}")
                print(f"   🤖 Total agents: {status.get('total_agents')}")
                print(f"   ✅ Active agents: {status.get('active_agents')}")
                print(f"   📋 Total sessions: {status.get('total_sessions')}")
                print(f"   🔄 Active sessions: {status.get('active_sessions')}")
                print(f"   📊 Total tasks: {status.get('total_tasks')}")
                print(f"   ✅ Completed tasks: {status.get('completed_tasks')}")
                print(f"   ❌ Failed tasks: {status.get('failed_tasks')}")
                print(f"   ⏱️  Avg processing time: {status.get('avg_processing_time', 0):.2f}s")
                
                # Show agent statuses
                agent_statuses = status.get('agent_statuses', [])
                if agent_statuses:
                    print(f"   🤖 Agent details:")
                    for agent in agent_statuses:
                        print(f"      - {agent.get('agent_id')}: {agent.get('state')} ({agent.get('agent_type')})")
            else:
                print(f"   ❌ Failed to get system status: {response.status_code}")
    
    def generate_summary_report(self):
        """Generate a summary report of all agent operations."""
        print("\n" + "=" * 50)
        print("📊 AI AGENT DEMO SUMMARY")
        print("=" * 50)
        
        total_operations = len(self.results)
        successful_operations = sum(1 for r in self.results.values() if r.get('success', False))
        
        print(f"Total Operations: {total_operations}")
        print(f"Successful: {successful_operations}")
        print(f"Success Rate: {(successful_operations / total_operations * 100):.1f}%" if total_operations > 0 else "N/A")
        
        print("\n📋 Operation Details:")
        for operation, result in self.results.items():
            success = "✅" if result.get('success', False) else "❌"
            confidence = result.get('confidence', 0)
            processing_time = result.get('processing_time', 0)
            
            print(f"   {operation:20} | {success:2} | Confidence: {confidence:.2f} | Time: {processing_time:.2f}s")
        
        # Save detailed results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_agent_demo_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: {filename}")
        print("\n🎉 AI Agent demo completed successfully!")
        print("\n🌐 Access the API documentation at: http://localhost:8000/docs")
        print("📊 View agent metrics at: http://localhost:3002 (Grafana)")


async def main():
    """Main demo function."""
    demo = AIAgentDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main())
