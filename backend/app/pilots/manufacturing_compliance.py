"""
Manufacturing Compliance Pilot for XReason
Handles quality control, safety standards, environmental regulations, supply chain compliance, and manufacturing best practices.
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from app.services.metrics_service import metrics_service


class ManufacturingDomain(Enum):
    QUALITY_CONTROL = "quality_control"
    SAFETY_STANDARDS = "safety_standards"
    ENVIRONMENTAL = "environmental"
    SUPPLY_CHAIN = "supply_chain"
    ISO_STANDARDS = "iso_standards"
    LEAN_MANUFACTURING = "lean_manufacturing"
    AUTOMOTIVE = "automotive"
    AEROSPACE = "aerospace"


@dataclass
class ManufacturingViolation:
    """Represents a manufacturing compliance violation found in analysis."""
    rule_id: str
    rule_name: str
    severity: str
    description: str
    evidence: str
    recommendation: str
    standard_reference: Optional[str] = None
    penalty_info: Optional[str] = None
    risk_level: Optional[str] = None


@dataclass
class ManufacturingAnalysis:
    """Result of manufacturing compliance analysis."""
    domain: ManufacturingDomain
    is_compliant: bool
    confidence: float
    violations: List[ManufacturingViolation]
    recommendations: List[str]
    risk_score: float
    analysis_timestamp: datetime
    metadata: Dict[str, Any]


class ManufacturingCompliancePilot:
    """Manufacturing compliance analysis pilot for XReason."""
    
    def __init__(self):
        self.quality_control_rules = self._load_quality_control_rules()
        self.safety_standards_rules = self._load_safety_standards_rules()
        self.environmental_rules = self._load_environmental_rules()
        self.supply_chain_rules = self._load_supply_chain_rules()
        self.iso_standards_rules = self._load_iso_standards_rules()
        self.lean_manufacturing_rules = self._load_lean_manufacturing_rules()
        self.automotive_rules = self._load_automotive_rules()
        self.aerospace_rules = self._load_aerospace_rules()
    
    def _load_quality_control_rules(self) -> Dict[str, Dict]:
        """Load quality control compliance rules."""
        return {
            "statistical_process_control": {
                "name": "Statistical Process Control",
                "description": "Check for statistical process control implementation",
                "keywords": ["spc", "statistical process control", "control charts", "process capability", "six sigma"],
                "severity": "high",
                "standard": "ISO 7870",
                "penalty": "Quality issues and customer complaints",
                "risk_level": "high"
            },
            "inspection_procedures": {
                "name": "Inspection Procedures",
                "description": "Check for proper inspection procedures",
                "keywords": ["inspection", "quality inspection", "measurement", "calibration", "testing"],
                "severity": "high",
                "standard": "ISO 9001",
                "penalty": "Defective products and recalls",
                "risk_level": "high"
            },
            "documentation_control": {
                "name": "Documentation Control",
                "description": "Check for documentation control procedures",
                "keywords": ["documentation control", "document management", "version control", "change control"],
                "severity": "medium",
                "standard": "ISO 9001",
                "penalty": "Compliance issues",
                "risk_level": "medium"
            },
            "corrective_actions": {
                "name": "Corrective and Preventive Actions",
                "description": "Check for CAPA procedures",
                "keywords": ["capa", "corrective action", "preventive action", "root cause analysis", "nonconformity"],
                "severity": "high",
                "standard": "ISO 9001",
                "penalty": "Recurring quality issues",
                "risk_level": "high"
            },
            "training_competence": {
                "name": "Training and Competence",
                "description": "Check for training and competence requirements",
                "keywords": ["training", "competence", "qualification", "skills", "certification"],
                "severity": "medium",
                "standard": "ISO 9001",
                "penalty": "Human error and quality issues",
                "risk_level": "medium"
            }
        }
    
    def _load_safety_standards_rules(self) -> Dict[str, Dict]:
        """Load safety standards compliance rules."""
        return {
            "occupational_safety": {
                "name": "Occupational Safety",
                "description": "Check for occupational safety requirements",
                "keywords": ["occupational safety", "osha", "workplace safety", "hazard assessment", "ppe"],
                "severity": "critical",
                "standard": "OSHA Standards",
                "penalty": "Injuries, fatalities, and regulatory fines",
                "risk_level": "critical"
            },
            "machine_safety": {
                "name": "Machine Safety",
                "description": "Check for machine safety requirements",
                "keywords": ["machine safety", "guarding", "lockout tagout", "safety interlocks", "emergency stops"],
                "severity": "critical",
                "standard": "ISO 12100",
                "penalty": "Serious injuries and regulatory action",
                "risk_level": "critical"
            },
            "chemical_safety": {
                "name": "Chemical Safety",
                "description": "Check for chemical safety requirements",
                "keywords": ["chemical safety", "hazmat", "sds", "chemical handling", "ventilation"],
                "severity": "high",
                "standard": "OSHA HazCom",
                "penalty": "Chemical exposure and regulatory fines",
                "risk_level": "high"
            },
            "fire_safety": {
                "name": "Fire Safety",
                "description": "Check for fire safety requirements",
                "keywords": ["fire safety", "fire prevention", "fire suppression", "emergency evacuation", "fire alarms"],
                "severity": "high",
                "standard": "NFPA Standards",
                "penalty": "Fire incidents and regulatory action",
                "risk_level": "high"
            },
            "ergonomics": {
                "name": "Ergonomics",
                "description": "Check for ergonomic requirements",
                "keywords": ["ergonomics", "workplace design", "manual handling", "repetitive motion", "musculoskeletal"],
                "severity": "medium",
                "standard": "OSHA Ergonomics",
                "penalty": "Workplace injuries",
                "risk_level": "medium"
            }
        }
    
    def _load_environmental_rules(self) -> Dict[str, Dict]:
        """Load environmental compliance rules."""
        return {
            "waste_management": {
                "name": "Waste Management",
                "description": "Check for waste management requirements",
                "keywords": ["waste management", "hazardous waste", "recycling", "waste disposal", "waste reduction"],
                "severity": "high",
                "standard": "EPA Regulations",
                "penalty": "Environmental violations and fines",
                "risk_level": "high"
            },
            "air_emissions": {
                "name": "Air Emissions Control",
                "description": "Check for air emissions control",
                "keywords": ["air emissions", "air quality", "emissions control", "clean air act", "permit"],
                "severity": "high",
                "standard": "Clean Air Act",
                "penalty": "Environmental violations and fines",
                "risk_level": "high"
            },
            "water_management": {
                "name": "Water Management",
                "description": "Check for water management requirements",
                "keywords": ["water management", "wastewater", "water quality", "discharge permit", "water conservation"],
                "severity": "high",
                "standard": "Clean Water Act",
                "penalty": "Environmental violations and fines",
                "risk_level": "high"
            },
            "energy_efficiency": {
                "name": "Energy Efficiency",
                "description": "Check for energy efficiency requirements",
                "keywords": ["energy efficiency", "energy management", "energy conservation", "energy audit"],
                "severity": "medium",
                "standard": "ISO 50001",
                "penalty": "Higher energy costs",
                "risk_level": "medium"
            },
            "sustainability": {
                "name": "Sustainability Practices",
                "description": "Check for sustainability practices",
                "keywords": ["sustainability", "green manufacturing", "carbon footprint", "life cycle assessment"],
                "severity": "medium",
                "standard": "ISO 14001",
                "penalty": "Reputational damage",
                "risk_level": "medium"
            }
        }
    
    def _load_supply_chain_rules(self) -> Dict[str, Dict]:
        """Load supply chain compliance rules."""
        return {
            "supplier_qualification": {
                "name": "Supplier Qualification",
                "description": "Check for supplier qualification procedures",
                "keywords": ["supplier qualification", "supplier assessment", "supplier audit", "approved suppliers"],
                "severity": "high",
                "standard": "ISO 9001",
                "penalty": "Quality issues and supply disruptions",
                "risk_level": "high"
            },
            "traceability": {
                "name": "Traceability Requirements",
                "description": "Check for traceability requirements",
                "keywords": ["traceability", "lot tracking", "serial numbers", "batch tracking", "supply chain visibility"],
                "severity": "high",
                "standard": "ISO 9001",
                "penalty": "Recall difficulties and compliance issues",
                "risk_level": "high"
            },
            "inventory_management": {
                "name": "Inventory Management",
                "description": "Check for inventory management procedures",
                "keywords": ["inventory management", "stock control", "just in time", "kanban", "inventory accuracy"],
                "severity": "medium",
                "standard": "Lean Manufacturing",
                "penalty": "Stockouts and excess inventory",
                "risk_level": "medium"
            },
            "logistics_compliance": {
                "name": "Logistics Compliance",
                "description": "Check for logistics compliance requirements",
                "keywords": ["logistics", "transportation", "shipping", "customs", "import export"],
                "severity": "medium",
                "standard": "Various regulations",
                "penalty": "Shipping delays and customs issues",
                "risk_level": "medium"
            },
            "risk_management": {
                "name": "Supply Chain Risk Management",
                "description": "Check for supply chain risk management",
                "keywords": ["risk management", "supply chain risk", "business continuity", "contingency planning"],
                "severity": "high",
                "standard": "ISO 31000",
                "penalty": "Supply disruptions",
                "risk_level": "high"
            }
        }
    
    def _load_iso_standards_rules(self) -> Dict[str, Dict]:
        """Load ISO standards compliance rules."""
        return {
            "iso_9001": {
                "name": "ISO 9001 Quality Management",
                "description": "Check for ISO 9001 quality management system",
                "keywords": ["iso 9001", "quality management system", "qms", "process approach", "continual improvement"],
                "severity": "high",
                "standard": "ISO 9001:2015",
                "penalty": "Loss of certification",
                "risk_level": "high"
            },
            "iso_14001": {
                "name": "ISO 14001 Environmental Management",
                "description": "Check for ISO 14001 environmental management system",
                "keywords": ["iso 14001", "environmental management system", "ems", "environmental policy", "environmental objectives"],
                "severity": "high",
                "standard": "ISO 14001:2015",
                "penalty": "Loss of certification",
                "risk_level": "high"
            },
            "iso_45001": {
                "name": "ISO 45001 Occupational Health and Safety",
                "description": "Check for ISO 45001 occupational health and safety management",
                "keywords": ["iso 45001", "occupational health and safety", "ohs", "safety management system"],
                "severity": "high",
                "standard": "ISO 45001:2018",
                "penalty": "Loss of certification",
                "risk_level": "high"
            },
            "iso_27001": {
                "name": "ISO 27001 Information Security",
                "description": "Check for ISO 27001 information security management",
                "keywords": ["iso 27001", "information security", "cybersecurity", "data protection", "security controls"],
                "severity": "high",
                "standard": "ISO 27001:2013",
                "penalty": "Loss of certification",
                "risk_level": "high"
            },
            "iso_50001": {
                "name": "ISO 50001 Energy Management",
                "description": "Check for ISO 50001 energy management system",
                "keywords": ["iso 50001", "energy management", "energy efficiency", "energy policy", "energy objectives"],
                "severity": "medium",
                "standard": "ISO 50001:2018",
                "penalty": "Loss of certification",
                "risk_level": "medium"
            }
        }
    
    def _load_lean_manufacturing_rules(self) -> Dict[str, Dict]:
        """Load lean manufacturing compliance rules."""
        return {
            "waste_elimination": {
                "name": "Waste Elimination",
                "description": "Check for waste elimination practices",
                "keywords": ["waste elimination", "muda", "seven wastes", "value stream", "lean principles"],
                "severity": "medium",
                "standard": "Lean Manufacturing",
                "penalty": "Inefficiency and higher costs",
                "risk_level": "medium"
            },
            "continuous_improvement": {
                "name": "Continuous Improvement",
                "description": "Check for continuous improvement practices",
                "keywords": ["continuous improvement", "kaizen", "pdca", "improvement culture", "problem solving"],
                "severity": "medium",
                "standard": "Lean Manufacturing",
                "penalty": "Stagnation and competitive disadvantage",
                "risk_level": "medium"
            },
            "standardized_work": {
                "name": "Standardized Work",
                "description": "Check for standardized work procedures",
                "keywords": ["standardized work", "work instructions", "standard operating procedures", "sop"],
                "severity": "high",
                "standard": "Lean Manufacturing",
                "penalty": "Variability and quality issues",
                "risk_level": "high"
            },
            "visual_management": {
                "name": "Visual Management",
                "description": "Check for visual management practices",
                "keywords": ["visual management", "5s", "visual controls", "kanban", "visual workplace"],
                "severity": "medium",
                "standard": "Lean Manufacturing",
                "penalty": "Disorganization and inefficiency",
                "risk_level": "medium"
            },
            "pull_system": {
                "name": "Pull System",
                "description": "Check for pull system implementation",
                "keywords": ["pull system", "just in time", "jit", "demand driven", "flow"],
                "severity": "medium",
                "standard": "Lean Manufacturing",
                "penalty": "Excess inventory and waste",
                "risk_level": "medium"
            }
        }
    
    def _load_automotive_rules(self) -> Dict[str, Dict]:
        """Load automotive industry compliance rules."""
        return {
            "iatf_16949": {
                "name": "IATF 16949 Automotive Quality Management",
                "description": "Check for IATF 16949 automotive quality management system",
                "keywords": ["iatf 16949", "automotive quality", "automotive qms", "automotive standards"],
                "severity": "critical",
                "standard": "IATF 16949:2016",
                "penalty": "Loss of automotive business",
                "risk_level": "critical"
            },
            "apqp": {
                "name": "Advanced Product Quality Planning",
                "description": "Check for APQP implementation",
                "keywords": ["apqp", "advanced product quality planning", "product development", "quality planning"],
                "severity": "high",
                "standard": "AIAG APQP",
                "penalty": "Product development delays",
                "risk_level": "high"
            },
            "ppap": {
                "name": "Production Part Approval Process",
                "description": "Check for PPAP requirements",
                "keywords": ["ppap", "production part approval process", "part approval", "customer approval"],
                "severity": "high",
                "standard": "AIAG PPAP",
                "penalty": "Customer rejection",
                "risk_level": "high"
            },
            "fmea": {
                "name": "Failure Mode and Effects Analysis",
                "description": "Check for FMEA implementation",
                "keywords": ["fmea", "failure mode", "risk analysis", "design fmea", "process fmea"],
                "severity": "high",
                "standard": "AIAG FMEA",
                "penalty": "Product failures and recalls",
                "risk_level": "high"
            },
            "msa": {
                "name": "Measurement System Analysis",
                "description": "Check for MSA requirements",
                "keywords": ["msa", "measurement system analysis", "gage r&r", "measurement capability"],
                "severity": "medium",
                "standard": "AIAG MSA",
                "penalty": "Measurement errors",
                "risk_level": "medium"
            }
        }
    
    def _load_aerospace_rules(self) -> Dict[str, Dict]:
        """Load aerospace industry compliance rules."""
        return {
            "as9100": {
                "name": "AS9100 Aerospace Quality Management",
                "description": "Check for AS9100 aerospace quality management system",
                "keywords": ["as9100", "aerospace quality", "aerospace qms", "aerospace standards"],
                "severity": "critical",
                "standard": "AS9100D",
                "penalty": "Loss of aerospace business",
                "risk_level": "critical"
            },
            "configuration_management": {
                "name": "Configuration Management",
                "description": "Check for configuration management requirements",
                "keywords": ["configuration management", "change control", "version control", "documentation control"],
                "severity": "high",
                "standard": "AS9100D",
                "penalty": "Configuration errors",
                "risk_level": "high"
            },
            "special_processes": {
                "name": "Special Processes",
                "description": "Check for special processes requirements",
                "keywords": ["special processes", "welding", "heat treatment", "non-destructive testing", "ndt"],
                "severity": "high",
                "standard": "AS9100D",
                "penalty": "Process failures",
                "risk_level": "high"
            },
            "first_article_inspection": {
                "name": "First Article Inspection",
                "description": "Check for first article inspection requirements",
                "keywords": ["first article inspection", "fai", "first article", "inspection requirements"],
                "severity": "high",
                "standard": "AS9102",
                "penalty": "Customer rejection",
                "risk_level": "high"
            },
            "counterfeit_parts": {
                "name": "Counterfeit Parts Prevention",
                "description": "Check for counterfeit parts prevention",
                "keywords": ["counterfeit parts", "obsolescence management", "supply chain security", "authenticity"],
                "severity": "critical",
                "standard": "AS6174",
                "penalty": "Safety incidents and regulatory action",
                "risk_level": "critical"
            }
        }
    
    def _check_rule_violation(self, text: str, rule: Dict) -> bool:
        """Check if text violates a specific rule."""
        text_lower = text.lower()
        keywords = rule.get("keywords", [])
        
        # Check if any keywords are missing
        missing_keywords = []
        for keyword in keywords:
            if keyword.lower() not in text_lower:
                missing_keywords.append(keyword)
        
        # If more than 50% of keywords are missing, consider it a violation
        return len(missing_keywords) > len(keywords) * 0.5
    
    async def analyze_quality_control(self, text: str, context: Optional[Dict] = None) -> ManufacturingAnalysis:
        """Analyze quality control compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each quality control rule
            for rule_id, rule in self.quality_control_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = ManufacturingViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        standard_reference=rule.get("standard"),
                        penalty_info=rule.get("penalty"),
                        risk_level=rule.get("risk_level")
                    )
                    violations.append(violation)
                    
                    # Calculate risk score
                    if rule["severity"] == "critical":
                        risk_score += 0.4
                    elif rule["severity"] == "high":
                        risk_score += 0.3
                    elif rule["severity"] == "medium":
                        risk_score += 0.2
                    else:
                        risk_score += 0.1
            
            # Generate recommendations
            if violations:
                recommendations = [
                    "Conduct comprehensive quality control audit",
                    "Implement statistical process control",
                    "Establish inspection procedures",
                    "Train staff on quality requirements",
                    "Review and update quality documentation"
                ]
            else:
                recommendations = [
                    "Maintain current quality control practices",
                    "Regularly review quality standards",
                    "Conduct periodic quality training"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("manufacturing", "quality_control_analysis", duration)
            metrics_service.record_reasoning_confidence("manufacturing", "quality_control_analysis", confidence)
            
            return ManufacturingAnalysis(
                domain=ManufacturingDomain.QUALITY_CONTROL,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.quality_control_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("manufacturing", "quality_control_analysis", str(e))
            raise
    
    async def analyze_safety_standards(self, text: str, context: Optional[Dict] = None) -> ManufacturingAnalysis:
        """Analyze safety standards compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each safety standards rule
            for rule_id, rule in self.safety_standards_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = ManufacturingViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        standard_reference=rule.get("standard"),
                        penalty_info=rule.get("penalty"),
                        risk_level=rule.get("risk_level")
                    )
                    violations.append(violation)
                    
                    # Calculate risk score
                    if rule["severity"] == "critical":
                        risk_score += 0.4
                    elif rule["severity"] == "high":
                        risk_score += 0.3
                    elif rule["severity"] == "medium":
                        risk_score += 0.2
                    else:
                        risk_score += 0.1
            
            # Generate recommendations
            if violations:
                recommendations = [
                    "Conduct comprehensive safety audit",
                    "Implement safety management system",
                    "Establish safety training programs",
                    "Review and update safety procedures",
                    "Conduct hazard assessments"
                ]
            else:
                recommendations = [
                    "Maintain current safety practices",
                    "Regularly review safety standards",
                    "Conduct periodic safety training"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("manufacturing", "safety_standards_analysis", duration)
            metrics_service.record_reasoning_confidence("manufacturing", "safety_standards_analysis", confidence)
            
            return ManufacturingAnalysis(
                domain=ManufacturingDomain.SAFETY_STANDARDS,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.safety_standards_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("manufacturing", "safety_standards_analysis", str(e))
            raise
    
    async def analyze_environmental_compliance(self, text: str, context: Optional[Dict] = None) -> ManufacturingAnalysis:
        """Analyze environmental compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each environmental rule
            for rule_id, rule in self.environmental_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = ManufacturingViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        standard_reference=rule.get("standard"),
                        penalty_info=rule.get("penalty"),
                        risk_level=rule.get("risk_level")
                    )
                    violations.append(violation)
                    
                    # Calculate risk score
                    if rule["severity"] == "critical":
                        risk_score += 0.4
                    elif rule["severity"] == "high":
                        risk_score += 0.3
                    elif rule["severity"] == "medium":
                        risk_score += 0.2
                    else:
                        risk_score += 0.1
            
            # Generate recommendations
            if violations:
                recommendations = [
                    "Conduct comprehensive environmental audit",
                    "Implement environmental management system",
                    "Establish waste management procedures",
                    "Train staff on environmental requirements",
                    "Review and update environmental procedures"
                ]
            else:
                recommendations = [
                    "Maintain current environmental practices",
                    "Regularly review environmental regulations",
                    "Conduct periodic environmental training"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("manufacturing", "environmental_analysis", duration)
            metrics_service.record_reasoning_confidence("manufacturing", "environmental_analysis", confidence)
            
            return ManufacturingAnalysis(
                domain=ManufacturingDomain.ENVIRONMENTAL,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.environmental_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("manufacturing", "environmental_analysis", str(e))
            raise
    
    async def analyze_comprehensive_manufacturing(self, text: str, context: Optional[Dict] = None) -> Dict[str, ManufacturingAnalysis]:
        """Analyze comprehensive manufacturing compliance across all domains."""
        results = {}
        
        # Analyze each domain
        results["quality_control"] = await self.analyze_quality_control(text, context)
        results["safety_standards"] = await self.analyze_safety_standards(text, context)
        results["environmental"] = await self.analyze_environmental_compliance(text, context)
        
        return results


# Global instance
manufacturing_pilot = ManufacturingCompliancePilot()
