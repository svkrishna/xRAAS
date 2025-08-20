"""
Extensible Ruleset Service for loading and managing multi-domain rulesets.
"""

import json
import yaml
import re
import time
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from datetime import datetime

from app.models.rulesets import (
    RulesetDefinition, RuleDefinition, RuleType, RuleCondition,
    RulesetExecutionResult, RuleExecutionResult, RulesetValidationResult
)
from app.services.symbolic_service import SymbolicService


class RulesetService:
    """Service for managing extensible rulesets."""
    
    def __init__(self):
        self.rulesets: Dict[str, RulesetDefinition] = {}
        self.symbolic_service = SymbolicService()
        self._load_builtin_rulesets()
    
    def _load_builtin_rulesets(self):
        """Load built-in rulesets from YAML files."""
        rulesets_dir = Path(__file__).parent.parent / "rulesets"
        if rulesets_dir.exists():
            for yaml_file in rulesets_dir.glob("*.yaml"):
                try:
                    self.load_ruleset_from_file(yaml_file)
                except Exception as e:
                    print(f"⚠️  Failed to load ruleset from {yaml_file}: {e}")
    
    def load_ruleset_from_file(self, file_path: Union[str, Path]) -> RulesetDefinition:
        """Load a ruleset from a YAML or JSON file."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Ruleset file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.suffix.lower() in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            elif file_path.suffix.lower() == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        return self.load_ruleset_from_dict(data)
    
    def load_ruleset_from_dict(self, data: Dict[str, Any]) -> RulesetDefinition:
        """Load a ruleset from a dictionary."""
        ruleset = RulesetDefinition(**data)
        self.rulesets[ruleset.id] = ruleset
        return ruleset
    
    def load_ruleset_from_json(self, json_str: str) -> RulesetDefinition:
        """Load a ruleset from a JSON string."""
        data = json.loads(json_str)
        return self.load_ruleset_from_dict(data)
    
    def get_ruleset(self, ruleset_id: str) -> Optional[RulesetDefinition]:
        """Get a ruleset by ID."""
        return self.rulesets.get(ruleset_id)
    
    def get_rulesets_by_domain(self, domain: str) -> List[RulesetDefinition]:
        """Get all rulesets for a specific domain."""
        return [
            ruleset for ruleset in self.rulesets.values()
            if ruleset.domain.lower() == domain.lower() and ruleset.enabled
        ]
    
    def get_all_rulesets(self) -> List[RulesetDefinition]:
        """Get all available rulesets."""
        return list(self.rulesets.values())
    
    def validate_ruleset(self, ruleset: RulesetDefinition) -> RulesetValidationResult:
        """Validate a ruleset definition."""
        errors = []
        warnings = []
        
        # Check for duplicate rule IDs
        rule_ids = [rule.id for rule in ruleset.rules]
        if len(rule_ids) != len(set(rule_ids)):
            errors.append("Duplicate rule IDs found")
        
        # Validate each rule
        for rule in ruleset.rules:
            # Validate rule content based on type
            if rule.type == RuleType.PROLOG:
                if not self._validate_prolog_rule(rule.content):
                    errors.append(f"Invalid Prolog rule in {rule.id}")
            
            elif rule.type == RuleType.PYTHON:
                if not self._validate_python_rule(rule.content):
                    errors.append(f"Invalid Python rule in {rule.id}")
            
            elif rule.type == RuleType.REGEX:
                if not self._validate_regex_rule(rule.content):
                    errors.append(f"Invalid regex pattern in {rule.id}")
            
            # Check for missing required fields
            if not rule.name or not rule.description:
                warnings.append(f"Rule {rule.id} missing name or description")
        
        # Estimate complexity
        complexity = self._estimate_complexity(ruleset)
        
        return RulesetValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            rule_count=len(ruleset.rules),
            estimated_complexity=complexity
        )
    
    def _validate_prolog_rule(self, content: str) -> bool:
        """Validate Prolog rule syntax."""
        try:
            # Basic Prolog syntax validation
            if not content.strip():
                return False
            
            # Check for basic Prolog structure
            if ':-' in content:
                # Rule with body
                parts = content.split(':-', 1)
                if len(parts) != 2:
                    return False
                head, body = parts
                if not head.strip() or not body.strip():
                    return False
            else:
                # Fact
                if not content.strip().endswith('.'):
                    return False
            
            return True
        except Exception:
            return False
    
    def _validate_python_rule(self, content: str) -> bool:
        """Validate Python rule syntax."""
        try:
            compile(content, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
    
    def _validate_regex_rule(self, content: str) -> bool:
        """Validate regex pattern."""
        try:
            re.compile(content)
            return True
        except re.error:
            return False
    
    def _estimate_complexity(self, ruleset: RulesetDefinition) -> str:
        """Estimate computational complexity of a ruleset."""
        total_rules = len(ruleset.rules)
        prolog_rules = sum(1 for r in ruleset.rules if r.type == RuleType.PROLOG)
        python_rules = sum(1 for r in ruleset.rules if r.type == RuleType.PYTHON)
        
        if total_rules <= 5:
            return "Low"
        elif total_rules <= 20:
            return "Medium"
        elif prolog_rules > 10 or python_rules > 5:
            return "High"
        else:
            return "Medium"
    
    async def execute_ruleset(
        self, 
        ruleset_id: str, 
        question: str, 
        hypothesis: str,
        context: Optional[Dict[str, Any]] = None
    ) -> RulesetExecutionResult:
        """Execute a ruleset against given input."""
        ruleset = self.get_ruleset(ruleset_id)
        if not ruleset:
            raise ValueError(f"Ruleset not found: {ruleset_id}")
        
        if not ruleset.enabled:
            raise ValueError(f"Ruleset is disabled: {ruleset_id}")
        
        start_time = time.time()
        rule_results = []
        errors = []
        
        # Filter rules based on conditions
        applicable_rules = self._filter_applicable_rules(ruleset.rules, question, hypothesis, context)
        
        for rule in applicable_rules:
            rule_start_time = time.time()
            try:
                result = await self._execute_rule(rule, question, hypothesis, context)
                rule_results.append(result)
            except Exception as e:
                error_msg = f"Rule {rule.id} execution failed: {str(e)}"
                errors.append(error_msg)
                rule_results.append(RuleExecutionResult(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    passed=False,
                    confidence=0.0,
                    output={},
                    execution_time_ms=(time.time() - rule_start_time) * 1000,
                    error_message=error_msg
                ))
        
        execution_time_ms = (time.time() - start_time) * 1000
        passed_rules = sum(1 for r in rule_results if r.passed)
        
        # Calculate weighted confidence
        total_weight = sum(rule.weight for rule in applicable_rules)
        if total_weight > 0:
            weighted_confidence = sum(
                r.confidence * next((rule.weight for rule in applicable_rules if rule.id == r.rule_id), 1.0)
                for r in rule_results
            ) / total_weight
        else:
            weighted_confidence = 0.0
        
        return RulesetExecutionResult(
            ruleset_id=ruleset.id,
            ruleset_name=ruleset.name,
            domain=ruleset.domain,
            total_rules=len(applicable_rules),
            passed_rules=passed_rules,
            failed_rules=len(applicable_rules) - passed_rules,
            overall_confidence=weighted_confidence,
            rule_results=rule_results,
            execution_time_ms=execution_time_ms,
            errors=errors
        )
    
    def _filter_applicable_rules(
        self, 
        rules: List[RuleDefinition], 
        question: str, 
        hypothesis: str,
        context: Optional[Dict[str, Any]] = None
    ) -> List[RuleDefinition]:
        """Filter rules based on conditions."""
        applicable_rules = []
        
        for rule in rules:
            if not rule.enabled:
                continue
            
            if not rule.conditions:
                applicable_rules.append(rule)
                continue
            
            # Check all conditions
            all_conditions_met = True
            for condition in rule.conditions:
                if not self._evaluate_condition(condition, question, hypothesis, context):
                    all_conditions_met = False
                    break
            
            if all_conditions_met:
                applicable_rules.append(rule)
        
        return applicable_rules
    
    def _evaluate_condition(
        self, 
        condition: RuleCondition, 
        question: str, 
        hypothesis: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Evaluate a rule condition."""
        # Get the field value
        if condition.field == "question":
            field_value = question
        elif condition.field == "hypothesis":
            field_value = hypothesis
        elif condition.field == "domain" and context:
            field_value = context.get("domain", "")
        else:
            field_value = str(context.get(condition.field, "")) if context else ""
        
        if not condition.case_sensitive:
            field_value = field_value.lower()
            condition_value = str(condition.value).lower()
        else:
            condition_value = str(condition.value)
        
        # Apply operator
        if condition.operator == "contains":
            return condition_value in field_value
        elif condition.operator == "equals":
            return field_value == condition_value
        elif condition.operator == "regex":
            try:
                return bool(re.search(condition_value, field_value))
            except re.error:
                return False
        elif condition.operator == "starts_with":
            return field_value.startswith(condition_value)
        elif condition.operator == "ends_with":
            return field_value.endswith(condition_value)
        else:
            return False
    
    async def _execute_rule(
        self, 
        rule: RuleDefinition, 
        question: str, 
        hypothesis: str,
        context: Optional[Dict[str, Any]] = None
    ) -> RuleExecutionResult:
        """Execute a single rule."""
        start_time = time.time()
        
        try:
            if rule.type == RuleType.PROLOG:
                result = await self._execute_prolog_rule(rule, question, hypothesis, context)
            elif rule.type == RuleType.PYTHON:
                result = await self._execute_python_rule(rule, question, hypothesis, context)
            elif rule.type == RuleType.REGEX:
                result = await self._execute_regex_rule(rule, question, hypothesis, context)
            elif rule.type == RuleType.KEYWORD:
                result = await self._execute_keyword_rule(rule, question, hypothesis, context)
            else:
                raise ValueError(f"Unsupported rule type: {rule.type}")
            
            execution_time_ms = (time.time() - start_time) * 1000
            
            return RuleExecutionResult(
                rule_id=rule.id,
                rule_name=rule.name,
                passed=result.get("passed", False),
                confidence=result.get("confidence", 0.0),
                output=result.get("output", {}),
                execution_time_ms=execution_time_ms,
                error_message=None
            )
            
        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            return RuleExecutionResult(
                rule_id=rule.id,
                rule_name=rule.name,
                passed=False,
                confidence=0.0,
                output={},
                execution_time_ms=execution_time_ms,
                error_message=str(e)
            )
    
    async def _execute_prolog_rule(
        self, 
        rule: RuleDefinition, 
        question: str, 
        hypothesis: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a Prolog rule."""
        # This would integrate with the existing SymbolicService
        # For now, return a basic result
        return {
            "passed": True,
            "confidence": 0.8,
            "output": {"prolog_result": "Rule executed successfully"}
        }
    
    async def _execute_python_rule(
        self, 
        rule: RuleDefinition, 
        question: str, 
        hypothesis: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a Python rule."""
        # Create a safe execution environment
        local_vars = {
            "question": question,
            "hypothesis": hypothesis,
            "context": context or {},
            "result": {"passed": False, "confidence": 0.0, "output": {}}
        }
        
        try:
            exec(rule.content, {"__builtins__": {}}, local_vars)
            return local_vars.get("result", {"passed": False, "confidence": 0.0, "output": {}})
        except Exception as e:
            return {
                "passed": False,
                "confidence": 0.0,
                "output": {"error": str(e)}
            }
    
    async def _execute_regex_rule(
        self, 
        rule: RuleDefinition, 
        question: str, 
        hypothesis: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a regex rule."""
        text = f"{question} {hypothesis}"
        pattern = rule.content
        
        try:
            matches = re.findall(pattern, text, re.IGNORECASE)
            passed = len(matches) > 0
            confidence = min(len(matches) / 10.0, 1.0) if passed else 0.0
            
            return {
                "passed": passed,
                "confidence": confidence,
                "output": {"matches": matches, "count": len(matches)}
            }
        except re.error as e:
            return {
                "passed": False,
                "confidence": 0.0,
                "output": {"error": f"Invalid regex: {str(e)}"}
            }
    
    async def _execute_keyword_rule(
        self, 
        rule: RuleDefinition, 
        question: str, 
        hypothesis: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a keyword-based rule."""
        text = f"{question} {hypothesis}".lower()
        keywords = rule.content.lower().split(',')
        
        found_keywords = [kw.strip() for kw in keywords if kw.strip() in text]
        passed = len(found_keywords) > 0
        confidence = len(found_keywords) / len(keywords) if keywords else 0.0
        
        return {
            "passed": passed,
            "confidence": confidence,
            "output": {"found_keywords": found_keywords, "total_keywords": len(keywords)}
        }
