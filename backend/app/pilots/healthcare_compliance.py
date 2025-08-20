"""
Healthcare Compliance Pilot for XReason
Handles HIPAA, FDA, clinical trials, medical devices, and healthcare quality compliance.
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from app.services.metrics_service import metrics_service


class HealthcareDomain(Enum):
    HIPAA = "hipaa"
    FDA = "fda"
    CLINICAL_TRIALS = "clinical_trials"
    MEDICAL_DEVICES = "medical_devices"
    QUALITY_STANDARDS = "quality_standards"
    PHARMACY = "pharmacy"
    LABORATORY = "laboratory"
    EMERGENCY_MEDICINE = "emergency_medicine"


@dataclass
class HealthcareViolation:
    """Represents a healthcare compliance violation found in analysis."""
    rule_id: str
    rule_name: str
    severity: str
    description: str
    evidence: str
    recommendation: str
    regulation_reference: Optional[str] = None
    penalty_info: Optional[str] = None
    risk_level: Optional[str] = None


@dataclass
class HealthcareAnalysis:
    """Result of healthcare compliance analysis."""
    domain: HealthcareDomain
    is_compliant: bool
    confidence: float
    violations: List[HealthcareViolation]
    recommendations: List[str]
    risk_score: float
    analysis_timestamp: datetime
    metadata: Dict[str, Any]


class HealthcareCompliancePilot:
    """Healthcare compliance analysis pilot for XReason."""
    
    def __init__(self):
        self.hipaa_rules = self._load_hipaa_rules()
        self.fda_rules = self._load_fda_rules()
        self.clinical_trial_rules = self._load_clinical_trial_rules()
        self.medical_device_rules = self._load_medical_device_rules()
        self.quality_standards_rules = self._load_quality_standards_rules()
        self.pharmacy_rules = self._load_pharmacy_rules()
        self.laboratory_rules = self._load_laboratory_rules()
        self.emergency_medicine_rules = self._load_emergency_medicine_rules()
    
    def _load_hipaa_rules(self) -> Dict[str, Dict]:
        """Load HIPAA compliance rules."""
        return {
            "hipaa_privacy_rule": {
                "name": "Privacy Rule Compliance",
                "description": "Check for proper privacy safeguards for PHI",
                "keywords": ["privacy", "confidential", "protected health information", "phi", "patient privacy"],
                "severity": "high",
                "regulation": "45 CFR 164.312(a)(1)",
                "penalty": "Up to $50,000 per violation",
                "risk_level": "high"
            },
            "hipaa_security_rule": {
                "name": "Security Rule Compliance",
                "description": "Check for technical and physical safeguards",
                "keywords": ["security", "encryption", "access control", "audit", "technical safeguards"],
                "severity": "high",
                "regulation": "45 CFR 164.312(c)(1)",
                "penalty": "Up to $50,000 per violation",
                "risk_level": "high"
            },
            "hipaa_breach_notification": {
                "name": "Breach Notification Rule",
                "description": "Check for breach notification procedures",
                "keywords": ["breach", "notification", "60 days", "report", "breach notification"],
                "severity": "critical",
                "regulation": "45 CFR 164.400-414",
                "penalty": "Up to $50,000 per violation",
                "risk_level": "critical"
            },
            "hipaa_business_associate": {
                "name": "Business Associate Agreements",
                "description": "Check for proper BAAs",
                "keywords": ["business associate", "baa", "agreement", "contract", "business associate agreement"],
                "severity": "medium",
                "regulation": "45 CFR 164.308(b)(1)",
                "penalty": "Up to $50,000 per violation",
                "risk_level": "medium"
            },
            "hipaa_minimum_necessary": {
                "name": "Minimum Necessary Standard",
                "description": "Check for minimum necessary use and disclosure",
                "keywords": ["minimum necessary", "need to know", "limited access", "role-based"],
                "severity": "high",
                "regulation": "45 CFR 164.502(b)",
                "penalty": "Up to $50,000 per violation",
                "risk_level": "high"
            },
            "hipaa_authorization": {
                "name": "Patient Authorization",
                "description": "Check for proper patient authorization procedures",
                "keywords": ["authorization", "patient consent", "written authorization", "patient rights"],
                "severity": "high",
                "regulation": "45 CFR 164.508",
                "penalty": "Up to $50,000 per violation",
                "risk_level": "high"
            }
        }
    
    def _load_fda_rules(self) -> Dict[str, Dict]:
        """Load FDA compliance rules."""
        return {
            "fda_drug_approval": {
                "name": "Drug Approval Process",
                "description": "Check for proper FDA drug approval process",
                "keywords": ["fda approval", "new drug application", "nda", "clinical trials", "safety"],
                "severity": "critical",
                "regulation": "21 CFR 314",
                "penalty": "Up to $250,000 per violation",
                "risk_level": "critical"
            },
            "fda_device_approval": {
                "name": "Medical Device Approval",
                "description": "Check for proper FDA device approval process",
                "keywords": ["fda approval", "medical device", "510k", "pma", "class i", "class ii", "class iii"],
                "severity": "critical",
                "regulation": "21 CFR 807",
                "penalty": "Up to $250,000 per violation",
                "risk_level": "critical"
            },
            "fda_labeling": {
                "name": "Product Labeling Requirements",
                "description": "Check for proper product labeling",
                "keywords": ["labeling", "package insert", "indications", "contraindications", "warnings"],
                "severity": "high",
                "regulation": "21 CFR 201",
                "penalty": "Up to $100,000 per violation",
                "risk_level": "high"
            },
            "fda_adverse_events": {
                "name": "Adverse Event Reporting",
                "description": "Check for adverse event reporting procedures",
                "keywords": ["adverse event", "medwatch", "reporting", "side effects", "safety"],
                "severity": "high",
                "regulation": "21 CFR 314.80",
                "penalty": "Up to $100,000 per violation",
                "risk_level": "high"
            },
            "fda_gmp": {
                "name": "Good Manufacturing Practices",
                "description": "Check for GMP compliance",
                "keywords": ["gmp", "good manufacturing practices", "quality control", "manufacturing"],
                "severity": "high",
                "regulation": "21 CFR 210-211",
                "penalty": "Up to $100,000 per violation",
                "risk_level": "high"
            }
        }
    
    def _load_clinical_trial_rules(self) -> Dict[str, Dict]:
        """Load clinical trial compliance rules."""
        return {
            "informed_consent": {
                "name": "Informed Consent",
                "description": "Check for proper informed consent procedures",
                "keywords": ["informed consent", "consent form", "voluntary", "comprehension", "disclosure"],
                "severity": "critical",
                "regulation": "21 CFR 50",
                "penalty": "Up to $250,000 per violation",
                "risk_level": "critical"
            },
            "irb_approval": {
                "name": "IRB Approval",
                "description": "Check for IRB approval requirements",
                "keywords": ["irb", "institutional review board", "ethics committee", "protocol approval"],
                "severity": "critical",
                "regulation": "21 CFR 56",
                "penalty": "Up to $250,000 per violation",
                "risk_level": "critical"
            },
            "protocol_compliance": {
                "name": "Protocol Compliance",
                "description": "Check for protocol compliance",
                "keywords": ["protocol", "study protocol", "protocol deviation", "compliance"],
                "severity": "high",
                "regulation": "21 CFR 312",
                "penalty": "Up to $100,000 per violation",
                "risk_level": "high"
            },
            "data_integrity": {
                "name": "Data Integrity",
                "description": "Check for data integrity in clinical trials",
                "keywords": ["data integrity", "source documents", "case report forms", "audit trail"],
                "severity": "high",
                "regulation": "21 CFR 312",
                "penalty": "Up to $100,000 per violation",
                "risk_level": "high"
            },
            "safety_monitoring": {
                "name": "Safety Monitoring",
                "description": "Check for safety monitoring procedures",
                "keywords": ["safety monitoring", "dsmb", "data safety monitoring board", "safety"],
                "severity": "high",
                "regulation": "21 CFR 312",
                "penalty": "Up to $100,000 per violation",
                "risk_level": "high"
            }
        }
    
    def _load_medical_device_rules(self) -> Dict[str, Dict]:
        """Load medical device compliance rules."""
        return {
            "device_classification": {
                "name": "Device Classification",
                "description": "Check for proper device classification",
                "keywords": ["class i", "class ii", "class iii", "device classification", "risk"],
                "severity": "high",
                "regulation": "21 CFR 860",
                "penalty": "Up to $100,000 per violation",
                "risk_level": "high"
            },
            "device_registration": {
                "name": "Device Registration",
                "description": "Check for device registration requirements",
                "keywords": ["device registration", "establishment registration", "fda registration"],
                "severity": "medium",
                "regulation": "21 CFR 807",
                "penalty": "Up to $50,000 per violation",
                "risk_level": "medium"
            },
            "device_labeling": {
                "name": "Device Labeling",
                "description": "Check for device labeling requirements",
                "keywords": ["device labeling", "instructions for use", "ifu", "labeling"],
                "severity": "high",
                "regulation": "21 CFR 801",
                "penalty": "Up to $100,000 per violation",
                "risk_level": "high"
            },
            "device_reporting": {
                "name": "Device Reporting",
                "description": "Check for device reporting requirements",
                "keywords": ["device reporting", "maude", "adverse event", "malfunction"],
                "severity": "high",
                "regulation": "21 CFR 803",
                "penalty": "Up to $100,000 per violation",
                "risk_level": "high"
            },
            "quality_system": {
                "name": "Quality System Regulation",
                "description": "Check for quality system compliance",
                "keywords": ["quality system", "qsr", "quality management", "iso 13485"],
                "severity": "high",
                "regulation": "21 CFR 820",
                "penalty": "Up to $100,000 per violation",
                "risk_level": "high"
            }
        }
    
    def _load_quality_standards_rules(self) -> Dict[str, Dict]:
        """Load healthcare quality standards rules."""
        return {
            "joint_commission": {
                "name": "Joint Commission Standards",
                "description": "Check for Joint Commission accreditation standards",
                "keywords": ["joint commission", "jcaho", "accreditation", "standards", "quality"],
                "severity": "high",
                "regulation": "Joint Commission Standards",
                "penalty": "Loss of accreditation",
                "risk_level": "high"
            },
            "iso_9001": {
                "name": "ISO 9001 Quality Management",
                "description": "Check for ISO 9001 quality management system",
                "keywords": ["iso 9001", "quality management", "process improvement", "customer focus"],
                "severity": "medium",
                "regulation": "ISO 9001:2015",
                "penalty": "Loss of certification",
                "risk_level": "medium"
            },
            "six_sigma": {
                "name": "Six Sigma Quality",
                "description": "Check for Six Sigma quality standards",
                "keywords": ["six sigma", "quality improvement", "defect reduction", "process improvement"],
                "severity": "medium",
                "regulation": "Six Sigma Methodology",
                "penalty": "Quality issues",
                "risk_level": "medium"
            },
            "lean_healthcare": {
                "name": "Lean Healthcare",
                "description": "Check for Lean healthcare principles",
                "keywords": ["lean", "waste reduction", "value stream", "continuous improvement"],
                "severity": "medium",
                "regulation": "Lean Methodology",
                "penalty": "Inefficiency",
                "risk_level": "medium"
            }
        }
    
    def _load_pharmacy_rules(self) -> Dict[str, Dict]:
        """Load pharmacy compliance rules."""
        return {
            "prescription_requirements": {
                "name": "Prescription Requirements",
                "description": "Check for prescription requirements",
                "keywords": ["prescription", "rx", "prescriber", "dosage", "directions"],
                "severity": "high",
                "regulation": "State Pharmacy Laws",
                "penalty": "License suspension",
                "risk_level": "high"
            },
            "drug_interactions": {
                "name": "Drug Interaction Screening",
                "description": "Check for drug interaction screening",
                "keywords": ["drug interaction", "contraindication", "drug-drug interaction", "screening"],
                "severity": "critical",
                "regulation": "Pharmacy Practice Standards",
                "penalty": "Patient harm",
                "risk_level": "critical"
            },
            "controlled_substances": {
                "name": "Controlled Substances",
                "description": "Check for controlled substance compliance",
                "keywords": ["controlled substance", "schedule", "dea", "narcotic", "opioid"],
                "severity": "critical",
                "regulation": "21 CFR 1300",
                "penalty": "Criminal charges",
                "risk_level": "critical"
            },
            "compounding": {
                "name": "Compounding Standards",
                "description": "Check for compounding standards",
                "keywords": ["compounding", "sterile compounding", "usp", "beyond-use date"],
                "severity": "high",
                "regulation": "USP 795/797",
                "penalty": "License suspension",
                "risk_level": "high"
            }
        }
    
    def _load_laboratory_rules(self) -> Dict[str, Dict]:
        """Load laboratory compliance rules."""
        return {
            "clia_compliance": {
                "name": "CLIA Compliance",
                "description": "Check for CLIA compliance",
                "keywords": ["clia", "clinical laboratory", "certification", "proficiency testing"],
                "severity": "high",
                "regulation": "42 CFR 493",
                "penalty": "Loss of certification",
                "risk_level": "high"
            },
            "quality_control": {
                "name": "Quality Control",
                "description": "Check for quality control procedures",
                "keywords": ["quality control", "qc", "calibration", "validation", "verification"],
                "severity": "high",
                "regulation": "CLIA Standards",
                "penalty": "Quality issues",
                "risk_level": "high"
            },
            "result_reporting": {
                "name": "Result Reporting",
                "description": "Check for result reporting requirements",
                "keywords": ["result reporting", "critical values", "turnaround time", "reporting"],
                "severity": "high",
                "regulation": "CLIA Standards",
                "penalty": "Patient harm",
                "risk_level": "high"
            },
            "specimen_handling": {
                "name": "Specimen Handling",
                "description": "Check for specimen handling procedures",
                "keywords": ["specimen", "collection", "transport", "storage", "chain of custody"],
                "severity": "medium",
                "regulation": "CLIA Standards",
                "penalty": "Quality issues",
                "risk_level": "medium"
            }
        }
    
    def _load_emergency_medicine_rules(self) -> Dict[str, Dict]:
        """Load emergency medicine compliance rules."""
        return {
            "emtala": {
                "name": "EMTALA Compliance",
                "description": "Check for EMTALA compliance",
                "keywords": ["emtala", "emergency", "stabilization", "transfer", "dumping"],
                "severity": "critical",
                "regulation": "42 CFR 489",
                "penalty": "Up to $50,000 per violation",
                "risk_level": "critical"
            },
            "emergency_protocols": {
                "name": "Emergency Protocols",
                "description": "Check for emergency protocols",
                "keywords": ["emergency protocol", "code", "resuscitation", "trauma", "emergency"],
                "severity": "high",
                "regulation": "Emergency Medicine Standards",
                "penalty": "Patient harm",
                "risk_level": "high"
            },
            "triage": {
                "name": "Triage Standards",
                "description": "Check for triage standards",
                "keywords": ["triage", "acuity", "priority", "emergency severity index", "esi"],
                "severity": "high",
                "regulation": "Emergency Medicine Standards",
                "penalty": "Patient harm",
                "risk_level": "high"
            },
            "emergency_consent": {
                "name": "Emergency Consent",
                "description": "Check for emergency consent procedures",
                "keywords": ["emergency consent", "implied consent", "emergency treatment", "consent"],
                "severity": "high",
                "regulation": "State Laws",
                "penalty": "Legal liability",
                "risk_level": "high"
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
    
    async def analyze_hipaa_compliance(self, text: str, context: Optional[Dict] = None) -> HealthcareAnalysis:
        """Analyze HIPAA compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each HIPAA rule
            for rule_id, rule in self.hipaa_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = HealthcareViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        regulation_reference=rule.get("regulation"),
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
                    "Conduct comprehensive HIPAA compliance audit",
                    "Implement privacy and security safeguards",
                    "Train staff on HIPAA requirements",
                    "Establish breach notification procedures",
                    "Review and update business associate agreements"
                ]
            else:
                recommendations = [
                    "Maintain current HIPAA compliance practices",
                    "Regularly review privacy and security policies",
                    "Conduct periodic HIPAA training"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("healthcare", "hipaa_analysis", duration)
            metrics_service.record_reasoning_confidence("healthcare", "hipaa_analysis", confidence)
            
            return HealthcareAnalysis(
                domain=HealthcareDomain.HIPAA,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.hipaa_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("healthcare", "hipaa_analysis", str(e))
            raise
    
    async def analyze_fda_compliance(self, text: str, context: Optional[Dict] = None) -> HealthcareAnalysis:
        """Analyze FDA compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each FDA rule
            for rule_id, rule in self.fda_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = HealthcareViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        regulation_reference=rule.get("regulation"),
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
                    "Conduct comprehensive FDA compliance audit",
                    "Implement proper approval processes",
                    "Establish quality control systems",
                    "Train staff on FDA requirements",
                    "Review and update labeling requirements"
                ]
            else:
                recommendations = [
                    "Maintain current FDA compliance practices",
                    "Regularly review FDA regulations",
                    "Conduct periodic FDA training"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("healthcare", "fda_analysis", duration)
            metrics_service.record_reasoning_confidence("healthcare", "fda_analysis", confidence)
            
            return HealthcareAnalysis(
                domain=HealthcareDomain.FDA,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.fda_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("healthcare", "fda_analysis", str(e))
            raise
    
    async def analyze_clinical_trial_compliance(self, text: str, context: Optional[Dict] = None) -> HealthcareAnalysis:
        """Analyze clinical trial compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each clinical trial rule
            for rule_id, rule in self.clinical_trial_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = HealthcareViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        regulation_reference=rule.get("regulation"),
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
                    "Conduct comprehensive clinical trial compliance audit",
                    "Implement proper informed consent procedures",
                    "Establish IRB oversight",
                    "Train staff on clinical trial requirements",
                    "Review and update protocols"
                ]
            else:
                recommendations = [
                    "Maintain current clinical trial compliance practices",
                    "Regularly review clinical trial regulations",
                    "Conduct periodic clinical trial training"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("healthcare", "clinical_trial_analysis", duration)
            metrics_service.record_reasoning_confidence("healthcare", "clinical_trial_analysis", confidence)
            
            return HealthcareAnalysis(
                domain=HealthcareDomain.CLINICAL_TRIALS,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.clinical_trial_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("healthcare", "clinical_trial_analysis", str(e))
            raise
    
    async def analyze_comprehensive_healthcare(self, text: str, context: Optional[Dict] = None) -> Dict[str, HealthcareAnalysis]:
        """Analyze comprehensive healthcare compliance across all domains."""
        results = {}
        
        # Analyze each domain
        results["hipaa"] = await self.analyze_hipaa_compliance(text, context)
        results["fda"] = await self.analyze_fda_compliance(text, context)
        results["clinical_trials"] = await self.analyze_clinical_trial_compliance(text, context)
        
        return results


# Global instance
healthcare_pilot = HealthcareCompliancePilot()
