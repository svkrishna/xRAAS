"""
Scientific Validation Pilot for XReason
Handles research validation, mathematical proofs, statistical analysis, and scientific reasoning.
"""

import re
import math
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import statistics

from app.services.metrics_service import metrics_service


class ScientificDomain(Enum):
    MATHEMATICS = "mathematics"
    STATISTICS = "statistics"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    RESEARCH = "research"
    METHODOLOGY = "methodology"
    COMPUTER_SCIENCE = "computer_science"
    ENGINEERING = "engineering"
    MEDICINE = "medicine"
    PSYCHOLOGY = "psychology"
    ECONOMICS = "economics"


@dataclass
class ScientificIssue:
    """Represents a scientific issue found in analysis."""
    issue_id: str
    issue_type: str
    severity: str
    description: str
    evidence: str
    recommendation: str
    formula_reference: Optional[str] = None
    statistical_test: Optional[str] = None


@dataclass
class ScientificAnalysis:
    """Result of scientific validation analysis."""
    domain: ScientificDomain
    is_valid: bool
    confidence: float
    issues: List[ScientificIssue]
    recommendations: List[str]
    validity_score: float
    analysis_timestamp: datetime
    metadata: Dict[str, Any]


class ScientificValidationPilot:
    """Scientific validation analysis pilot for XReason."""
    
    def __init__(self):
        self.math_rules = self._load_math_rules()
        self.statistical_rules = self._load_statistical_rules()
        self.research_rules = self._load_research_rules()
        self.methodology_rules = self._load_methodology_rules()
        self.physics_rules = self._load_physics_rules()
        self.chemistry_rules = self._load_chemistry_rules()
        self.biology_rules = self._load_biology_rules()
        self.computer_science_rules = self._load_computer_science_rules()
        self.engineering_rules = self._load_engineering_rules()
        self.medicine_rules = self._load_medicine_rules()
        self.psychology_rules = self._load_psychology_rules()
        self.economics_rules = self._load_economics_rules()
        
    def _load_math_rules(self) -> Dict[str, Dict]:
        """Load mathematical validation rules."""
        return {
            "mathematical_consistency": {
                "name": "Mathematical Consistency",
                "description": "Check for mathematical consistency in calculations",
                "severity": "high",
                "patterns": [
                    r"(\d+)\s*[+\-*/]\s*(\d+)\s*=\s*(\d+)",
                    r"sqrt\((\d+)\)\s*=\s*(\d+)",
                    r"(\d+)\^(\d+)\s*=\s*(\d+)"
                ]
            },
            "unit_consistency": {
                "name": "Unit Consistency",
                "description": "Check for consistent units in calculations",
                "severity": "medium",
                "patterns": [
                    r"(\d+)\s*(kg|m|s|N|J|W)\s*[+\-*/]\s*(\d+)\s*(kg|m|s|N|J|W)",
                    r"(\d+)\s*(kg|m|s|N|J|W)\s*=\s*(\d+)\s*(kg|m|s|N|J|W)"
                ]
            },
            "formula_validation": {
                "name": "Formula Validation",
                "description": "Check if formulas are correctly applied",
                "severity": "high",
                "patterns": [
                    r"F\s*=\s*m\s*\*\s*a",
                    r"E\s*=\s*m\s*\*\s*c\^2",
                    r"P\s*=\s*F\s*/\s*A"
                ]
            }
        }
    
    def _load_statistical_rules(self) -> Dict[str, Dict]:
        """Load statistical validation rules."""
        return {
            "sample_size": {
                "name": "Sample Size Adequacy",
                "description": "Check if sample size is adequate for statistical tests",
                "severity": "high",
                "min_sample_size": 30
            },
            "p_value": {
                "name": "P-Value Significance",
                "description": "Check if p-values are properly interpreted",
                "severity": "high",
                "significance_level": 0.05
            },
            "confidence_interval": {
                "name": "Confidence Interval",
                "description": "Check if confidence intervals are properly calculated",
                "severity": "medium",
                "confidence_levels": [0.90, 0.95, 0.99]
            },
            "correlation_interpretation": {
                "name": "Correlation Interpretation",
                "description": "Check if correlations are properly interpreted",
                "severity": "medium",
                "correlation_thresholds": {
                    "weak": 0.3,
                    "moderate": 0.5,
                    "strong": 0.7
                }
            }
        }
    
    def _load_research_rules(self) -> Dict[str, Dict]:
        """Load research validation rules."""
        return {
            "hypothesis_testing": {
                "name": "Hypothesis Testing Framework",
                "description": "Check if proper hypothesis testing framework is used",
                "severity": "high",
                "keywords": ["hypothesis", "null hypothesis", "alternative hypothesis", "test statistic"]
            },
            "control_group": {
                "name": "Control Group",
                "description": "Check for proper control group in experiments",
                "severity": "high",
                "keywords": ["control", "control group", "baseline", "comparison"]
            },
            "randomization": {
                "name": "Randomization",
                "description": "Check for proper randomization in studies",
                "severity": "medium",
                "keywords": ["random", "randomization", "randomized", "randomly assigned"]
            },
            "blinding": {
                "name": "Blinding",
                "description": "Check for proper blinding in studies",
                "severity": "medium",
                "keywords": ["blind", "blinding", "double-blind", "single-blind"]
            },
            "replication": {
                "name": "Replication",
                "description": "Check for replication or reproducibility",
                "severity": "medium",
                "keywords": ["replicate", "replication", "reproducible", "reproducibility"]
            }
        }
    
    def _load_methodology_rules(self) -> Dict[str, Dict]:
        """Load methodology validation rules."""
        return {
            "research_design": {
                "name": "Research Design",
                "description": "Check for appropriate research design",
                "severity": "high",
                "keywords": ["experimental", "observational", "longitudinal", "cross-sectional"]
            },
            "data_collection": {
                "name": "Data Collection Methods",
                "description": "Check for appropriate data collection methods",
                "severity": "medium",
                "keywords": ["survey", "interview", "observation", "measurement", "instrument"]
            },
            "bias_assessment": {
                "name": "Bias Assessment",
                "description": "Check for bias assessment and mitigation",
                "severity": "high",
                "keywords": ["bias", "confounding", "selection bias", "measurement bias"]
            },
            "validity": {
                "name": "Validity Assessment",
                "description": "Check for validity assessment",
                "severity": "high",
                "keywords": ["validity", "internal validity", "external validity", "construct validity"]
            }
        }
    
    def _load_physics_rules(self) -> Dict[str, Dict]:
        """Load physics validation rules."""
        return {
            "conservation_laws": {
                "name": "Conservation Laws",
                "description": "Check for conservation of energy, momentum, and mass",
                "severity": "high",
                "keywords": ["conservation", "energy", "momentum", "mass", "law of conservation"],
                "formula_reference": "Conservation principles"
            },
            "dimensional_analysis": {
                "name": "Dimensional Analysis",
                "description": "Check for proper dimensional analysis",
                "severity": "medium",
                "keywords": ["dimension", "unit", "dimensional analysis", "si units"],
                "formula_reference": "Dimensional analysis"
            },
            "newton_laws": {
                "name": "Newton's Laws",
                "description": "Check for proper application of Newton's laws",
                "severity": "high",
                "keywords": ["newton", "force", "acceleration", "action", "reaction"],
                "formula_reference": "Newton's laws of motion"
            },
            "thermodynamics": {
                "name": "Thermodynamics",
                "description": "Check for thermodynamic principles",
                "severity": "high",
                "keywords": ["thermodynamics", "entropy", "energy", "heat", "work"],
                "formula_reference": "Laws of thermodynamics"
            }
        }
    
    def _load_chemistry_rules(self) -> Dict[str, Dict]:
        """Load chemistry validation rules."""
        return {
            "chemical_equations": {
                "name": "Chemical Equation Balance",
                "description": "Check for balanced chemical equations",
                "severity": "high",
                "keywords": ["chemical equation", "balance", "stoichiometry", "reaction"],
                "formula_reference": "Chemical stoichiometry"
            },
            "molecular_structure": {
                "name": "Molecular Structure",
                "description": "Check for valid molecular structures",
                "severity": "medium",
                "keywords": ["molecular", "structure", "bond", "valence", "electron"],
                "formula_reference": "Molecular bonding"
            },
            "reaction_kinetics": {
                "name": "Reaction Kinetics",
                "description": "Check for reaction kinetics principles",
                "severity": "medium",
                "keywords": ["kinetics", "rate", "reaction rate", "catalyst", "activation energy"],
                "formula_reference": "Chemical kinetics"
            },
            "equilibrium": {
                "name": "Chemical Equilibrium",
                "description": "Check for equilibrium principles",
                "severity": "high",
                "keywords": ["equilibrium", "equilibrium constant", "le chatelier", "concentration"],
                "formula_reference": "Chemical equilibrium"
            }
        }
    
    def _load_biology_rules(self) -> Dict[str, Dict]:
        """Load biology validation rules."""
        return {
            "cell_biology": {
                "name": "Cell Biology",
                "description": "Check for cell biology principles",
                "severity": "medium",
                "keywords": ["cell", "membrane", "organelle", "mitochondria", "nucleus"],
                "formula_reference": "Cell biology"
            },
            "genetics": {
                "name": "Genetics",
                "description": "Check for genetic principles",
                "severity": "high",
                "keywords": ["gene", "dna", "rna", "mutation", "inheritance", "allele"],
                "formula_reference": "Mendelian genetics"
            },
            "evolution": {
                "name": "Evolution",
                "description": "Check for evolutionary principles",
                "severity": "medium",
                "keywords": ["evolution", "natural selection", "adaptation", "speciation"],
                "formula_reference": "Evolutionary theory"
            },
            "ecology": {
                "name": "Ecology",
                "description": "Check for ecological principles",
                "severity": "medium",
                "keywords": ["ecosystem", "population", "community", "biodiversity", "food web"],
                "formula_reference": "Ecological principles"
            }
        }
    
    def _load_computer_science_rules(self) -> Dict[str, Dict]:
        """Load computer science validation rules."""
        return {
            "algorithm_complexity": {
                "name": "Algorithm Complexity",
                "description": "Check for proper algorithm complexity analysis",
                "severity": "high",
                "keywords": ["algorithm", "complexity", "big o", "time complexity", "space complexity"],
                "formula_reference": "Computational complexity theory"
            },
            "data_structures": {
                "name": "Data Structures",
                "description": "Check for appropriate data structure usage",
                "severity": "medium",
                "keywords": ["data structure", "array", "linked list", "tree", "graph", "hash table"],
                "formula_reference": "Data structure theory"
            },
            "software_engineering": {
                "name": "Software Engineering",
                "description": "Check for software engineering principles",
                "severity": "medium",
                "keywords": ["software engineering", "design pattern", "modularity", "testing", "documentation"],
                "formula_reference": "Software engineering principles"
            },
            "artificial_intelligence": {
                "name": "Artificial Intelligence",
                "description": "Check for AI/ML principles",
                "severity": "medium",
                "keywords": ["machine learning", "neural network", "algorithm", "training", "validation"],
                "formula_reference": "Machine learning theory"
            }
        }
    
    def _load_engineering_rules(self) -> Dict[str, Dict]:
        """Load engineering validation rules."""
        return {
            "structural_analysis": {
                "name": "Structural Analysis",
                "description": "Check for structural engineering principles",
                "severity": "high",
                "keywords": ["structural", "load", "stress", "strain", "safety factor"],
                "formula_reference": "Structural mechanics"
            },
            "fluid_dynamics": {
                "name": "Fluid Dynamics",
                "description": "Check for fluid dynamics principles",
                "severity": "medium",
                "keywords": ["fluid", "flow", "pressure", "velocity", "bernoulli"],
                "formula_reference": "Fluid mechanics"
            },
            "electrical_circuits": {
                "name": "Electrical Circuits",
                "description": "Check for electrical circuit principles",
                "severity": "high",
                "keywords": ["circuit", "voltage", "current", "resistance", "ohm's law"],
                "formula_reference": "Electrical circuit theory"
            },
            "control_systems": {
                "name": "Control Systems",
                "description": "Check for control system principles",
                "severity": "medium",
                "keywords": ["control system", "feedback", "stability", "transfer function"],
                "formula_reference": "Control theory"
            }
        }
    
    def _load_medicine_rules(self) -> Dict[str, Dict]:
        """Load medicine validation rules."""
        return {
            "clinical_trials": {
                "name": "Clinical Trial Design",
                "description": "Check for proper clinical trial design",
                "severity": "high",
                "keywords": ["clinical trial", "randomized", "placebo", "double-blind", "protocol"],
                "formula_reference": "Clinical trial methodology"
            },
            "epidemiology": {
                "name": "Epidemiology",
                "description": "Check for epidemiological principles",
                "severity": "medium",
                "keywords": ["epidemiology", "incidence", "prevalence", "risk factor", "cohort"],
                "formula_reference": "Epidemiological methods"
            },
            "pharmacology": {
                "name": "Pharmacology",
                "description": "Check for pharmacological principles",
                "severity": "high",
                "keywords": ["pharmacology", "dose", "concentration", "half-life", "metabolism"],
                "formula_reference": "Pharmacokinetics"
            },
            "anatomy_physiology": {
                "name": "Anatomy and Physiology",
                "description": "Check for anatomical and physiological principles",
                "severity": "medium",
                "keywords": ["anatomy", "physiology", "organ", "system", "function"],
                "formula_reference": "Human anatomy and physiology"
            }
        }
    
    def _load_psychology_rules(self) -> Dict[str, Dict]:
        """Load psychology validation rules."""
        return {
            "experimental_design": {
                "name": "Experimental Design",
                "description": "Check for proper experimental design in psychology",
                "severity": "high",
                "keywords": ["experimental design", "independent variable", "dependent variable", "control"],
                "formula_reference": "Psychological research methods"
            },
            "cognitive_psychology": {
                "name": "Cognitive Psychology",
                "description": "Check for cognitive psychology principles",
                "severity": "medium",
                "keywords": ["cognitive", "memory", "attention", "perception", "learning"],
                "formula_reference": "Cognitive psychology theory"
            },
            "behavioral_analysis": {
                "name": "Behavioral Analysis",
                "description": "Check for behavioral analysis principles",
                "severity": "medium",
                "keywords": ["behavior", "reinforcement", "conditioning", "stimulus", "response"],
                "formula_reference": "Behavioral psychology"
            },
            "psychometrics": {
                "name": "Psychometrics",
                "description": "Check for psychometric principles",
                "severity": "medium",
                "keywords": ["psychometrics", "reliability", "validity", "test", "measurement"],
                "formula_reference": "Psychometric theory"
            }
        }
    
    def _load_economics_rules(self) -> Dict[str, Dict]:
        """Load economics validation rules."""
        return {
            "microeconomics": {
                "name": "Microeconomics",
                "description": "Check for microeconomic principles",
                "severity": "medium",
                "keywords": ["supply", "demand", "price", "market", "elasticity", "utility"],
                "formula_reference": "Microeconomic theory"
            },
            "macroeconomics": {
                "name": "Macroeconomics",
                "description": "Check for macroeconomic principles",
                "severity": "medium",
                "keywords": ["gdp", "inflation", "unemployment", "monetary policy", "fiscal policy"],
                "formula_reference": "Macroeconomic theory"
            },
            "econometrics": {
                "name": "Econometrics",
                "description": "Check for econometric methods",
                "severity": "high",
                "keywords": ["regression", "correlation", "causation", "endogeneity", "heteroscedasticity"],
                "formula_reference": "Econometric methods"
            },
            "game_theory": {
                "name": "Game Theory",
                "description": "Check for game theory principles",
                "severity": "medium",
                "keywords": ["game theory", "nash equilibrium", "strategy", "payoff", "dominant strategy"],
                "formula_reference": "Game theory"
            }
        }
    
    async def analyze_mathematical_consistency(self, text: str, context: Optional[Dict] = None) -> ScientificAnalysis:
        """Analyze mathematical consistency in given text."""
        start_time = datetime.now()
        
        try:
            issues = []
            recommendations = []
            validity_score = 1.0
            
            # Check mathematical patterns
            for rule_id, rule in self.math_rules.items():
                patterns = rule.get("patterns", [])
                
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    
                    for match in matches:
                        if not self._validate_mathematical_expression(match, pattern):
                            issue = ScientificIssue(
                                issue_id=rule_id,
                                issue_type="mathematical_error",
                                severity=rule["severity"],
                                description=rule["description"],
                                evidence=f"Invalid expression: {match}",
                                recommendation="Verify mathematical calculations",
                                formula_reference=pattern
                            )
                            issues.append(issue)
                            validity_score -= 0.2
            
            # Generate recommendations
            if issues:
                recommendations = [
                    "Review all mathematical calculations",
                    "Verify unit consistency throughout",
                    "Check formula applications",
                    "Consider using mathematical software for verification"
                ]
            else:
                recommendations = [
                    "Mathematical expressions appear consistent",
                    "Consider peer review of calculations",
                    "Document calculation methods clearly"
                ]
            
            is_valid = len(issues) == 0
            confidence = max(0.1, validity_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("scientific", "math_analysis", duration)
            metrics_service.record_reasoning_confidence("scientific", "math_analysis", confidence)
            
            return ScientificAnalysis(
                domain=ScientificDomain.MATHEMATICS,
                is_valid=is_valid,
                confidence=confidence,
                issues=issues,
                recommendations=recommendations,
                validity_score=max(0.0, validity_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.math_rules),
                    "issues_found": len(issues),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("scientific", "math_analysis", str(e))
            raise
    
    async def analyze_statistical_validity(self, text: str, context: Optional[Dict] = None) -> ScientificAnalysis:
        """Analyze statistical validity in given text."""
        start_time = datetime.now()
        
        try:
            issues = []
            recommendations = []
            validity_score = 1.0
            
            # Extract statistical information
            stats_info = self._extract_statistical_info(text)
            
            # Check sample size
            if stats_info.get("sample_size", 0) < self.statistical_rules["sample_size"]["min_sample_size"]:
                issue = ScientificIssue(
                    issue_id="sample_size",
                    issue_type="statistical_issue",
                    severity="high",
                    description="Sample size may be inadequate",
                    evidence=f"Sample size: {stats_info.get('sample_size', 'unknown')}",
                    recommendation="Consider larger sample size or power analysis",
                    statistical_test="sample_size_adequacy"
                )
                issues.append(issue)
                validity_score -= 0.3
            
            # Check p-values
            p_values = stats_info.get("p_values", [])
            for p_val in p_values:
                if p_val < self.statistical_rules["p_value"]["significance_level"]:
                    # Significant result
                    pass
                else:
                    # Non-significant result - check if properly interpreted
                    if "significant" in text.lower() and p_val > 0.05:
                        issue = ScientificIssue(
                            issue_id="p_value_interpretation",
                            issue_type="statistical_issue",
                            severity="high",
                            description="Incorrect interpretation of non-significant p-value",
                            evidence=f"P-value: {p_val}",
                            recommendation="Correctly interpret non-significant results",
                            statistical_test="p_value_interpretation"
                        )
                        issues.append(issue)
                        validity_score -= 0.2
            
            # Check correlations
            correlations = stats_info.get("correlations", [])
            for corr in correlations:
                if abs(corr) > 0.7:
                    strength = "strong"
                elif abs(corr) > 0.5:
                    strength = "moderate"
                elif abs(corr) > 0.3:
                    strength = "weak"
                else:
                    strength = "very weak"
                
                # Check if interpretation matches strength
                if strength in ["weak", "very weak"] and "strong" in text.lower():
                    issue = ScientificIssue(
                        issue_id="correlation_interpretation",
                        issue_type="statistical_issue",
                        severity="medium",
                        description="Incorrect interpretation of correlation strength",
                        evidence=f"Correlation: {corr} (strength: {strength})",
                        recommendation="Correctly interpret correlation strength",
                        statistical_test="correlation_interpretation"
                    )
                    issues.append(issue)
                    validity_score -= 0.1
            
            # Generate recommendations
            if issues:
                recommendations = [
                    "Review statistical analysis methods",
                    "Ensure adequate sample sizes",
                    "Correctly interpret p-values and significance",
                    "Use appropriate statistical tests",
                    "Consider effect sizes alongside p-values"
                ]
            else:
                recommendations = [
                    "Statistical analysis appears valid",
                    "Consider reporting effect sizes",
                    "Document statistical methods clearly"
                ]
            
            is_valid = len(issues) == 0
            confidence = max(0.1, validity_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("scientific", "statistical_analysis", duration)
            metrics_service.record_reasoning_confidence("scientific", "statistical_analysis", confidence)
            
            return ScientificAnalysis(
                domain=ScientificDomain.STATISTICS,
                is_valid=is_valid,
                confidence=confidence,
                issues=issues,
                recommendations=recommendations,
                validity_score=max(0.0, validity_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.statistical_rules),
                    "issues_found": len(issues),
                    "analysis_duration": duration,
                    "statistical_info": stats_info
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("scientific", "statistical_analysis", str(e))
            raise
    
    async def analyze_research_methodology(self, text: str, context: Optional[Dict] = None) -> ScientificAnalysis:
        """Analyze research methodology in given text."""
        start_time = datetime.now()
        
        try:
            issues = []
            recommendations = []
            validity_score = 1.0
            
            # Check research rules
            for rule_id, rule in self.research_rules.items():
                keywords = rule.get("keywords", [])
                found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
                
                if len(found_keywords) < len(keywords) * 0.5:
                    issue = ScientificIssue(
                        issue_id=rule_id,
                        issue_type="methodology_issue",
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing keywords: {', '.join(set(keywords) - set(found_keywords))}",
                        recommendation=f"Address {rule['name'].lower()}",
                        statistical_test=None
                    )
                    issues.append(issue)
                    
                    if rule["severity"] == "high":
                        validity_score -= 0.3
                    else:
                        validity_score -= 0.1
            
            # Check methodology rules
            for rule_id, rule in self.methodology_rules.items():
                keywords = rule.get("keywords", [])
                found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
                
                if len(found_keywords) < len(keywords) * 0.5:
                    issue = ScientificIssue(
                        issue_id=rule_id,
                        issue_type="methodology_issue",
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing keywords: {', '.join(set(keywords) - set(found_keywords))}",
                        recommendation=f"Address {rule['name'].lower()}",
                        statistical_test=None
                    )
                    issues.append(issue)
                    
                    if rule["severity"] == "high":
                        validity_score -= 0.3
                    else:
                        validity_score -= 0.1
            
            # Generate recommendations
            if issues:
                recommendations = [
                    "Strengthen research methodology",
                    "Address missing methodological elements",
                    "Consider peer review of methodology",
                    "Document methodology clearly",
                    "Address potential biases and limitations"
                ]
            else:
                recommendations = [
                    "Research methodology appears sound",
                    "Consider documenting methodology more thoroughly",
                    "Address potential limitations explicitly"
                ]
            
            is_valid = len(issues) == 0
            confidence = max(0.1, validity_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("scientific", "methodology_analysis", duration)
            metrics_service.record_reasoning_confidence("scientific", "methodology_analysis", confidence)
            
            return ScientificAnalysis(
                domain=ScientificDomain.METHODOLOGY,
                is_valid=is_valid,
                confidence=confidence,
                issues=issues,
                recommendations=recommendations,
                validity_score=max(0.0, validity_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.research_rules) + len(self.methodology_rules),
                    "issues_found": len(issues),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("scientific", "methodology_analysis", str(e))
            raise
    
    def _validate_mathematical_expression(self, match: Tuple, pattern: str) -> bool:
        """Validate a mathematical expression."""
        try:
            if pattern == r"(\d+)\s*[+\-*/]\s*(\d+)\s*=\s*(\d+)":
                a, b, result = map(float, match)
                if '+' in pattern:
                    return abs(a + b - result) < 0.001
                elif '-' in pattern:
                    return abs(a - b - result) < 0.001
                elif '*' in pattern:
                    return abs(a * b - result) < 0.001
                elif '/' in pattern:
                    return abs(a / b - result) < 0.001
            elif pattern == r"sqrt\((\d+)\)\s*=\s*(\d+)":
                num, result = map(float, match)
                return abs(math.sqrt(num) - result) < 0.001
            elif pattern == r"(\d+)\^(\d+)\s*=\s*(\d+)":
                base, exp, result = map(float, match)
                return abs(base ** exp - result) < 0.001
            return True
        except:
            return False
    
    def _extract_statistical_info(self, text: str) -> Dict[str, Any]:
        """Extract statistical information from text."""
        info = {
            "sample_size": 0,
            "p_values": [],
            "correlations": [],
            "confidence_intervals": []
        }
        
        # Extract sample size
        sample_patterns = [
            r"n\s*=\s*(\d+)",
            r"sample\s+size\s*[=:]\s*(\d+)",
            r"(\d+)\s+participants",
            r"(\d+)\s+subjects"
        ]
        
        for pattern in sample_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    size = int(match)
                    info["sample_size"] = max(info["sample_size"], size)
                except:
                    pass
        
        # Extract p-values
        p_patterns = [
            r"p\s*[=<>]\s*([0-9.]+)",
            r"p-value\s*[=:]\s*([0-9.]+)",
            r"p\s*<\s*([0-9.]+)"
        ]
        
        for pattern in p_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    p_val = float(match)
                    if 0 <= p_val <= 1:
                        info["p_values"].append(p_val)
                except:
                    pass
        
        # Extract correlations
        corr_patterns = [
            r"r\s*=\s*([+-]?[0-9.]+)",
            r"correlation\s*[=:]\s*([+-]?[0-9.]+)",
            r"r\s*\([^)]*\)\s*=\s*([+-]?[0-9.]+)"
        ]
        
        for pattern in corr_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    corr = float(match)
                    if -1 <= corr <= 1:
                        info["correlations"].append(corr)
                except:
                    pass
        
        return info
    
    async def analyze_scientific_validity(self, text: str, domains: List[ScientificDomain] = None) -> Dict[str, ScientificAnalysis]:
        """Analyze scientific validity across multiple domains."""
        if domains is None:
            domains = [ScientificDomain.MATHEMATICS, ScientificDomain.STATISTICS, ScientificDomain.METHODOLOGY]
        
        results = {}
        
        for domain in domains:
            if domain == ScientificDomain.MATHEMATICS:
                results["mathematics"] = await self.analyze_mathematical_consistency(text)
            elif domain == ScientificDomain.STATISTICS:
                results["statistics"] = await self.analyze_statistical_validity(text)
            elif domain == ScientificDomain.METHODOLOGY:
                results["methodology"] = await self.analyze_research_methodology(text)
        
        return results


# Global instance
scientific_pilot = ScientificValidationPilot()
