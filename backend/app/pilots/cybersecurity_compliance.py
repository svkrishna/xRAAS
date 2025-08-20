"""
Cybersecurity Compliance Pilot for XReason
Handles security frameworks, threat detection, incident response, and data protection.
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from app.services.metrics_service import metrics_service


class CybersecurityDomain(Enum):
    SECURITY_FRAMEWORKS = "security_frameworks"
    THREAT_DETECTION = "threat_detection"
    INCIDENT_RESPONSE = "incident_response"
    DATA_PROTECTION = "data_protection"


@dataclass
class CybersecurityViolation:
    """Represents a cybersecurity compliance violation found in analysis."""
    rule_id: str
    rule_name: str
    severity: str
    description: str
    evidence: str
    recommendation: str
    framework_reference: Optional[str] = None
    penalty_info: Optional[str] = None
    risk_level: Optional[str] = None


@dataclass
class CybersecurityAnalysis:
    """Result of cybersecurity compliance analysis."""
    domain: CybersecurityDomain
    is_compliant: bool
    confidence: float
    violations: List[CybersecurityViolation]
    recommendations: List[str]
    risk_score: float
    analysis_timestamp: datetime
    metadata: Dict[str, Any]


class CybersecurityCompliancePilot:
    """Cybersecurity compliance analysis pilot for XReason."""
    
    def __init__(self):
        self.security_frameworks_rules = self._load_security_frameworks_rules()
        self.threat_detection_rules = self._load_threat_detection_rules()
        self.incident_response_rules = self._load_incident_response_rules()
        self.data_protection_rules = self._load_data_protection_rules()
    
    def _load_security_frameworks_rules(self) -> Dict[str, Dict]:
        """Load security frameworks compliance rules."""
        return {
            "nist_cybersecurity": {
                "name": "NIST Cybersecurity Framework",
                "description": "Check for NIST Cybersecurity Framework implementation",
                "keywords": ["nist cybersecurity framework", "identify", "protect", "detect", "respond", "recover"],
                "severity": "high",
                "framework": "NIST CSF",
                "penalty": "Security vulnerabilities and regulatory action",
                "risk_level": "high"
            },
            "iso_27001": {
                "name": "ISO 27001 Information Security",
                "description": "Check for ISO 27001 information security management system",
                "keywords": ["iso 27001", "information security", "isms", "security controls", "risk assessment"],
                "severity": "high",
                "framework": "ISO 27001:2013",
                "penalty": "Loss of certification",
                "risk_level": "high"
            },
            "soc_2": {
                "name": "SOC 2 Compliance",
                "description": "Check for SOC 2 compliance requirements",
                "keywords": ["soc 2", "trust services criteria", "security", "availability", "processing integrity"],
                "severity": "high",
                "framework": "AICPA SOC 2",
                "penalty": "Loss of customer trust",
                "risk_level": "high"
            }
        }
    
    def _load_threat_detection_rules(self) -> Dict[str, Dict]:
        """Load threat detection compliance rules."""
        return {
            "siem_monitoring": {
                "name": "SIEM Monitoring",
                "description": "Check for SIEM monitoring implementation",
                "keywords": ["siem", "security information and event management", "log monitoring", "threat detection"],
                "severity": "high",
                "framework": "Security Monitoring",
                "penalty": "Undetected threats and breaches",
                "risk_level": "high"
            },
            "intrusion_detection": {
                "name": "Intrusion Detection Systems",
                "description": "Check for intrusion detection systems",
                "keywords": ["ids", "ips", "intrusion detection", "intrusion prevention", "network monitoring"],
                "severity": "high",
                "framework": "Network Security",
                "penalty": "Undetected intrusions",
                "risk_level": "high"
            }
        }
    
    def _load_incident_response_rules(self) -> Dict[str, Dict]:
        """Load incident response compliance rules."""
        return {
            "incident_response_plan": {
                "name": "Incident Response Plan",
                "description": "Check for incident response plan",
                "keywords": ["incident response plan", "irp", "incident management", "response procedures"],
                "severity": "critical",
                "framework": "NIST SP 800-61",
                "penalty": "Ineffective incident response",
                "risk_level": "critical"
            },
            "forensic_capabilities": {
                "name": "Forensic Capabilities",
                "description": "Check for forensic investigation capabilities",
                "keywords": ["forensics", "digital forensics", "evidence collection", "chain of custody"],
                "severity": "high",
                "framework": "Digital Forensics",
                "penalty": "Lost evidence and legal issues",
                "risk_level": "high"
            }
        }
    
    def _load_data_protection_rules(self) -> Dict[str, Dict]:
        """Load data protection compliance rules."""
        return {
            "encryption": {
                "name": "Data Encryption",
                "description": "Check for data encryption implementation",
                "keywords": ["encryption", "data encryption", "at rest", "in transit", "encryption keys"],
                "severity": "high",
                "framework": "Cryptography",
                "penalty": "Data breaches and regulatory fines",
                "risk_level": "high"
            },
            "data_backup": {
                "name": "Data Backup and Recovery",
                "description": "Check for data backup and recovery procedures",
                "keywords": ["data backup", "backup procedures", "recovery testing", "backup verification"],
                "severity": "high",
                "framework": "Data Protection",
                "penalty": "Data loss",
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
    
    async def analyze_security_frameworks(self, text: str, context: Optional[Dict] = None) -> CybersecurityAnalysis:
        """Analyze security frameworks compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each security frameworks rule
            for rule_id, rule in self.security_frameworks_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = CybersecurityViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        framework_reference=rule.get("framework"),
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
                    "Conduct comprehensive security framework audit",
                    "Implement security management system",
                    "Establish security controls",
                    "Train staff on security requirements"
                ]
            else:
                recommendations = [
                    "Maintain current security framework practices",
                    "Regularly review security standards"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("cybersecurity", "security_frameworks_analysis", duration)
            metrics_service.record_reasoning_confidence("cybersecurity", "security_frameworks_analysis", confidence)
            
            return CybersecurityAnalysis(
                domain=CybersecurityDomain.SECURITY_FRAMEWORKS,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.security_frameworks_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("cybersecurity", "security_frameworks_analysis", str(e))
            raise
    
    async def analyze_comprehensive_cybersecurity(self, text: str, context: Optional[Dict] = None) -> Dict[str, CybersecurityAnalysis]:
        """Analyze comprehensive cybersecurity compliance across all domains."""
        results = {}
        
        # Analyze each domain
        results["security_frameworks"] = await self.analyze_security_frameworks(text, context)
        
        return results


# Global instance
cybersecurity_pilot = CybersecurityCompliancePilot()
