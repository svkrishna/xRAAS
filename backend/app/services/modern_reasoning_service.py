"""
Modern Reasoning Service
State-of-the-art reasoning combining LLM validation with graph-based reasoning.
"""

import re
import json
import uuid
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging
import networkx as nx
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of LLM-based validation."""
    validation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_valid: bool = False
    confidence: float = 0.0
    reasoning: str = ""
    evidence: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    compliance_status: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0


@dataclass
class GraphNode:
    """A node in the knowledge graph."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    label: str = ""
    node_type: str = ""  # entity, concept, rule, regulation
    properties: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


@dataclass
class GraphEdge:
    """An edge in the knowledge graph."""
    source: str = ""
    target: str = ""
    relationship: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


class KnowledgeGraph:
    """Modern knowledge graph for reasoning."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, GraphEdge] = {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize with domain knowledge
        self._initialize_domain_knowledge()
    
    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph."""
        self.nodes[node.id] = node
        self.graph.add_node(node.id, **node.properties)
        self.logger.info(f"Added node: {node.label} ({node.id})")
    
    def add_edge(self, edge: GraphEdge) -> None:
        """Add an edge to the graph."""
        edge_id = f"{edge.source}->{edge.target}:{edge.relationship}"
        self.edges[edge_id] = edge
        self.graph.add_edge(edge.source, edge.target, 
                           relationship=edge.relationship, **edge.properties)
    
    def query(self, subject: str, predicate: str = None) -> List[Tuple[str, str, Dict[str, Any]]]:
        """Query the graph for relationships."""
        results = []
        
        # Find node by label
        subject_node_id = None
        for node_id, node in self.nodes.items():
            if node.label == subject:
                subject_node_id = node_id
                break
        
        if not subject_node_id:
            return results
        
        if predicate:
            # Find specific relationships
            for source, target, data in self.graph.edges(data=True):
                if source == subject_node_id and data.get('relationship') == predicate:
                    results.append((source, target, data))
        else:
            # Find all relationships from subject
            for source, target, data in self.graph.edges(data=True):
                if source == subject_node_id:
                    results.append((source, target, data))
        
        return results
    
    def find_path(self, source: str, target: str, max_length: int = 3) -> List[str]:
        """Find path between two nodes."""
        try:
            # Find node IDs by labels
            source_id = None
            target_id = None
            
            for node_id, node in self.nodes.items():
                if node.label == source:
                    source_id = node_id
                elif node.label == target:
                    target_id = node_id
            
            if not source_id or not target_id:
                return []
            
            path = nx.shortest_path(self.graph, source_id, target_id)
            return path if len(path) <= max_length else []
        except nx.NetworkXNoPath:
            return []
    
    def get_related_concepts(self, concept: str, max_depth: int = 2) -> List[str]:
        """Get related concepts up to a certain depth."""
        related = set()
        visited = set()
        
        # Find node ID by label
        concept_id = None
        for node_id, node in self.nodes.items():
            if node.label == concept:
                concept_id = node_id
                break
        
        if not concept_id:
            return []
        
        def dfs(node_id: str, depth: int):
            if depth > max_depth or node_id in visited:
                return
            visited.add(node_id)
            related.add(node_id)
            
            for neighbor in self.graph.neighbors(node_id):
                dfs(neighbor, depth + 1)
        
        dfs(concept_id, 0)
        return list(related - {concept_id})
    
    def _initialize_domain_knowledge(self):
        """Initialize the graph with domain-specific knowledge."""
        
        # HIPAA Knowledge
        hipaa_node = GraphNode(label="HIPAA", node_type="regulation")
        self.add_node(hipaa_node)
        
        access_control = GraphNode(label="Access Control", node_type="requirement")
        self.add_node(access_control)
        
        authentication = GraphNode(label="Authentication", node_type="requirement")
        self.add_node(authentication)
        
        phi = GraphNode(label="Protected Health Information", node_type="concept")
        self.add_node(phi)
        
        # Add relationships using node IDs
        self.add_edge(GraphEdge(
            source=hipaa_node.id,
            target=access_control.id,
            relationship="requires"
        ))
        
        self.add_edge(GraphEdge(
            source=hipaa_node.id,
            target=authentication.id,
            relationship="requires"
        ))
        
        self.add_edge(GraphEdge(
            source=access_control.id,
            target=phi.id,
            relationship="protects"
        ))
        
        # Financial Knowledge
        financial_metrics = GraphNode(label="Financial Metrics", node_type="concept")
        self.add_node(financial_metrics)
        
        debt_equity = GraphNode(label="Debt-to-Equity Ratio", node_type="metric")
        self.add_node(debt_equity)
        
        current_ratio = GraphNode(label="Current Ratio", node_type="metric")
        self.add_node(current_ratio)
        
        self.add_edge(GraphEdge(
            source=financial_metrics.id,
            target=debt_equity.id,
            relationship="includes"
        ))
        
        self.add_edge(GraphEdge(
            source=financial_metrics.id,
            target=current_ratio.id,
            relationship="includes"
        ))


class LLMValidator:
    """LLM-based validation service."""
    
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.logger = logging.getLogger(__name__)
    
    async def validate_hipaa_compliance(self, text: str) -> ValidationResult:
        """Validate HIPAA compliance using LLM."""
        start_time = datetime.utcnow()
        
        prompt = f"""
        Analyze the following text for HIPAA compliance:

        TEXT: "{text}"

        Evaluate compliance with these key HIPAA requirements:
        1. Access Control (164.312(a)(1)) - Technical policies for electronic PHI access
        2. Integrity (164.312(c)(1)) - Protection from improper alteration/destruction  
        3. Authentication (164.312(d)) - Verification of person/entity identity
        4. Transmission Security (164.312(e)(1)) - Encryption of electronic PHI

        Return a JSON response with this structure:
        {{
            "is_compliant": boolean,
            "confidence": float (0-1),
            "reasoning": "detailed explanation",
            "evidence": ["list of supporting evidence"],
            "recommendations": ["list of improvement suggestions"],
            "compliance_details": {{
                "access_control": {{"compliant": boolean, "details": "string"}},
                "integrity": {{"compliant": boolean, "details": "string"}},
                "authentication": {{"compliant": boolean, "details": "string"}},
                "transmission_security": {{"compliant": boolean, "details": "string"}}
            }}
        }}
        """
        
        try:
            response = await self.llm_service.generate(prompt)
            result_data = json.loads(response)
            
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            return ValidationResult(
                is_valid=result_data.get("is_compliant", False),
                confidence=result_data.get("confidence", 0.0),
                reasoning=result_data.get("reasoning", ""),
                evidence=result_data.get("evidence", []),
                recommendations=result_data.get("recommendations", []),
                compliance_status=result_data.get("compliance_details", {}),
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            self.logger.error(f"Error in HIPAA validation: {e}")
            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                reasoning=f"Validation failed: {str(e)}",
                execution_time_ms=(datetime.utcnow() - start_time).total_seconds() * 1000
            )
    
    async def validate_financial_calculations(self, text: str) -> ValidationResult:
        """Validate financial calculations using LLM."""
        start_time = datetime.utcnow()
        
        prompt = f"""
        Analyze the following text for financial calculation accuracy:

        TEXT: "{text}"

        Check for:
        1. Mathematical accuracy of calculations
        2. Proper use of financial formulas
        3. Logical consistency of financial statements
        4. Appropriate financial metrics and ratios

        Return a JSON response with this structure:
        {{
            "is_valid": boolean,
            "confidence": float (0-1),
            "reasoning": "detailed explanation",
            "evidence": ["list of supporting evidence"],
            "recommendations": ["list of improvement suggestions"],
            "calculations": [
                {{
                    "formula": "formula used",
                    "result": "calculated result",
                    "is_correct": boolean,
                    "explanation": "why correct/incorrect"
                }}
            ]
        }}
        """
        
        try:
            response = await self.llm_service.generate(prompt)
            result_data = json.loads(response)
            
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            return ValidationResult(
                is_valid=result_data.get("is_valid", False),
                confidence=result_data.get("confidence", 0.0),
                reasoning=result_data.get("reasoning", ""),
                evidence=result_data.get("evidence", []),
                recommendations=result_data.get("recommendations", []),
                compliance_status={"calculations": result_data.get("calculations", [])},
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            self.logger.error(f"Error in financial validation: {e}")
            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                reasoning=f"Validation failed: {str(e)}",
                execution_time_ms=(datetime.utcnow() - start_time).total_seconds() * 1000
            )
    
    async def validate_logical_consistency(self, statements: List[str]) -> ValidationResult:
        """Validate logical consistency using LLM."""
        start_time = datetime.utcnow()
        
        statements_text = "\n".join([f"{i+1}. {stmt}" for i, stmt in enumerate(statements)])
        
        prompt = f"""
        Analyze the following statements for logical consistency:

        STATEMENTS:
        {statements_text}

        Check for:
        1. Direct contradictions between statements
        2. Logical inconsistencies
        3. Circular reasoning
        4. Unsupported assumptions

        Return a JSON response with this structure:
        {{
            "is_consistent": boolean,
            "confidence": float (0-1),
            "reasoning": "detailed explanation",
            "contradictions": ["list of contradictions found"],
            "inconsistencies": ["list of logical inconsistencies"],
            "recommendations": ["list of improvement suggestions"]
        }}
        """
        
        try:
            response = await self.llm_service.generate(prompt)
            result_data = json.loads(response)
            
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            return ValidationResult(
                is_valid=result_data.get("is_consistent", False),
                confidence=result_data.get("confidence", 0.0),
                reasoning=result_data.get("reasoning", ""),
                evidence=result_data.get("contradictions", []) + result_data.get("inconsistencies", []),
                recommendations=result_data.get("recommendations", []),
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            self.logger.error(f"Error in logical validation: {e}")
            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                reasoning=f"Validation failed: {str(e)}",
                execution_time_ms=(datetime.utcnow() - start_time).total_seconds() * 1000
            )


class ModernReasoningService:
    """Modern reasoning service combining LLM validation with graph reasoning."""
    
    def __init__(self, llm_service):
        self.llm_validator = LLMValidator(llm_service)
        self.knowledge_graph = KnowledgeGraph()
        self.logger = logging.getLogger(__name__)
    
    async def reason_about_text(self, text: str, domain: str = "general") -> Dict[str, Any]:
        """Apply modern reasoning to text."""
        results = {
            "text": text,
            "domain": domain,
            "validation_results": {},
            "graph_insights": {},
            "overall_confidence": 0.0,
            "recommendations": []
        }
        
        # LLM-based validation
        if domain == "healthcare":
            results["validation_results"]["hipaa"] = await self.llm_validator.validate_hipaa_compliance(text)
        elif domain == "finance":
            results["validation_results"]["financial"] = await self.llm_validator.validate_financial_calculations(text)
        else:
            # General logical consistency
            statements = [s.strip() for s in text.split('.') if s.strip()]
            if len(statements) > 1:
                results["validation_results"]["logical"] = await self.llm_validator.validate_logical_consistency(statements)
        
        # Graph-based insights
        results["graph_insights"] = self._extract_graph_insights(text, domain)
        
        # Calculate overall confidence
        validations = list(results["validation_results"].values())
        if validations:
            results["overall_confidence"] = sum(v.confidence for v in validations) / len(validations)
        
        # Collect recommendations
        for validation in validations:
            results["recommendations"].extend(validation.recommendations)
        
        return results
    
    def _extract_graph_insights(self, text: str, domain: str) -> Dict[str, Any]:
        """Extract insights using the knowledge graph."""
        insights = {
            "related_concepts": [],
            "compliance_paths": [],
            "knowledge_gaps": []
        }
        
        # Extract key terms from text
        terms = self._extract_terms(text)
        
        # Find related concepts
        for term in terms:
            related = self.knowledge_graph.get_related_concepts(term)
            insights["related_concepts"].extend(related)
        
        # Find compliance paths for healthcare
        if domain == "healthcare":
            for term in terms:
                if "hipaa" in term.lower():
                    paths = self.knowledge_graph.find_path("HIPAA", term)
                    if paths:
                        insights["compliance_paths"].append(paths)
        
        return insights
    
    def _extract_terms(self, text: str) -> List[str]:
        """Extract key terms from text."""
        # Simple term extraction - could be enhanced with NLP
        terms = []
        if not text:
            return terms
            
        text_lower = text.lower()
        
        # Look for domain-specific terms
        if "hipaa" in text_lower or "health" in text_lower:
            terms.extend(["HIPAA", "healthcare"])
        
        if "debt" in text_lower or "equity" in text_lower or "ratio" in text_lower:
            terms.extend(["financial", "metrics"])
        
        return list(set(terms))
    
    async def validate_compliance(self, text: str, regulation: str) -> ValidationResult:
        """Validate compliance with specific regulations."""
        if regulation.lower() == "hipaa":
            return await self.llm_validator.validate_hipaa_compliance(text)
        elif regulation.lower() == "financial":
            return await self.llm_validator.validate_financial_calculations(text)
        else:
            # Generic validation
            statements = [s.strip() for s in text.split('.') if s.strip()]
            return await self.llm_validator.validate_logical_consistency(statements)
    
    def add_knowledge(self, subject: str, predicate: str, object: str, confidence: float = 1.0):
        """Add knowledge to the graph."""
        # Create nodes if they don't exist
        if subject not in self.knowledge_graph.nodes:
            subject_node = GraphNode(label=subject, node_type="concept")
            self.knowledge_graph.add_node(subject_node)
        
        if object not in self.knowledge_graph.nodes:
            object_node = GraphNode(label=object, node_type="concept")
            self.knowledge_graph.add_node(object_node)
        
        # Add relationship
        edge = GraphEdge(
            source=subject,
            target=object,
            relationship=predicate,
            confidence=confidence
        )
        self.knowledge_graph.add_edge(edge)
    
    def query_knowledge(self, query: str) -> List[Tuple[str, str, str]]:
        """Query the knowledge graph."""
        # Simple query parsing - could be enhanced with NLP
        if "->" in query:
            parts = query.split("->")
            if len(parts) == 2:
                subject = parts[0].strip()
                predicate = parts[1].strip()
                return self.knowledge_graph.query(subject, predicate)
        
        return self.knowledge_graph.query(query)


# Factory function to create the service
def create_modern_reasoning_service(llm_service) -> ModernReasoningService:
    """Create a modern reasoning service instance."""
    return ModernReasoningService(llm_service)
