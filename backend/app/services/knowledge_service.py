"""
Knowledge Service for fact storage and verification.
"""

import json
from typing import Dict, Any, Optional, List, Set
import networkx as nx
from app.models.reasoning import ReasoningTrace, ReasoningStage, KnowledgeFact


class KnowledgeService:
    """Service for knowledge graph and fact verification."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.facts: Dict[str, KnowledgeFact] = {}
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with domain-specific facts."""
        
        # Healthcare/HIPAA facts
        healthcare_facts = [
            KnowledgeFact(
                subject="HIPAA_164_312_a_1",
                predicate="requires",
                object="access_control_mechanisms",
                confidence=1.0,
                source="HIPAA_Regulation"
            ),
            KnowledgeFact(
                subject="HIPAA_164_312_a_1",
                predicate="applies_to",
                object="electronic_protected_health_information",
                confidence=1.0,
                source="HIPAA_Regulation"
            ),
            KnowledgeFact(
                subject="access_control_mechanisms",
                predicate="includes",
                object="authentication",
                confidence=0.9,
                source="HIPAA_Guidance"
            ),
            KnowledgeFact(
                subject="access_control_mechanisms",
                predicate="includes",
                object="authorization",
                confidence=0.9,
                source="HIPAA_Guidance"
            ),
            KnowledgeFact(
                subject="HIPAA_164_312_c_1",
                predicate="requires",
                object="data_integrity_protection",
                confidence=1.0,
                source="HIPAA_Regulation"
            ),
            KnowledgeFact(
                subject="data_integrity_protection",
                predicate="prevents",
                object="unauthorized_alteration",
                confidence=0.9,
                source="HIPAA_Guidance"
            ),
            KnowledgeFact(
                subject="HIPAA_164_312_d",
                predicate="requires",
                object="entity_authentication",
                confidence=1.0,
                source="HIPAA_Regulation"
            )
        ]
        
        # Finance facts
        finance_facts = [
            KnowledgeFact(
                subject="debt_to_equity_ratio",
                predicate="formula",
                object="total_debt / total_equity",
                confidence=1.0,
                source="Financial_Accounting"
            ),
            KnowledgeFact(
                subject="current_ratio",
                predicate="formula",
                object="current_assets / current_liabilities",
                confidence=1.0,
                source="Financial_Accounting"
            ),
            KnowledgeFact(
                subject="roi",
                predicate="formula",
                object="(gain - cost) / cost * 100",
                confidence=1.0,
                source="Financial_Accounting"
            ),
            KnowledgeFact(
                subject="debt_to_equity_ratio",
                predicate="healthy_range",
                object="0.5_to_2.0",
                confidence=0.8,
                source="Financial_Analysis"
            ),
            KnowledgeFact(
                subject="current_ratio",
                predicate="healthy_range",
                object="1.5_to_3.0",
                confidence=0.8,
                source="Financial_Analysis"
            )
        ]
        
        # General facts
        general_facts = [
            KnowledgeFact(
                subject="mathematical_consistency",
                predicate="requires",
                object="logical_equivalence",
                confidence=1.0,
                source="Logic"
            ),
            KnowledgeFact(
                subject="logical_consistency",
                predicate="excludes",
                object="contradictions",
                confidence=1.0,
                source="Logic"
            )
        ]
        
        # Add all facts to the knowledge base
        all_facts = healthcare_facts + finance_facts + general_facts
        
        for fact in all_facts:
            self.add_fact(fact)
    
    def add_fact(self, fact: KnowledgeFact):
        """Add a fact to the knowledge base."""
        fact_id = f"{fact.subject}_{fact.predicate}_{fact.object}"
        self.facts[fact_id] = fact
        
        # Add to graph
        self.graph.add_node(fact.subject, type="entity")
        self.graph.add_node(fact.object, type="entity")
        self.graph.add_edge(fact.subject, fact.object, predicate=fact.predicate, confidence=fact.confidence)
    
    def query_facts(
        self, 
        subject: Optional[str] = None, 
        predicate: Optional[str] = None, 
        object: Optional[str] = None
    ) -> List[KnowledgeFact]:
        """Query facts from the knowledge base."""
        results = []
        
        for fact in self.facts.values():
            if subject and fact.subject != subject:
                continue
            if predicate and fact.predicate != predicate:
                continue
            if object and fact.object != object:
                continue
            results.append(fact)
        
        return results
    
    def verify_hypothesis(
        self, 
        hypothesis: str, 
        question: str, 
        domain: Optional[str] = None
    ) -> ReasoningTrace:
        """
        Verify hypothesis against knowledge base.
        
        Args:
            hypothesis: LLM-generated hypothesis
            question: Original question
            domain: Domain context
            
        Returns:
            ReasoningTrace with verification results
        """
        
        # Extract key concepts from hypothesis and question
        concepts = self._extract_concepts(f"{question} {hypothesis}")
        
        # Find relevant facts
        relevant_facts = []
        verification_results = []
        
        for concept in concepts:
            facts = self.query_facts(subject=concept)
            facts.extend(self.query_facts(object=concept))
            
            for fact in facts:
                if fact not in relevant_facts:
                    relevant_facts.append(fact)
        
        # Verify against facts
        for fact in relevant_facts:
            verification = self._verify_against_fact(hypothesis, fact)
            verification_results.append(verification)
        
        # Calculate overall confidence
        if verification_results:
            confidence = sum(r["confidence"] for r in verification_results) / len(verification_results)
        else:
            confidence = 0.5
        
        # Generate output
        output = f"Verified hypothesis against {len(relevant_facts)} relevant facts.\n\n"
        
        if relevant_facts:
            output += "Relevant facts found:\n"
            for fact in relevant_facts:
                output += f"- {fact.subject} {fact.predicate} {fact.object} (confidence: {fact.confidence})\n"
        
        if verification_results:
            output += "\nVerification results:\n"
            for result in verification_results:
                status = "PASS" if result["verified"] else "FAIL"
                output += f"- {result['fact'].subject} {result['fact'].predicate} {result['fact'].object}: {status}\n"
        
        return ReasoningTrace(
            stage=ReasoningStage.KNOWLEDGE_GRAPH,
            output=output,
            confidence=confidence,
            metadata={
                "domain": domain,
                "facts_checked": len(relevant_facts),
                "verification_results": verification_results
            }
        )
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text."""
        # Simple concept extraction - in a real system, this would be more sophisticated
        concepts = []
        
        # Extract domain-specific terms
        healthcare_terms = [
            "hipaa", "access_control", "authentication", "authorization", 
            "integrity", "electronic", "protected_health_information", "phi"
        ]
        
        finance_terms = [
            "debt", "equity", "ratio", "assets", "liabilities", "roi", 
            "return_on_investment", "current_ratio"
        ]
        
        text_lower = text.lower()
        
        for term in healthcare_terms + finance_terms:
            if term in text_lower:
                concepts.append(term)
        
        return concepts
    
    def _verify_against_fact(self, hypothesis: str, fact: KnowledgeFact) -> Dict[str, Any]:
        """Verify hypothesis against a specific fact."""
        hypothesis_lower = hypothesis.lower()
        
        # Check if the fact's components are mentioned in the hypothesis
        subject_mentioned = fact.subject.lower() in hypothesis_lower
        predicate_mentioned = fact.predicate.lower() in hypothesis_lower
        object_mentioned = fact.object.lower() in hypothesis_lower
        
        # Simple verification logic
        if subject_mentioned and predicate_mentioned and object_mentioned:
            verified = True
            confidence = fact.confidence
        elif subject_mentioned and (predicate_mentioned or object_mentioned):
            verified = True
            confidence = fact.confidence * 0.8
        else:
            verified = False
            confidence = 0.3
        
        return {
            "fact": fact,
            "verified": verified,
            "confidence": confidence,
            "subject_mentioned": subject_mentioned,
            "predicate_mentioned": predicate_mentioned,
            "object_mentioned": object_mentioned
        }
    
    def get_knowledge_summary(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """Get a summary of the knowledge base."""
        if domain:
            # Filter facts by domain
            domain_facts = []
            for fact in self.facts.values():
                if domain in fact.subject.lower() or domain in fact.object.lower():
                    domain_facts.append(fact)
            facts = domain_facts
        else:
            facts = list(self.facts.values())
        
        return {
            "total_facts": len(facts),
            "domains": self._get_domains(),
            "graph_nodes": self.graph.number_of_nodes(),
            "graph_edges": self.graph.number_of_edges()
        }
    
    def _get_domains(self) -> List[str]:
        """Get list of domains in the knowledge base."""
        domains = set()
        
        for fact in self.facts.values():
            if "hipaa" in fact.subject.lower() or "hipaa" in fact.object.lower():
                domains.add("healthcare")
            elif any(term in fact.subject.lower() or term in fact.object.lower() 
                    for term in ["debt", "equity", "ratio", "roi"]):
                domains.add("finance")
            else:
                domains.add("general")
        
        return list(domains)
