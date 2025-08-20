"""
Symbolic Service for System 2 reasoning (rule-based, logical verification).
"""

import re
import math
from typing import Dict, Any, Optional, List, Tuple

# Import optional dependencies with fallbacks
try:
    from z3 import *
    Z3_AVAILABLE = True
except ImportError:
    Z3_AVAILABLE = False
    print("⚠️  Z3 solver not available. Some symbolic reasoning features will be limited.")

try:
    from pyswip import Prolog
    # Test if SWI-Prolog is actually available
    test_prolog = Prolog()
    PROLOG_AVAILABLE = True
except (ImportError, Exception) as e:
    PROLOG_AVAILABLE = False
    print(f"⚠️  Prolog (pyswip) not available: {e}")
    print("💡 To enable Prolog reasoning, install SWI-Prolog: brew install swi-prolog")

from app.models.reasoning import ReasoningTrace, ReasoningStage


class SymbolicService:
    """Service for symbolic/rule-based reasoning."""
    
    def __init__(self):
        self.rule_sets = self._initialize_rule_sets()
        self._initialize_prolog_rules()
    
    def _initialize_prolog_rules(self):
        """Initialize Prolog rules for advanced reasoning."""
        if not PROLOG_AVAILABLE:
            print("⚠️  Skipping Prolog rule initialization - pyswip not available")
            return
            
        try:
            self.prolog = Prolog()
            
            # HIPAA compliance rules
            hipaa_rules = """
                % Rule: Access request is HIPAA compliant if user has authentication and authorization for electronic PHI
                hipaa_compliant(access_request) :- 
                    has_authentication(user),
                    has_authorization(user, resource),
                    electronic_phi(resource).
                
                % Rule: Access request is compliant if it's not for electronic PHI
                hipaa_compliant(access_request) :- 
                    not(electronic_phi(resource)).
                
                % Financial calculation rules
                debt_to_equity_ratio(Debt, Equity, Ratio) :- 
                    Ratio is Debt / Equity.
                
                current_ratio(Assets, Liabilities, Ratio) :- 
                    Ratio is Assets / Liabilities.
                
                roi(Gain, Cost, Percentage) :- 
                    Percentage is ((Gain - Cost) / Cost) * 100.
                
                % Logical consistency rules
                logically_consistent(Statement) :- 
                    not(contradicts(Statement, Statement)).
                
                % Transitive implication
                implies(A, C) :- 
                    implies(A, B),
                    implies(B, C).
            """
            
            # Load rules into Prolog
            for rule in hipaa_rules.strip().split('\n'):
                if rule.strip() and not rule.strip().startswith('%'):
                    try:
                        self.prolog.assertz(rule.strip())
                    except Exception as e:
                        print(f"⚠️  Warning: Could not load Prolog rule '{rule.strip()}': {e}")
                        
        except Exception as e:
            print(f"⚠️  Error initializing Prolog rules: {e}")
            global PROLOG_AVAILABLE
            PROLOG_AVAILABLE = False
    
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
                    "description": "Implement technical policies and procedures for electronic information systems that maintain electronic protected health information to allow access only to those persons or software programs that have been granted access rights",
                    "keywords": ["access control", "electronic", "protected health information", "access rights"],
                    "check_function": self._check_hipaa_access_control
                },
                {
                    "id": "hipaa_164_312_c_1",
                    "name": "Integrity",
                    "description": "Implement policies and procedures to protect electronic protected health information from improper alteration or destruction",
                    "keywords": ["integrity", "alteration", "destruction", "electronic"],
                    "check_function": self._check_hipaa_integrity
                },
                {
                    "id": "hipaa_164_312_d",
                    "name": "Person or Entity Authentication",
                    "description": "Implement procedures to verify that a person or entity seeking access to electronic protected health information is the one claimed",
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
                    "keywords": ["calculate", "math", "formula", "equation"],
                    "check_function": self._check_mathematical_consistency
                },
                {
                    "id": "logical_consistency",
                    "name": "Logical Consistency",
                    "description": "Check for logical consistency in statements",
                    "keywords": ["logic", "consistent", "contradiction"],
                    "check_function": self._check_logical_consistency
                }
            ]
        }
    
    async def apply_rules(
        self, 
        hypothesis: str, 
        question: str, 
        domain: Optional[str] = None
    ) -> ReasoningTrace:
        """
        Apply symbolic rules to validate the hypothesis.
        
        Args:
            hypothesis: LLM-generated hypothesis
            question: Original question
            domain: Domain context
            
        Returns:
            ReasoningTrace with rule check results
        """
        
        if not domain or domain not in self.rule_sets:
            domain = "general"
        
        rule_set = self.rule_sets[domain]
        results = []
        pydatalog_results = []
        
        # Apply traditional rule-based checks
        for rule in rule_set["rules"]:
            # Check if rule is relevant based on keywords
            if self._is_rule_relevant(rule, question, hypothesis):
                try:
                    result = await rule["check_function"](question, hypothesis)
                    results.append({
                        "rule": rule["name"],
                        "result": result,
                        "passed": result.get("passed", False)
                    })
                except Exception as e:
                    results.append({
                        "rule": rule["name"],
                        "result": {"error": str(e)},
                        "passed": False
                    })
        
        # Apply Prolog-based reasoning
        if PROLOG_AVAILABLE:
            try:
                prolog_results = await self._apply_prolog_reasoning(question, hypothesis, domain)
            except Exception as e:
                prolog_results = [{"error": f"Prolog reasoning failed: {str(e)}"}]
        else:
            prolog_results = [{"info": "Prolog not available - using fallback reasoning methods"}]
        
        # Combine results
        all_results = results + prolog_results
        
        # Calculate overall confidence based on rule results
        passed_rules = sum(1 for r in results if r.get("passed", False))
        total_rules = len(results)
        confidence = passed_rules / total_rules if total_rules > 0 else 0.5
        
        output = f"Applied {total_rules} traditional rules and {len(prolog_results)} Prolog rules from {rule_set['name']}. "
        output += f"Passed: {passed_rules}/{total_rules} traditional rules."
        
        if results:
            output += "\n\nTraditional rule results:\n"
            for result in results:
                output += f"- {result['rule']}: {'PASS' if result['passed'] else 'FAIL'}\n"
        
        if prolog_results:
            output += "\n\nProlog reasoning results:\n"
            for result in prolog_results:
                if "error" in result:
                    output += f"- Error: {result['error']}\n"
                else:
                    output += f"- {result.get('rule', 'Unknown')}: {result.get('result', 'N/A')}\n"
        
        return ReasoningTrace(
            stage=ReasoningStage.RULE_CHECK,
            output=output,
            confidence=confidence,
            metadata={
                "domain": domain,
                "rule_set": rule_set["name"],
                "traditional_results": results,
                "prolog_results": prolog_results
            }
        )
    
    def _is_rule_relevant(self, rule: Dict[str, Any], question: str, hypothesis: str) -> bool:
        """Check if a rule is relevant to the question/hypothesis."""
        text = f"{question} {hypothesis}".lower()
        keywords = [kw.lower() for kw in rule.get("keywords", [])]
        
        return any(keyword in text for keyword in keywords)
    
    async def _apply_prolog_reasoning(
        self, 
        question: str, 
        hypothesis: str, 
        domain: str
    ) -> List[Dict[str, Any]]:
        """
        Apply Prolog-based reasoning for advanced rule evaluation.
        
        Args:
            question: Original question
            hypothesis: LLM-generated hypothesis
            domain: Domain context
            
        Returns:
            List of Prolog reasoning results
        """
        if not PROLOG_AVAILABLE:
            return [{"info": "Prolog not available - using fallback reasoning methods"}]
            
        results = []
        
        try:
            if domain == "healthcare":
                results.extend(await self._apply_hipaa_prolog_rules(question, hypothesis))
            elif domain == "finance":
                results.extend(await self._apply_finance_prolog_rules(question, hypothesis))
            else:
                results.extend(await self._apply_general_prolog_rules(question, hypothesis))
                
        except Exception as e:
            results.append({
                "rule": "prolog_reasoning",
                "result": f"Error in Prolog reasoning: {str(e)}",
                "passed": False
            })
        
        return results
    
    async def _apply_hipaa_prolog_rules(self, question: str, hypothesis: str) -> List[Dict[str, Any]]:
        """Apply HIPAA-specific Prolog rules."""
        if not PROLOG_AVAILABLE:
            return [{"info": "Prolog not available for HIPAA rules"}]
            
        results = []
        
        # Extract entities from text
        text = f"{question} {hypothesis}".lower()
        
        # Check for authentication
        has_auth = any(term in text for term in ["authentication", "login", "password", "2fa"])
        
        # Check for authorization
        has_authz = any(term in text for term in ["authorization", "permission", "role", "access control"])
        
        # Check for electronic PHI
        has_ephi = any(term in text for term in ["electronic", "digital", "computer", "system", "database"])
        
        # Add facts to Prolog
        if has_auth:
            self.prolog.assertz('has_authentication(user)')
        if has_authz:
            self.prolog.assertz('has_authorization(user, resource)')
        if has_ephi:
            self.prolog.assertz('electronic_phi(resource)')
        
        # Query compliance
        try:
            compliance_result = list(self.prolog.query('hipaa_compliant(access_request)'))
            results.append({
                "rule": "HIPAA_Compliance_Prolog",
                "result": f"Compliance check: {len(compliance_result) > 0}",
                "passed": len(compliance_result) > 0
            })
        except Exception as e:
            results.append({
                "rule": "HIPAA_Compliance_Prolog",
                "result": f"Query failed: {str(e)}",
                "passed": False
            })
        
        return results
    
    async def _apply_finance_prolog_rules(self, question: str, hypothesis: str) -> List[Dict[str, Any]]:
        """Apply finance-specific Prolog rules."""
        if not PROLOG_AVAILABLE:
            return [{"info": "Prolog not available for finance rules"}]
            
        results = []
        
        # Extract numbers from text
        numbers = re.findall(r'\d+(?:\.\d+)?', f"{question} {hypothesis}")
        
        if len(numbers) >= 2:
            try:
                debt = float(numbers[0])
                equity = float(numbers[1])
                
                # Query debt-to-equity ratio
                ratio_result = list(self.prolog.query(f'debt_to_equity_ratio({debt}, {equity}, Ratio)'))
                if ratio_result:
                    calculated_ratio = ratio_result[0]['Ratio']
                    results.append({
                        "rule": "Debt_to_Equity_Prolog",
                        "result": f"Calculated ratio: {calculated_ratio}",
                        "passed": True
                    })
                
                # Query current ratio if we have more numbers
                if len(numbers) >= 4:
                    assets = float(numbers[2])
                    liabilities = float(numbers[3])
                    
                    current_ratio_result = list(self.prolog.query(f'current_ratio({assets}, {liabilities}, Ratio)'))
                    if current_ratio_result:
                        calculated_current_ratio = current_ratio_result[0]['Ratio']
                        results.append({
                            "rule": "Current_Ratio_Prolog",
                            "result": f"Calculated current ratio: {calculated_current_ratio}",
                            "passed": True
                        })
                        
            except Exception as e:
                results.append({
                    "rule": "Finance_Calculations_Prolog",
                    "result": f"Calculation failed: {str(e)}",
                    "passed": False
                })
        
        return results
    
    async def _apply_general_prolog_rules(self, question: str, hypothesis: str) -> List[Dict[str, Any]]:
        """Apply general Prolog rules for logical consistency."""
        if not PROLOG_AVAILABLE:
            return [{"info": "Prolog not available for general rules"}]
            
        results = []
        
        # Check for logical contradictions
        text = hypothesis.lower()
        contradictions = [
            ("yes", "no"),
            ("true", "false"),
            ("compliant", "non-compliant"),
            ("allowed", "prohibited")
        ]
        
        has_contradiction = False
        for pos, neg in contradictions:
            if pos in text and neg in text:
                has_contradiction = True
                break
        
        # Add facts to Prolog
        if has_contradiction:
            self.prolog.assertz('contradicts(statement, statement)')
        
        # Query logical consistency
        try:
            consistency_result = list(self.prolog.query('logically_consistent(statement)'))
            results.append({
                "rule": "Logical_Consistency_Prolog",
                "result": f"Logical consistency: {len(consistency_result) > 0}",
                "passed": not has_contradiction
            })
        except Exception as e:
            results.append({
                "rule": "Logical_Consistency_Prolog",
                "result": f"Consistency check failed: {str(e)}",
                "passed": False
            })
        
        return results
    
    # HIPAA Rule Check Functions
    async def _check_hipaa_access_control(self, question: str, hypothesis: str) -> Dict[str, Any]:
        """Check HIPAA access control compliance."""
        text = f"{question} {hypothesis}".lower()
        
        # Simple keyword-based checks
        has_access_control = any(term in text for term in ["access control", "authentication", "authorization"])
        has_electronic_phi = any(term in text for term in ["electronic", "phi", "protected health information"])
        
        passed = has_access_control and has_electronic_phi
        
        return {
            "passed": passed,
            "details": {
                "access_control_mentioned": has_access_control,
                "electronic_phi_mentioned": has_electronic_phi
            }
        }
    
    async def _check_hipaa_integrity(self, question: str, hypothesis: str) -> Dict[str, Any]:
        """Check HIPAA integrity compliance."""
        text = f"{question} {hypothesis}".lower()
        
        has_integrity = any(term in text for term in ["integrity", "unaltered", "unaltered", "protection"])
        has_alteration_protection = any(term in text for term in ["alteration", "destruction", "modification"])
        
        passed = has_integrity or has_alteration_protection
        
        return {
            "passed": passed,
            "details": {
                "integrity_mentioned": has_integrity,
                "alteration_protection_mentioned": has_alteration_protection
            }
        }
    
    async def _check_hipaa_authentication(self, question: str, hypothesis: str) -> Dict[str, Any]:
        """Check HIPAA authentication compliance."""
        text = f"{question} {hypothesis}".lower()
        
        has_authentication = any(term in text for term in ["authentication", "verification", "identity"])
        has_person_entity = any(term in text for term in ["person", "entity", "user", "individual"])
        
        passed = has_authentication and has_person_entity
        
        return {
            "passed": passed,
            "details": {
                "authentication_mentioned": has_authentication,
                "person_entity_mentioned": has_person_entity
            }
        }
    
    # Finance Rule Check Functions
    async def _check_debt_to_equity(self, question: str, hypothesis: str) -> Dict[str, Any]:
        """Check debt-to-equity ratio calculation."""
        # Extract numbers from text
        numbers = re.findall(r'\d+(?:\.\d+)?', f"{question} {hypothesis}")
        
        if len(numbers) >= 2:
            try:
                debt = float(numbers[0])
                equity = float(numbers[1])
                
                if equity != 0:
                    calculated_ratio = debt / equity
                    
                    # Look for ratio in hypothesis
                    ratio_match = re.search(r'(\d+(?:\.\d+)?)', hypothesis)
                    if ratio_match:
                        stated_ratio = float(ratio_match.group(1))
                        tolerance = 0.01
                        passed = abs(calculated_ratio - stated_ratio) < tolerance
                        
                        return {
                            "passed": passed,
                            "details": {
                                "debt": debt,
                                "equity": equity,
                                "calculated_ratio": calculated_ratio,
                                "stated_ratio": stated_ratio,
                                "difference": abs(calculated_ratio - stated_ratio)
                            }
                        }
            except (ValueError, ZeroDivisionError):
                pass
        
        return {"passed": False, "details": {"error": "Could not extract or calculate ratio"}}
    
    async def _check_current_ratio(self, question: str, hypothesis: str) -> Dict[str, Any]:
        """Check current ratio calculation."""
        # Similar to debt-to-equity but for current assets/liabilities
        numbers = re.findall(r'\d+(?:\.\d+)?', f"{question} {hypothesis}")
        
        if len(numbers) >= 2:
            try:
                assets = float(numbers[0])
                liabilities = float(numbers[1])
                
                if liabilities != 0:
                    calculated_ratio = assets / liabilities
                    
                    ratio_match = re.search(r'(\d+(?:\.\d+)?)', hypothesis)
                    if ratio_match:
                        stated_ratio = float(ratio_match.group(1))
                        tolerance = 0.01
                        passed = abs(calculated_ratio - stated_ratio) < tolerance
                        
                        return {
                            "passed": passed,
                            "details": {
                                "assets": assets,
                                "liabilities": liabilities,
                                "calculated_ratio": calculated_ratio,
                                "stated_ratio": stated_ratio
                            }
                        }
            except (ValueError, ZeroDivisionError):
                pass
        
        return {"passed": False, "details": {"error": "Could not extract or calculate ratio"}}
    
    async def _check_roi(self, question: str, hypothesis: str) -> Dict[str, Any]:
        """Check ROI calculation."""
        numbers = re.findall(r'\d+(?:\.\d+)?', f"{question} {hypothesis}")
        
        if len(numbers) >= 2:
            try:
                gain = float(numbers[0])
                cost = float(numbers[1])
                
                if cost != 0:
                    calculated_roi = (gain - cost) / cost * 100
                    
                    roi_match = re.search(r'(\d+(?:\.\d+)?)%', hypothesis)
                    if roi_match:
                        stated_roi = float(roi_match.group(1))
                        tolerance = 0.1
                        passed = abs(calculated_roi - stated_roi) < tolerance
                        
                        return {
                            "passed": passed,
                            "details": {
                                "gain": gain,
                                "cost": cost,
                                "calculated_roi": calculated_roi,
                                "stated_roi": stated_roi
                            }
                        }
            except (ValueError, ZeroDivisionError):
                pass
        
        return {"passed": False, "details": {"error": "Could not extract or calculate ROI"}}
    
    # General Rule Check Functions
    async def _check_mathematical_consistency(self, question: str, hypothesis: str) -> Dict[str, Any]:
        """Check mathematical consistency."""
        # Look for mathematical expressions and verify they're consistent
        math_expressions = re.findall(r'[\d\+\-\*\/\(\)\=]+', hypothesis)
        
        if math_expressions:
            try:
                # Simple evaluation of expressions
                for expr in math_expressions:
                    if '=' in expr:
                        left, right = expr.split('=', 1)
                        try:
                            left_val = eval(left.strip())
                            right_val = eval(right.strip())
                            if abs(left_val - right_val) > 0.001:
                                return {"passed": False, "details": {"inconsistent_expression": expr}}
                        except:
                            pass
                
                return {"passed": True, "details": {"expressions_checked": len(math_expressions)}}
            except:
                pass
        
        return {"passed": True, "details": {"no_math_expressions": True}}
    
    async def _check_logical_consistency(self, question: str, hypothesis: str) -> Dict[str, Any]:
        """Check logical consistency."""
        # Look for logical contradictions
        contradictions = [
            ("yes", "no"),
            ("true", "false"),
            ("compliant", "non-compliant"),
            ("allowed", "prohibited")
        ]
        
        text = hypothesis.lower()
        for pos, neg in contradictions:
            if pos in text and neg in text:
                return {
                    "passed": False, 
                    "details": {"contradiction": f"{pos} vs {neg}"}
                }
        
        return {"passed": True, "details": {"no_contradictions": True}}
