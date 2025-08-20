"""
Advanced AI Agent Service for XReason
Provides intelligent agents with knowledge integration and multi-agent coordination.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import uuid

from pydantic import BaseModel
import httpx

from app.core.config import settings
from app.services.llm_service import LLMService
from app.services.symbolic_service import SymbolicService
from app.services.knowledge_service import KnowledgeService
from app.services.metrics_service import ReasoningMetricsService
from app.models.reasoning_graph import ReasoningGraph, GraphNode, GraphEdge
from app.schemas.agent import (
    AgentType, AgentState, TaskPriority, TaskStatus,
    AgentProcessingRequest, AgentProcessingResponse,
    AgentStatusResponse, AgentSystemStatus
)

logger = logging.getLogger(__name__)


@dataclass
class AgentContext:
    """Context for agent operations."""
    session_id: str
    user_id: Optional[str] = None
    domain: Optional[str] = None
    task_type: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """Result from agent operation."""
    success: bool
    data: Any
    confidence: float
    reasoning: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class AgentMemory:
    """Memory system for agents."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.short_term: List[Dict] = []
        self.long_term: Dict[str, Any] = {}
        self.patterns: Dict[str, Any] = {}
    
    def add_memory(self, key: str, value: Any, memory_type: str = "short_term"):
        """Add memory entry."""
        if memory_type == "short_term":
            self.short_term.append({
                "key": key,
                "value": value,
                "timestamp": datetime.now(),
                "access_count": 0
            })
            if len(self.short_term) > self.max_size:
                self.short_term.pop(0)
        else:
            self.long_term[key] = {
                "value": value,
                "timestamp": datetime.now(),
                "access_count": 0
            }
    
    def get_memory(self, key: str, memory_type: str = "short_term") -> Optional[Any]:
        """Retrieve memory entry."""
        if memory_type == "short_term":
            for memory in self.short_term:
                if memory["key"] == key:
                    memory["access_count"] += 1
                    return memory["value"]
        else:
            if key in self.long_term:
                self.long_term[key]["access_count"] += 1
                return self.long_term[key]["value"]
        return None
    
    def update_patterns(self, pattern: str, frequency: int = 1):
        """Update pattern recognition."""
        if pattern in self.patterns:
            self.patterns[pattern]["frequency"] += frequency
            self.patterns[pattern]["last_seen"] = datetime.now()
        else:
            self.patterns[pattern] = {
                "frequency": frequency,
                "first_seen": datetime.now(),
                "last_seen": datetime.now()
            }


class BaseAgent:
    """Base class for all AI agents."""
    
    def __init__(self, agent_id: str, agent_type: AgentType, capabilities: List[str]):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.state = AgentState.IDLE
        self.memory = AgentMemory()
        self.llm_service = LLMService()
        self.symbolic_service = SymbolicService()
        self.knowledge_service = KnowledgeService()
        self.metrics_service = ReasoningMetricsService()
        self.performance_metrics = {
            "tasks_completed": 0,
            "success_rate": 0.0,
            "avg_response_time": 0.0,
            "total_response_time": 0.0
        }
    
    async def think(self, context: AgentContext, input_data: Any) -> AgentResult:
        """Agent thinking process."""
        raise NotImplementedError
    
    def update_metrics(self, success: bool, response_time: float):
        """Update performance metrics."""
        self.performance_metrics["tasks_completed"] += 1
        self.performance_metrics["total_response_time"] += response_time
        self.performance_metrics["avg_response_time"] = (
            self.performance_metrics["total_response_time"] / 
            self.performance_metrics["tasks_completed"]
        )
        
        if self.performance_metrics["tasks_completed"] > 0:
            success_count = sum(1 for _ in range(self.performance_metrics["tasks_completed"]) if success)
            self.performance_metrics["success_rate"] = success_count / self.performance_metrics["tasks_completed"]


class ReasoningAgent(BaseAgent):
    """Intelligent reasoning agent with advanced reasoning capabilities."""
    
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.REASONING_AGENT,
            capabilities=["reasoning", "hypothesis_generation", "logical_inference", "pattern_recognition"]
        )
        self.reasoning_strategies = [
            "deductive_reasoning",
            "inductive_reasoning",
            "abductive_reasoning",
            "analogical_reasoning",
            "causal_reasoning"
        ]
    
    async def think(self, context: AgentContext, input_data: Any) -> AgentResult:
        """Advanced reasoning process."""
        start_time = datetime.now()
        self.state = AgentState.THINKING
        
        try:
            # Analyze input and determine reasoning strategy
            strategy = await self._select_reasoning_strategy(input_data)
            
            # Generate hypotheses
            hypotheses = await self._generate_hypotheses(input_data, strategy)
            
            # Evaluate hypotheses using symbolic reasoning
            evaluations = await self._evaluate_hypotheses(hypotheses)
            
            # Integrate knowledge
            knowledge_integration = await self._integrate_knowledge(input_data, hypotheses)
            
            # Synthesize final reasoning
            reasoning_result = await self._synthesize_reasoning(
                input_data, hypotheses, evaluations, knowledge_integration
            )
            
            response_time = (datetime.now() - start_time).total_seconds()
            self.update_metrics(True, response_time)
            
            return AgentResult(
                success=True,
                data=reasoning_result,
                confidence=reasoning_result.get("confidence", 0.8),
                reasoning=reasoning_result.get("reasoning", ""),
                metadata={
                    "strategy": strategy,
                    "hypotheses_count": len(hypotheses),
                    "response_time": response_time
                }
            )
            
        except Exception as e:
            logger.error(f"Reasoning agent error: {e}")
            response_time = (datetime.now() - start_time).total_seconds()
            self.update_metrics(False, response_time)
            
            return AgentResult(
                success=False,
                data=None,
                confidence=0.0,
                reasoning=f"Error in reasoning: {str(e)}",
                metadata={"error": str(e)}
            )
        finally:
            self.state = AgentState.IDLE
    
    async def _select_reasoning_strategy(self, input_data: Any) -> str:
        """Select appropriate reasoning strategy."""
        prompt = f"""
        Analyze the following input and select the most appropriate reasoning strategy:
        
        Input: {input_data}
        
        Available strategies:
        - deductive_reasoning: For logical conclusions from premises
        - inductive_reasoning: For generalizing from specific observations
        - abductive_reasoning: For finding the best explanation
        - analogical_reasoning: For finding similarities and patterns
        - causal_reasoning: For understanding cause-effect relationships
        
        Return only the strategy name.
        """
        
        response = await self.llm_service.generate_response(prompt)
        strategy = response.strip().lower()
        
        if strategy not in self.reasoning_strategies:
            strategy = "deductive_reasoning"  # Default
        
        return strategy
    
    async def _generate_hypotheses(self, input_data: Any, strategy: str) -> List[Dict]:
        """Generate hypotheses based on reasoning strategy."""
        prompt = f"""
        Generate hypotheses using {strategy} for the following input:
        
        Input: {input_data}
        
        Generate 3-5 hypotheses with confidence scores and reasoning.
        Return as JSON array with fields: hypothesis, confidence, reasoning
        """
        
        response = await self.llm_service.generate_response(prompt)
        
        try:
            hypotheses = json.loads(response)
            return hypotheses if isinstance(hypotheses, list) else []
        except json.JSONDecodeError:
            return []
    
    async def _evaluate_hypotheses(self, hypotheses: List[Dict]) -> List[Dict]:
        """Evaluate hypotheses using symbolic reasoning."""
        evaluations = []
        
        for hypothesis in hypotheses:
            # Use symbolic service to validate hypothesis
            validation_result = await self.symbolic_service.validate_statement(
                hypothesis.get("hypothesis", "")
            )
            
            evaluations.append({
                "hypothesis": hypothesis,
                "symbolic_validation": validation_result,
                "confidence_adjustment": validation_result.get("confidence", 0.0)
            })
        
        return evaluations
    
    async def _integrate_knowledge(self, input_data: Any, hypotheses: List[Dict]) -> Dict:
        """Integrate knowledge from knowledge graph."""
        # Extract key concepts from input and hypotheses
        concepts = await self._extract_concepts(input_data, hypotheses)
        
        # Query knowledge graph
        knowledge_results = {}
        for concept in concepts:
            knowledge = await self.knowledge_service.query_knowledge(concept)
            if knowledge:
                knowledge_results[concept] = knowledge
        
        return {
            "concepts": concepts,
            "knowledge": knowledge_results,
            "integration_score": len(knowledge_results) / max(len(concepts), 1)
        }
    
    async def _extract_concepts(self, input_data: Any, hypotheses: List[Dict]) -> List[str]:
        """Extract key concepts for knowledge integration."""
        prompt = f"""
        Extract key concepts from the following input and hypotheses:
        
        Input: {input_data}
        Hypotheses: {hypotheses}
        
        Return as JSON array of concept strings.
        """
        
        response = await self.llm_service.generate_response(prompt)
        
        try:
            concepts = json.loads(response)
            return concepts if isinstance(concepts, list) else []
        except json.JSONDecodeError:
            return []
    
    async def _synthesize_reasoning(
        self, 
        input_data: Any, 
        hypotheses: List[Dict], 
        evaluations: List[Dict], 
        knowledge_integration: Dict
    ) -> Dict:
        """Synthesize final reasoning result."""
        prompt = f"""
        Synthesize the final reasoning result from:
        
        Input: {input_data}
        Hypotheses: {hypotheses}
        Evaluations: {evaluations}
        Knowledge Integration: {knowledge_integration}
        
        Return as JSON with fields: conclusion, confidence, reasoning, supporting_evidence
        """
        
        response = await self.llm_service.generate_response(prompt)
        
        try:
            result = json.loads(response)
            return result if isinstance(result, dict) else {}
        except json.JSONDecodeError:
            return {
                "conclusion": "Unable to synthesize reasoning",
                "confidence": 0.0,
                "reasoning": "Error in synthesis",
                "supporting_evidence": []
            }


class KnowledgeAgent(BaseAgent):
    """Knowledge integration and management agent."""
    
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.KNOWLEDGE_AGENT,
            capabilities=["knowledge_integration", "knowledge_discovery", "knowledge_validation", "knowledge_synthesis"]
        )
    
    async def think(self, context: AgentContext, input_data: Any) -> AgentResult:
        """Knowledge integration process."""
        start_time = datetime.now()
        self.state = AgentState.THINKING
        
        try:
            # Discover relevant knowledge
            discovered_knowledge = await self._discover_knowledge(input_data)
            
            # Validate knowledge consistency
            validation_result = await self._validate_knowledge(discovered_knowledge)
            
            # Synthesize knowledge
            synthesis_result = await self._synthesize_knowledge(discovered_knowledge, validation_result)
            
            # Update knowledge graph
            update_result = await self._update_knowledge_graph(synthesis_result)
            
            response_time = (datetime.now() - start_time).total_seconds()
            self.update_metrics(True, response_time)
            
            return AgentResult(
                success=True,
                data=synthesis_result,
                confidence=synthesis_result.get("confidence", 0.8),
                reasoning=synthesis_result.get("reasoning", ""),
                metadata={
                    "discovered_count": len(discovered_knowledge),
                    "validated_count": len(validation_result.get("valid", [])),
                    "update_count": update_result.get("updated", 0)
                }
            )
            
        except Exception as e:
            logger.error(f"Knowledge agent error: {e}")
            response_time = (datetime.now() - start_time).total_seconds()
            self.update_metrics(False, response_time)
            
            return AgentResult(
                success=False,
                data=None,
                confidence=0.0,
                reasoning=f"Error in knowledge integration: {str(e)}",
                metadata={"error": str(e)}
            )
        finally:
            self.state = AgentState.IDLE
    
    async def _discover_knowledge(self, input_data: Any) -> List[Dict]:
        """Discover relevant knowledge from various sources."""
        # Extract entities and relationships
        entities = await self._extract_entities(input_data)
        
        # Query knowledge graph
        knowledge_results = []
        for entity in entities:
            knowledge = await self.knowledge_service.query_knowledge(entity)
            if knowledge:
                knowledge_results.append({
                    "entity": entity,
                    "knowledge": knowledge,
                    "source": "knowledge_graph"
                })
        
        # Discover patterns
        patterns = await self._discover_patterns(input_data)
        knowledge_results.extend(patterns)
        
        return knowledge_results
    
    async def _extract_entities(self, input_data: Any) -> List[str]:
        """Extract entities from input."""
        prompt = f"""
        Extract named entities and key concepts from:
        
        Input: {input_data}
        
        Return as JSON array of entity strings.
        """
        
        response = await self.llm_service.generate_response(prompt)
        
        try:
            entities = json.loads(response)
            return entities if isinstance(entities, list) else []
        except json.JSONDecodeError:
            return []
    
    async def _discover_patterns(self, input_data: Any) -> List[Dict]:
        """Discover patterns in the input."""
        # Use memory patterns
        patterns = []
        for pattern, data in self.memory.patterns.items():
            if pattern.lower() in str(input_data).lower():
                patterns.append({
                    "pattern": pattern,
                    "frequency": data["frequency"],
                    "source": "memory_patterns"
                })
        
        return patterns
    
    async def _validate_knowledge(self, knowledge_list: List[Dict]) -> Dict:
        """Validate knowledge consistency."""
        valid_knowledge = []
        invalid_knowledge = []
        
        for knowledge_item in knowledge_list:
            # Use symbolic reasoning to validate
            validation = await self.symbolic_service.validate_statement(
                str(knowledge_item)
            )
            
            if validation.get("is_valid", False):
                valid_knowledge.append(knowledge_item)
            else:
                invalid_knowledge.append(knowledge_item)
        
        return {
            "valid": valid_knowledge,
            "invalid": invalid_knowledge,
            "validation_score": len(valid_knowledge) / max(len(knowledge_list), 1)
        }
    
    async def _synthesize_knowledge(self, knowledge_list: List[Dict], validation_result: Dict) -> Dict:
        """Synthesize knowledge into coherent structure."""
        valid_knowledge = validation_result.get("valid", [])
        
        prompt = f"""
        Synthesize the following knowledge into a coherent structure:
        
        Knowledge: {valid_knowledge}
        
        Return as JSON with fields: synthesis, confidence, reasoning, relationships
        """
        
        response = await self.llm_service.generate_response(prompt)
        
        try:
            synthesis = json.loads(response)
            return synthesis if isinstance(synthesis, dict) else {}
        except json.JSONDecodeError:
            return {
                "synthesis": "Unable to synthesize knowledge",
                "confidence": 0.0,
                "reasoning": "Error in synthesis",
                "relationships": []
            }
    
    async def _update_knowledge_graph(self, synthesis_result: Dict) -> Dict:
        """Update knowledge graph with new information."""
        try:
            # Add new knowledge to graph
            updated_count = 0
            synthesis = synthesis_result.get("synthesis", "")
            relationships = synthesis_result.get("relationships", [])
            
            if synthesis:
                await self.knowledge_service.add_knowledge(synthesis)
                updated_count += 1
            
            for relationship in relationships:
                await self.knowledge_service.add_relationship(relationship)
                updated_count += 1
            
            return {"updated": updated_count}
        except Exception as e:
            logger.error(f"Knowledge graph update error: {e}")
            return {"updated": 0, "error": str(e)}


class ValidationAgent(BaseAgent):
    """Validation and verification agent."""
    
    def __init__(self, agent_id: str):
        super().__init__(
            agent_id=agent_id,
            agent_type=AgentType.VALIDATION_AGENT,
            capabilities=["validation", "verification", "consistency_checking", "error_detection"]
        )
    
    async def think(self, context: AgentContext, input_data: Any) -> AgentResult:
        """Validation process."""
        start_time = datetime.now()
        self.state = AgentState.THINKING
        
        try:
            # Multi-level validation
            logical_validation = await self._logical_validation(input_data)
            factual_validation = await self._factual_validation(input_data)
            consistency_validation = await self._consistency_validation(input_data)
            
            # Synthesize validation results
            validation_result = await self._synthesize_validation(
                logical_validation, factual_validation, consistency_validation
            )
            
            response_time = (datetime.now() - start_time).total_seconds()
            self.update_metrics(True, response_time)
            
            return AgentResult(
                success=True,
                data=validation_result,
                confidence=validation_result.get("confidence", 0.8),
                reasoning=validation_result.get("reasoning", ""),
                metadata={
                    "logical_score": logical_validation.get("score", 0.0),
                    "factual_score": factual_validation.get("score", 0.0),
                    "consistency_score": consistency_validation.get("score", 0.0)
                }
            )
            
        except Exception as e:
            logger.error(f"Validation agent error: {e}")
            response_time = (datetime.now() - start_time).total_seconds()
            self.update_metrics(False, response_time)
            
            return AgentResult(
                success=False,
                data=None,
                confidence=0.0,
                reasoning=f"Error in validation: {str(e)}",
                metadata={"error": str(e)}
            )
        finally:
            self.state = AgentState.IDLE
    
    async def _logical_validation(self, input_data: Any) -> Dict:
        """Validate logical consistency."""
        prompt = f"""
        Validate the logical consistency of:
        
        Input: {input_data}
        
        Check for logical contradictions, fallacies, and inconsistencies.
        Return as JSON with fields: is_valid, score, issues, reasoning
        """
        
        response = await self.llm_service.generate_response(prompt)
        
        try:
            result = json.loads(response)
            return result if isinstance(result, dict) else {"is_valid": False, "score": 0.0}
        except json.JSONDecodeError:
            return {"is_valid": False, "score": 0.0, "issues": ["JSON parsing error"]}
    
    async def _factual_validation(self, input_data: Any) -> Dict:
        """Validate factual accuracy."""
        # Extract factual claims
        claims = await self._extract_claims(input_data)
        
        # Validate against knowledge graph
        validation_results = []
        for claim in claims:
            knowledge = await self.knowledge_service.query_knowledge(claim)
            validation_results.append({
                "claim": claim,
                "supported": bool(knowledge),
                "evidence": knowledge
            })
        
        valid_count = sum(1 for r in validation_results if r["supported"])
        score = valid_count / max(len(validation_results), 1)
        
        return {
            "is_valid": score > 0.7,
            "score": score,
            "claims": validation_results,
            "reasoning": f"{valid_count}/{len(validation_results)} claims supported"
        }
    
    async def _extract_claims(self, input_data: Any) -> List[str]:
        """Extract factual claims from input."""
        prompt = f"""
        Extract factual claims from:
        
        Input: {input_data}
        
        Return as JSON array of claim strings.
        """
        
        response = await self.llm_service.generate_response(prompt)
        
        try:
            claims = json.loads(response)
            return claims if isinstance(claims, list) else []
        except json.JSONDecodeError:
            return []
    
    async def _consistency_validation(self, input_data: Any) -> Dict:
        """Validate internal consistency."""
        # Use symbolic service for consistency checking
        consistency_result = await self.symbolic_service.check_consistency(str(input_data))
        
        return {
            "is_valid": consistency_result.get("is_consistent", False),
            "score": consistency_result.get("consistency_score", 0.0),
            "issues": consistency_result.get("inconsistencies", []),
            "reasoning": consistency_result.get("reasoning", "")
        }
    
    async def _synthesize_validation(
        self, 
        logical_validation: Dict, 
        factual_validation: Dict, 
        consistency_validation: Dict
    ) -> Dict:
        """Synthesize validation results."""
        scores = [
            logical_validation.get("score", 0.0),
            factual_validation.get("score", 0.0),
            consistency_validation.get("score", 0.0)
        ]
        
        overall_score = sum(scores) / len(scores)
        is_valid = overall_score > 0.7
        
        issues = []
        issues.extend(logical_validation.get("issues", []))
        issues.extend(factual_validation.get("claims", []))
        issues.extend(consistency_validation.get("issues", []))
        
        return {
            "is_valid": is_valid,
            "confidence": overall_score,
            "overall_score": overall_score,
            "logical_score": logical_validation.get("score", 0.0),
            "factual_score": factual_validation.get("score", 0.0),
            "consistency_score": consistency_validation.get("score", 0.0),
            "issues": issues,
            "reasoning": f"Overall validation score: {overall_score:.2f}"
        }


class AIAgentService:
    """Main service for managing AI agents."""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.sessions: Dict[str, Dict] = {}
        self.metrics_service = ReasoningMetricsService()
        
        # Initialize agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all AI agents."""
        # Create specialized agents
        reasoning_agent = ReasoningAgent("reasoning_001")
        knowledge_agent = KnowledgeAgent("knowledge_001")
        validation_agent = ValidationAgent("validation_001")
        
        # Store agents
        self.agents["reasoning_001"] = reasoning_agent
        self.agents["knowledge_001"] = knowledge_agent
        self.agents["validation_001"] = validation_agent
    
    async def create_session(self, user_id: Optional[str] = None, domain: Optional[str] = None) -> str:
        """Create a new agent session."""
        session_id = str(uuid.uuid4())
        
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "domain": domain,
            "created_at": datetime.now(),
            "status": "active",
            "task_count": 0,
            "last_activity": datetime.now()
        }
        
        self.sessions[session_id] = session
        return session_id
    
    async def process_with_agents(
        self, 
        session_id: str, 
        input_data: Any, 
        agent_types: Optional[List[AgentType]] = None,
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> AgentResult:
        """Process input using AI agents."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # Create context
        context = AgentContext(
            session_id=session_id,
            user_id=session.get("user_id"),
            domain=session.get("domain"),
            priority=priority
        )
        
        # Determine which agents to use
        if agent_types:
            available_agents = [
                agent for agent in self.agents.values()
                if agent.agent_type in agent_types
            ]
        else:
            # Use reasoning agent by default
            available_agents = [self.agents["reasoning_001"]]
        
        if not available_agents:
            raise RuntimeError("No suitable agents available")
        
        # Use the first available agent
        agent = available_agents[0]
        result = await agent.think(context, input_data)
        
        # Update session
        session["last_activity"] = datetime.now()
        session["task_count"] += 1
        
        # Record metrics
        self.metrics_service.record_agent_usage(
            session_id=session_id,
            agent_types=[agent.agent_type.value],
            success=result.success,
            response_time=result.metadata.get("response_time", 0.0)
        )
        
        return result
    
    async def get_agent_status(self, agent_id: str) -> AgentStatusResponse:
        """Get status of a specific agent."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        agent = self.agents[agent_id]
        return AgentStatusResponse(
            agent_id=agent.agent_id,
            agent_type=agent.agent_type,
            state=agent.state,
            capabilities=agent.capabilities,
            performance_metrics=agent.performance_metrics,
            last_activity=datetime.now()  # TODO: Track actual last activity
        )
    
    async def get_all_agents_status(self) -> List[AgentStatusResponse]:
        """Get status of all agents."""
        return [
            await self.get_agent_status(agent_id)
            for agent_id in self.agents.keys()
        ]
    
    async def get_session_info(self, session_id: str) -> Dict:
        """Get information about a session."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        return {
            "session_id": session["session_id"],
            "user_id": session.get("user_id"),
            "domain": session.get("domain"),
            "created_at": session["created_at"].isoformat(),
            "last_activity": session["last_activity"].isoformat(),
            "status": session["status"],
            "task_count": session["task_count"]
        }
    
    async def get_system_status(self) -> AgentSystemStatus:
        """Get overall system status."""
        agent_statuses = await self.get_all_agents_status()
        
        total_agents = len(self.agents)
        active_agents = sum(1 for status in agent_statuses if status.state != AgentState.ERROR)
        total_sessions = len(self.sessions)
        active_sessions = sum(1 for session in self.sessions.values() if session["status"] == "active")
        
        # Calculate performance metrics
        total_tasks = sum(session["task_count"] for session in self.sessions.values())
        avg_processing_time = sum(
            agent.performance_metrics["avg_response_time"] 
            for agent in self.agents.values()
        ) / max(len(self.agents), 1)
        
        return AgentSystemStatus(
            total_agents=total_agents,
            active_agents=active_agents,
            total_sessions=total_sessions,
            active_sessions=active_sessions,
            total_tasks=total_tasks,
            completed_tasks=total_tasks,  # Simplified
            failed_tasks=0,  # TODO: Track failed tasks
            avg_processing_time=avg_processing_time,
            system_health="healthy" if active_agents == total_agents else "degraded",
            agent_statuses=agent_statuses,
            performance_metrics=[]  # TODO: Add detailed performance metrics
        )


# Global instance
ai_agent_service = AIAgentService()
