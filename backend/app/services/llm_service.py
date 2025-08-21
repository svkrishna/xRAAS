"""
LLM Service for System 1 reasoning (intuitive, fast reasoning).
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.reasoning import ReasoningTrace, ReasoningStage


class LLMService:
    """Service for LLM-based reasoning."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def generate_hypothesis(
        self, 
        question: str, 
        context: Optional[str] = None,
        domain: Optional[str] = None
    ) -> ReasoningTrace:
        """
        Generate an initial hypothesis using the LLM.
        
        Args:
            question: The question to reason about
            context: Additional context
            domain: Domain context (e.g., 'healthcare', 'finance')
            
        Returns:
            ReasoningTrace with the LLM hypothesis
        """
        
        # Build the prompt based on domain
        if domain == "healthcare":
            system_prompt = self._get_healthcare_prompt()
        elif domain == "finance":
            system_prompt = self._get_finance_prompt()
        else:
            system_prompt = self._get_general_prompt()
        
        # Build user message
        user_message = f"Question: {question}"
        if context:
            user_message += f"\nContext: {context}"
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            hypothesis = response.choices[0].message.content
            
            return ReasoningTrace(
                stage=ReasoningStage.LLM_HYPOTHESIS,
                output=hypothesis,
                confidence=0.8,  # Default confidence for LLM
                metadata={
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens,
                    "domain": domain
                }
            )
            
        except Exception as e:
            return ReasoningTrace(
                stage=ReasoningStage.LLM_HYPOTHESIS,
                output=f"Error generating hypothesis: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    def _get_general_prompt(self) -> str:
        """Get general reasoning prompt."""
        return """
        You are an AI reasoning assistant. Your task is to provide a clear, logical hypothesis 
        for the given question. Focus on:
        1. Understanding the core question
        2. Identifying key factors to consider
        3. Providing a reasoned hypothesis
        4. Acknowledging any uncertainties
        
        Be concise but thorough in your reasoning.
        """
    
    def _get_healthcare_prompt(self) -> str:
        """Get healthcare-specific reasoning prompt."""
        return """
        You are a healthcare compliance reasoning assistant. Your task is to analyze 
        healthcare-related questions, particularly focusing on:
        1. HIPAA compliance requirements
        2. Patient privacy and security
        3. Healthcare regulations and standards
        4. Risk assessment and mitigation
        
        Provide a reasoned hypothesis while being careful about medical advice limitations.
        """
    
    def _get_finance_prompt(self) -> str:
        """Get finance-specific reasoning prompt."""
        return """
        You are a financial reasoning assistant. Your task is to analyze financial questions, 
        focusing on:
        1. Mathematical accuracy in calculations
        2. Financial ratios and metrics
        3. Risk assessment
        4. Regulatory compliance
        
        Provide precise, mathematically sound reasoning.
        """
    
    async def validate_answer(
        self, 
        question: str, 
        answer: str, 
        domain: Optional[str] = None
    ) -> ReasoningTrace:
        """
        Validate an answer using the LLM.
        
        Args:
            question: Original question
            answer: Answer to validate
            domain: Domain context
            
        Returns:
            ReasoningTrace with validation result
        """
        
        validation_prompt = f"""
        Please validate the following answer for the given question:
        
        Question: {question}
        Answer: {answer}
        
        Provide a validation assessment including:
        1. Logical consistency
        2. Completeness
        3. Accuracy
        4. Confidence level (0-1)
        
        Respond in JSON format:
        {{
            "is_valid": true/false,
            "confidence": 0.85,
            "issues": ["list of any issues"],
            "reasoning": "explanation of validation"
        }}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a validation assistant. Respond only in valid JSON."},
                    {"role": "user", "content": validation_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            validation_result = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                parsed_result = json.loads(validation_result)
                confidence = parsed_result.get("confidence", 0.5)
                reasoning = parsed_result.get("reasoning", validation_result)
            except json.JSONDecodeError:
                confidence = 0.5
                reasoning = validation_result
            
            return ReasoningTrace(
                stage=ReasoningStage.VALIDATION,
                output=reasoning,
                confidence=confidence,
                metadata={
                    "model": self.model,
                    "validation_result": validation_result
                }
            )
            
        except Exception as e:
            return ReasoningTrace(
                stage=ReasoningStage.VALIDATION,
                output=f"Error during validation: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def generate(self, prompt: str) -> str:
        """
        Generate a response for a given prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            Generated response as string
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant. Respond in the requested format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
