"""
Orchestration Service for coordinating the reasoning pipeline.
"""

import asyncio
import time
import uuid
from typing import List, Dict, Any, Optional
from app.models.reasoning import (
    ReasoningRequest, 
    ReasoningResponse, 
    ReasoningTrace, 
    ReasoningStage,
    ReasoningSession
)
from app.services.llm_service import LLMService
from app.services.modern_reasoning_service import create_modern_reasoning_service
from app.services.knowledge_service import KnowledgeService
from app.core.config import settings


class OrchestrationService:
    """Service for orchestrating the reasoning pipeline."""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.symbolic_service = create_modern_reasoning_service(self.llm_service)
        self.knowledge_service = KnowledgeService()
    
    async def reason(
        self, 
        request: ReasoningRequest
    ) -> ReasoningResponse:
        """
        Execute the complete reasoning pipeline.
        
        Args:
            request: Reasoning request
            
        Returns:
            ReasoningResponse with answer and trace
        """
        
        start_time = time.time()
        reasoning_trace: List[ReasoningTrace] = []
        
        try:
            # Step 1: Generate LLM hypothesis (System 1)
            llm_trace = await self.llm_service.generate_hypothesis(
                question=request.question,
                context=request.context,
                domain=request.domain
            )
            reasoning_trace.append(llm_trace)
            
            # Step 2: Apply symbolic rules (System 2)
            symbolic_trace = await self.symbolic_service.apply_rules(
                hypothesis=llm_trace.output,
                question=request.question,
                domain=request.domain
            )
            reasoning_trace.append(symbolic_trace)
            
            # Step 3: Verify against knowledge base
            knowledge_trace = await self.knowledge_service.verify_hypothesis(
                hypothesis=llm_trace.output,
                question=request.question,
                domain=request.domain
            )
            reasoning_trace.append(knowledge_trace)
            
            # Step 4: Generate final answer
            final_answer = await self._generate_final_answer(
                llm_hypothesis=llm_trace.output,
                symbolic_result=symbolic_trace.output,
                knowledge_result=knowledge_trace.output,
                question=request.question,
                domain=request.domain
            )
            
            # Step 5: Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(reasoning_trace)
            
            # Step 6: Validate final answer
            validation_trace = await self.llm_service.validate_answer(
                question=request.question,
                answer=final_answer,
                domain=request.domain
            )
            reasoning_trace.append(validation_trace)
            
            processing_time = time.time() - start_time
            
            return ReasoningResponse(
                answer=final_answer,
                reasoning_trace=reasoning_trace,
                confidence=overall_confidence,
                domain=request.domain,
                metadata={
                    "processing_time": processing_time,
                    "session_id": str(uuid.uuid4()),
                    "steps_completed": len(reasoning_trace)
                }
            )
            
        except Exception as e:
            # Handle errors gracefully
            error_trace = ReasoningTrace(
                stage=ReasoningStage.FINAL_ANSWER,
                output=f"Error in reasoning pipeline: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )
            reasoning_trace.append(error_trace)
            
            return ReasoningResponse(
                answer=f"Error occurred during reasoning: {str(e)}",
                reasoning_trace=reasoning_trace,
                confidence=0.0,
                domain=request.domain,
                metadata={"error": str(e)}
            )
    
    async def _generate_final_answer(
        self,
        llm_hypothesis: str,
        symbolic_result: str,
        knowledge_result: str,
        question: str,
        domain: Optional[str] = None
    ) -> str:
        """
        Generate the final answer based on all reasoning steps.
        
        Args:
            llm_hypothesis: LLM-generated hypothesis
            symbolic_result: Symbolic rule check results
            knowledge_result: Knowledge base verification results
            question: Original question
            domain: Domain context
            
        Returns:
            Final synthesized answer
        """
        
        # Create a synthesis prompt
        synthesis_prompt = f"""
        Based on the following reasoning steps, provide a clear, final answer to the question.
        
        Question: {question}
        
        Reasoning Steps:
        1. LLM Hypothesis: {llm_hypothesis}
        2. Symbolic Rule Check: {symbolic_result}
        3. Knowledge Base Verification: {knowledge_result}
        
        Please synthesize these results into a clear, confident answer. If there are any 
        contradictions or low confidence indicators, acknowledge them in your response.
        
        Domain: {domain or 'general'}
        """
        
        try:
            response = await self.llm_service.client.chat.completions.create(
                model=self.llm_service.model,
                messages=[
                    {"role": "system", "content": "You are a reasoning synthesis assistant. Provide clear, accurate final answers."},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Fallback to simple synthesis
            return f"Based on the analysis: {llm_hypothesis}\n\nRule check results: {symbolic_result}\n\nKnowledge verification: {knowledge_result}"
    
    def _calculate_overall_confidence(self, reasoning_trace: List[ReasoningTrace]) -> float:
        """
        Calculate overall confidence based on all reasoning steps.
        
        Args:
            reasoning_trace: List of reasoning traces
            
        Returns:
            Overall confidence score (0-1)
        """
        
        if not reasoning_trace:
            return 0.0
        
        # Weight different stages differently
        weights = {
            ReasoningStage.LLM_HYPOTHESIS: 0.4,
            ReasoningStage.RULE_CHECK: 0.3,
            ReasoningStage.KNOWLEDGE_GRAPH: 0.2,
            ReasoningStage.VALIDATION: 0.1
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for trace in reasoning_trace:
            weight = weights.get(trace.stage, 0.1)
            confidence = trace.confidence or 0.5
            
            weighted_sum += weight * confidence
            total_weight += weight
        
        if total_weight == 0:
            return 0.5
        
        return weighted_sum / total_weight
    
    async def get_reasoning_summary(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a summary of the reasoning capabilities.
        
        Args:
            domain: Optional domain filter
            
        Returns:
            Summary of reasoning capabilities
        """
        
        return {
            "llm_model": self.llm_service.model,
            "available_rule_sets": list(self.symbolic_service.rule_sets.keys()),
            "knowledge_summary": self.knowledge_service.get_knowledge_summary(domain),
            "max_reasoning_steps": settings.max_reasoning_steps,
            "confidence_threshold": settings.default_confidence_threshold
        }
    
    async def validate_request(self, request: ReasoningRequest) -> Dict[str, Any]:
        """
        Validate a reasoning request.
        
        Args:
            request: Reasoning request to validate
            
        Returns:
            Validation results
        """
        
        validation_results = {
            "valid": True,
            "issues": [],
            "warnings": []
        }
        
        # Check question length
        if len(request.question) < 10:
            validation_results["warnings"].append("Question is quite short")
        
        if len(request.question) > 1000:
            validation_results["issues"].append("Question is too long (max 1000 characters)")
            validation_results["valid"] = False
        
        # Check domain
        if request.domain and request.domain not in self.symbolic_service.rule_sets:
            validation_results["warnings"].append(f"Domain '{request.domain}' not recognized")
        
        # Check confidence threshold
        if request.confidence_threshold and (request.confidence_threshold < 0 or request.confidence_threshold > 1):
            validation_results["issues"].append("Confidence threshold must be between 0 and 1")
            validation_results["valid"] = False
        
        # Check max steps
        if request.max_steps and request.max_steps > settings.max_reasoning_steps:
            validation_results["warnings"].append(f"Max steps reduced to {settings.max_reasoning_steps}")
            request.max_steps = settings.max_reasoning_steps
        
        return validation_results
