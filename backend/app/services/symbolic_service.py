"""
Symbolic Reasoning Service
Python-based rule engine for symbolic logic and validation.
"""

import re
import uuid
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Global flag for rule engine availability (always True for Python-based engine)
RULE_ENGINE_AVAILABLE = True


@dataclass
class Rule:
    """A rule for symbolic reasoning."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    condition: Callable = None
    action: Callable = None
    priority: int = 1
    domain: str = "general"
    is_active: bool = True


@dataclass
class RuleResult:
    """Result of applying a rule."""
    rule_id: str = ""
    rule_name: str = ""
    matched: bool = False
    result: Any = None
    confidence: float = 0.0
    reasoning: str = ""
    execution_time_ms: float = 0.0


class PythonRuleEngine:
    """Python-based rule engine for symbolic reasoning."""
    
    def __init__(self):
        self.rules: Dict[str, Rule] = {}
        self.facts: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize default rules
        self._initialize_default_rules()
    
    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the engine."""
        self.rules[rule.id] = rule
        self.logger.info(f"Added rule: {rule.name} ({rule.id})")
    
    def add_fact(self, key: str, value: Any) -> None:
        """Add a fact to the knowledge base."""
        self.facts[key] = value
    
    def get_fact(self, key: str) -> Any:
        """Get a fact from the knowledge base."""
        return self.facts.get(key)
    
    async def apply_rules(self, context: Dict[str, Any]) -> List[RuleResult]:
        """Apply all applicable rules to the context."""
        results = []
        
        # Add context to facts
        self.facts.update(context)
        
        for rule in self.rules.values():
            if not rule.is_active:
                continue
                
            start_time = datetime.utcnow()
            
            try:
                # Check if rule condition is met
                if rule.condition:
                    matched = rule.condition(self.facts)
                else:
                    matched = True
                
                if matched:
                    # Execute rule action
                    if rule.action:
                        result = rule.action(self.facts)
                    else:
                        result = True
                    
                    execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
                    
                    results.append(RuleResult(
                        rule_id=rule.id,
                        rule_name=rule.name,
                        matched=True,
                        result=result,
                        confidence=1.0,
                        reasoning=f"Rule '{rule.name}' matched and executed successfully",
                        execution_time_ms=execution_time
                    ))
                    
            except Exception as e:
                self.logger.error(f"Error applying rule {rule.name}: {e}")
                results.append(RuleResult(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    matched=False,
                    result=None,
                    confidence=0.0,
                    reasoning=f"Error: {str(e)}",
                    execution_time_ms=0.0
                ))
        
        return results
    
    def _initialize_default_rules(self):
        """Initialize default rules for common scenarios."""
        
        # HIPAA compliance rules
        def hipaa_access_control_condition(facts):
            text = facts.get('text', '').lower()
            return any(term in text for term in ['access control', 'electronic', 'protected health information'])
        
        def hipaa_access_control_action(facts):
            return {
                'compliant': True,
                'requirements_met': ['access_control', 'electronic_phi'],
                'recommendations': ['Ensure proper access controls are in place']
            }
        
        self.add_rule(Rule(
            name="HIPAA Access Control",
            description="Check HIPAA access control compliance",
            condition=hipaa_access_control_condition,
            action=hipaa_access_control_action,
            domain="healthcare"
        ))
        
        # Financial calculation rules
        def debt_to_equity_condition(facts):
            return 'debt' in facts and 'equity' in facts
        
        def debt_to_equity_action(facts):
            debt = facts['debt']
            equity = facts['equity']
            ratio = debt / equity if equity != 0 else float('inf')
            return {
                'ratio': ratio,
                'interpretation': 'High ratio indicates higher financial risk' if ratio > 2 else 'Healthy debt-to-equity ratio',
                'risk_level': 'high' if ratio > 2 else 'medium' if ratio > 1 else 'low'
            }
        
        self.add_rule(Rule(
            name="Debt-to-Equity Ratio",
            description="Calculate debt-to-equity ratio",
            condition=debt_to_equity_condition,
            action=debt_to_equity_action,
            domain="finance"
        ))
        
        # Logical consistency rules
        def logical_consistency_condition(facts):
            text = facts.get('text', '').lower()
            contradictions = [
                ('yes', 'no'), ('true', 'false'), ('compliant', 'non-compliant'),
                ('allowed', 'prohibited'), ('valid', 'invalid')
            ]
            return any(pos in text and neg in text for pos, neg in contradictions)
        
        def logical_consistency_action(facts):
            return {
                'consistent': False,
                'issue': 'Logical contradiction detected',
                'recommendation': 'Review and resolve contradictory statements'
            }
        
        self.add_rule(Rule(
            name="Logical Consistency",
            description="Check for logical contradictions",
            condition=logical_consistency_condition,
            action=logical_consistency_action,
            domain="general"
        ))


class SymbolicService:
    """Symbolic reasoning service using Python-based rule engine."""
    
    def __init__(self):
        self.rule_engine = PythonRuleEngine()
        self.rule_sets = self._initialize_rule_sets()
        self.logger = logging.getLogger(__name__)
    
    async def apply_symbolic_reasoning(self, question: str, hypothesis: str, domain: str = "general") -> List[Dict[str, Any]]:
        """Apply symbolic reasoning to validate a hypothesis."""
        try:
            # Prepare context
            context = {
                'question': question,
                'hypothesis': hypothesis,
                'text': f"{question} {hypothesis}",
                'domain': domain,
                'timestamp': datetime.utcnow()
            }
            
            # Apply rules
            results = await self.rule_engine.apply_rules(context)
            
            # Convert to expected format
            symbolic_results = []
            for result in results:
                symbolic_results.append({
                    "rule": result.rule_name,
                    "result": str(result.result),
                    "passed": result.matched,
                    "confidence": result.confidence,
                    "reasoning": result.reasoning,
                    "execution_time_ms": result.execution_time_ms
                })
            
            return symbolic_results
            
        except Exception as e:
            self.logger.error(f"Error in symbolic reasoning: {e}")
            return [{
                "rule": "Symbolic_Reasoning_Error",
                "result": f"Error: {str(e)}",
                "passed": False,
                "confidence": 0.0,
                "reasoning": "Symbolic reasoning failed due to an error"
            }]
    
    async def validate_mathematical_consistency(self, statement: str) -> Dict[str, Any]:
        """Validate mathematical consistency in a statement."""
        try:
            # Extract mathematical expressions
            math_patterns = [
                r'(\d+)\s*\+\s*(\d+)\s*=\s*(\d+)',
                r'(\d+)\s*\*\s*(\d+)\s*=\s*(\d+)',
                r'(\d+)\s*/\s*(\d+)\s*=\s*(\d+)',
                r'(\d+)\s*-\s*(\d+)\s*=\s*(\d+)'
            ]
            
            results = []
            for pattern in math_patterns:
                matches = re.findall(pattern, statement)
                for match in matches:
                    a, b, expected = map(float, match)
                    
                    # Calculate actual result based on pattern
                    if '+' in pattern:
                        actual = a + b
                        operation = "addition"
                    elif '*' in pattern:
                        actual = a * b
                        operation = "multiplication"
                    elif '/' in pattern:
                        actual = a / b if b != 0 else float('inf')
                        operation = "division"
                    elif '-' in pattern:
                        actual = a - b
                        operation = "subtraction"
                    
                    is_correct = abs(actual - expected) < 0.01
                    results.append({
                        "operation": operation,
                        "expression": f"{a} {operation} {b}",
                        "expected": expected,
                        "actual": actual,
                        "correct": is_correct
                    })
            
            return {
                "consistent": all(r["correct"] for r in results),
                "results": results,
                "summary": f"Found {len(results)} mathematical expressions, {sum(1 for r in results if r['correct'])} correct"
            }
            
        except Exception as e:
            self.logger.error(f"Error in mathematical validation: {e}")
            return {
                "consistent": False,
                "error": str(e)
            }
    
    async def check_logical_consistency(self, statements: List[str]) -> Dict[str, Any]:
        """Check logical consistency across multiple statements."""
        try:
            contradictions = []
            implications = []
            
            # Check for direct contradictions
            for i, stmt1 in enumerate(statements):
                for j, stmt2 in enumerate(statements[i+1:], i+1):
                    # Simple contradiction detection
                    if self._are_contradictory(stmt1, stmt2):
                        contradictions.append({
                            "statement1": stmt1,
                            "statement2": stmt2,
                            "reason": "Direct contradiction detected"
                        })
            
            # Check for logical implications
            for stmt1 in statements:
                for stmt2 in statements:
                    if stmt1 != stmt2 and self._implies(stmt1, stmt2):
                        implications.append({
                            "premise": stmt1,
                            "conclusion": stmt2
                        })
            
            return {
                "consistent": len(contradictions) == 0,
                "contradictions": contradictions,
                "implications": implications,
                "summary": f"Found {len(contradictions)} contradictions and {len(implications)} implications"
            }
            
        except Exception as e:
            self.logger.error(f"Error in logical consistency check: {e}")
            return {
                "consistent": False,
                "error": str(e)
            }
    
    def _are_contradictory(self, stmt1: str, stmt2: str) -> bool:
        """Check if two statements are contradictory."""
        stmt1_lower = stmt1.lower()
        stmt2_lower = stmt2.lower()
        
        # Simple contradiction patterns
        contradictions = [
            ("yes", "no"), ("true", "false"), ("compliant", "non-compliant"),
            ("allowed", "prohibited"), ("valid", "invalid"), ("success", "failure")
        ]
        
        for pos, neg in contradictions:
            if pos in stmt1_lower and neg in stmt2_lower:
                return True
            if neg in stmt1_lower and pos in stmt2_lower:
                return True
        
        return False
    
    def _implies(self, premise: str, conclusion: str) -> bool:
        """Check if premise implies conclusion."""
        # Simple implication detection
        premise_lower = premise.lower()
        conclusion_lower = conclusion.lower()
        
        # Check for common implication patterns
        if "if" in premise_lower and "then" in premise_lower:
            # Extract condition and consequence
            if "then" in premise_lower:
                condition_part = premise_lower.split("then")[0]
                if any(word in conclusion_lower for word in condition_part.split()):
                    return True
        
        return False
    
    def _initialize_rule_sets(self) -> Dict[str, Dict[str, Any]]:
        """Initialize available rule sets."""
        return {
            "healthcare": self._get_hipaa_rules(),
            "finance": self._get_finance_rules(),
            "general": self._get_general_rules()
        }
    
    def _get_hipaa_rules(self) -> Dict[str, Any]:
        """Get HIPAA compliance rules."""
        return {
            "name": "HIPAA Compliance Rules",
            "description": "Rules for HIPAA compliance checking",
            "rules": [
                {
                    "id": "hipaa_164_312_a_1",
                    "name": "Access Control",
                    "description": "Implement technical policies and procedures for electronic information systems",
                    "keywords": ["access control", "electronic", "protected health information"],
                    "check_function": self._check_hipaa_access_control
                },
                {
                    "id": "hipaa_164_312_c_1", 
                    "name": "Integrity",
                    "description": "Implement policies to protect electronic PHI from improper alteration",
                    "keywords": ["integrity", "alteration", "destruction", "electronic"],
                    "check_function": self._check_hipaa_integrity
                },
                {
                    "id": "hipaa_164_312_d",
                    "name": "Authentication",
                    "description": "Implement procedures to verify person or entity seeking access",
                    "keywords": ["authentication", "verification", "person", "entity"],
                    "check_function": self._check_hipaa_authentication
                }
            ]
        }
    
    def _get_finance_rules(self) -> Dict[str, Any]:
        """Get financial calculation rules."""
        return {
            "name": "Financial Calculation Rules",
            "description": "Rules for financial calculations and validations",
            "rules": [
                {
                    "id": "debt_to_equity",
                    "name": "Debt-to-Equity Ratio",
                    "description": "Calculate debt-to-equity ratio: Total Debt / Total Equity",
                    "keywords": ["debt", "equity", "ratio", "debt-to-equity"],
                    "check_function": self._check_debt_to_equity
                },
                {
                    "id": "current_ratio",
                    "name": "Current Ratio",
                    "description": "Calculate current ratio: Current Assets / Current Liabilities",
                    "keywords": ["current ratio", "current assets", "current liabilities"],
                    "check_function": self._check_current_ratio
                },
                {
                    "id": "roi",
                    "name": "Return on Investment",
                    "description": "Calculate ROI: (Gain - Cost) / Cost * 100",
                    "keywords": ["roi", "return on investment", "gain", "cost"],
                    "check_function": self._check_roi
                }
            ]
        }
    
    def _get_general_rules(self) -> Dict[str, Any]:
        """Get general logical rules."""
        return {
            "name": "General Logical Rules",
            "description": "General logical validation rules",
            "rules": [
                {
                    "id": "mathematical_consistency",
                    "name": "Mathematical Consistency",
                    "description": "Check for mathematical consistency in calculations",
                    "keywords": ["calculation", "math", "formula", "equation"],
                    "check_function": self._check_mathematical_consistency
                },
                {
                    "id": "logical_consistency",
                    "name": "Logical Consistency",
                    "description": "Check for logical consistency in statements",
                    "keywords": ["logic", "consistency", "contradiction"],
                    "check_function": self._check_logical_consistency
                }
            ]
        }
    
    # Rule check functions (simplified implementations)
    async def _check_hipaa_access_control(self, text: str) -> Dict[str, Any]:
        """Check HIPAA access control compliance."""
        text_lower = text.lower()
        has_access_control = any(term in text_lower for term in ["access control", "authentication", "authorization"])
        has_electronic = any(term in text_lower for term in ["electronic", "digital", "computer"])
        has_phi = any(term in text_lower for term in ["protected health information", "phi", "health data"])
        
        return {
            "compliant": has_access_control and has_electronic and has_phi,
            "requirements_met": {
                "access_control": has_access_control,
                "electronic_systems": has_electronic,
                "phi_protection": has_phi
            }
        }
    
    async def _check_hipaa_integrity(self, text: str) -> Dict[str, Any]:
        """Check HIPAA integrity compliance."""
        text_lower = text.lower()
        has_integrity = any(term in text_lower for term in ["integrity", "unaltered", "unaltered"])
        has_protection = any(term in text_lower for term in ["protection", "safeguard", "secure"])
        
        return {
            "compliant": has_integrity and has_protection,
            "requirements_met": {
                "integrity_protection": has_integrity,
                "data_protection": has_protection
            }
        }
    
    async def _check_hipaa_authentication(self, text: str) -> Dict[str, Any]:
        """Check HIPAA authentication compliance."""
        text_lower = text.lower()
        has_authentication = any(term in text_lower for term in ["authentication", "verification", "identity"])
        has_person_entity = any(term in text_lower for term in ["person", "entity", "user", "individual"])
        
        return {
            "compliant": has_authentication and has_person_entity,
            "requirements_met": {
                "authentication_procedures": has_authentication,
                "person_entity_verification": has_person_entity
            }
        }
    
    async def _check_debt_to_equity(self, text: str) -> Dict[str, Any]:
        """Check debt-to-equity ratio calculation."""
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        if len(numbers) >= 2:
            try:
                debt = float(numbers[0])
                equity = float(numbers[1])
                ratio = debt / equity if equity != 0 else float('inf')
                return {
                    "valid": True,
                    "ratio": ratio,
                    "interpretation": "High risk" if ratio > 2 else "Medium risk" if ratio > 1 else "Low risk"
                }
            except ValueError:
                pass
        
        return {"valid": False, "error": "Could not extract debt and equity values"}
    
    async def _check_current_ratio(self, text: str) -> Dict[str, Any]:
        """Check current ratio calculation."""
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        if len(numbers) >= 2:
            try:
                assets = float(numbers[0])
                liabilities = float(numbers[1])
                ratio = assets / liabilities if liabilities != 0 else float('inf')
                return {
                    "valid": True,
                    "ratio": ratio,
                    "interpretation": "Good liquidity" if ratio > 1 else "Poor liquidity"
                }
            except ValueError:
                pass
        
        return {"valid": False, "error": "Could not extract current assets and liabilities"}
    
    async def _check_roi(self, text: str) -> Dict[str, Any]:
        """Check ROI calculation."""
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        if len(numbers) >= 2:
            try:
                gain = float(numbers[0])
                cost = float(numbers[1])
                roi = ((gain - cost) / cost) * 100 if cost != 0 else float('inf')
                return {
                    "valid": True,
                    "roi_percentage": roi,
                    "interpretation": "Good investment" if roi > 0 else "Poor investment"
                }
            except ValueError:
                pass
        
        return {"valid": False, "error": "Could not extract gain and cost values"}
    
    async def _check_mathematical_consistency(self, text: str) -> Dict[str, Any]:
        """Check mathematical consistency."""
        return await self.validate_mathematical_consistency(text)
    
    async def _check_logical_consistency(self, text: str) -> Dict[str, Any]:
        """Check logical consistency."""
        statements = [s.strip() for s in text.split('.') if s.strip()]
        return await self.check_logical_consistency(statements)


# Global symbolic service instance
symbolic_service = SymbolicService()
