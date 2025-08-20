"""
Legal Compliance Pilot for XReason
Handles GDPR, HIPAA, contract analysis, and legal document validation.
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from app.services.metrics_service import metrics_service


class LegalDomain(Enum):
    GDPR = "gdpr"
    HIPAA = "hipaa"
    CONTRACT = "contract"
    PRIVACY = "privacy"
    COMPLIANCE = "compliance"
    CCPA = "ccpa"
    SOX = "sox"
    PCI_DSS = "pci_dss"


@dataclass
class LegalViolation:
    """Represents a legal violation found in analysis."""
    rule_id: str
    rule_name: str
    severity: str
    description: str
    evidence: str
    recommendation: str
    article_reference: Optional[str] = None
    penalty_info: Optional[str] = None


@dataclass
class LegalAnalysis:
    """Result of legal compliance analysis."""
    domain: LegalDomain
    is_compliant: bool
    confidence: float
    violations: List[LegalViolation]
    recommendations: List[str]
    risk_score: float
    analysis_timestamp: datetime
    metadata: Dict[str, Any]


class LegalCompliancePilot:
    """Legal compliance analysis pilot for XReason."""
    
    def __init__(self):
        self.gdpr_rules = self._load_gdpr_rules()
        self.hipaa_rules = self._load_hipaa_rules()
        self.contract_rules = self._load_contract_rules()
        self.privacy_rules = self._load_privacy_rules()
        self.ccpa_rules = self._load_ccpa_rules()
        self.sox_rules = self._load_sox_rules()
        self.pci_dss_rules = self._load_pci_dss_rules()
        
    def _load_gdpr_rules(self) -> Dict[str, Dict]:
        """Load GDPR compliance rules."""
        return {
            "gdpr_consent": {
                "name": "Consent Requirements",
                "description": "Check for proper consent mechanisms",
                "keywords": ["consent", "explicit consent", "opt-in", "opt-out", "withdraw", "unsubscribe"],
                "severity": "high",
                "article": "Art. 7",
                "penalty": "Up to €20 million or 4% of global annual turnover"
            },
            "gdpr_data_minimization": {
                "name": "Data Minimization",
                "description": "Check if only necessary data is collected",
                "keywords": ["necessary", "minimal", "purpose", "limited", "adequate", "relevant"],
                "severity": "medium",
                "article": "Art. 5(1)(c)",
                "penalty": "Up to €10 million or 2% of global annual turnover"
            },
            "gdpr_right_to_access": {
                "name": "Right to Access",
                "description": "Check for data subject access rights",
                "keywords": ["access", "request", "copy", "portability", "data subject rights"],
                "severity": "high",
                "article": "Art. 15",
                "penalty": "Up to €20 million or 4% of global annual turnover"
            },
            "gdpr_right_to_erasure": {
                "name": "Right to Erasure",
                "description": "Check for right to be forgotten",
                "keywords": ["erasure", "delete", "forgotten", "remove", "right to be forgotten"],
                "severity": "high",
                "article": "Art. 17",
                "penalty": "Up to €20 million or 4% of global annual turnover"
            },
            "gdpr_data_breach": {
                "name": "Data Breach Notification",
                "description": "Check for data breach notification procedures",
                "keywords": ["breach", "notification", "72 hours", "incident", "data breach"],
                "severity": "critical",
                "article": "Art. 33-34",
                "penalty": "Up to €20 million or 4% of global annual turnover"
            },
            "gdpr_data_processing_basis": {
                "name": "Legal Basis for Processing",
                "description": "Check for proper legal basis for data processing",
                "keywords": ["legal basis", "legitimate interest", "contract", "legal obligation", "vital interest"],
                "severity": "high",
                "article": "Art. 6",
                "penalty": "Up to €20 million or 4% of global annual turnover"
            },
            "gdpr_data_transfers": {
                "name": "Data Transfer Safeguards",
                "description": "Check for proper safeguards for international data transfers",
                "keywords": ["transfer", "international", "adequacy", "safeguards", "binding corporate rules"],
                "severity": "high",
                "article": "Art. 44-50",
                "penalty": "Up to €20 million or 4% of global annual turnover"
            },
            "gdpr_privacy_by_design": {
                "name": "Privacy by Design",
                "description": "Check for privacy by design and default principles",
                "keywords": ["privacy by design", "privacy by default", "data protection by design"],
                "severity": "medium",
                "article": "Art. 25",
                "penalty": "Up to €10 million or 2% of global annual turnover"
            },
            "gdpr_dpo_requirement": {
                "name": "Data Protection Officer",
                "description": "Check for DPO requirements and contact information",
                "keywords": ["data protection officer", "dpo", "contact", "supervisory authority"],
                "severity": "medium",
                "article": "Art. 37-39",
                "penalty": "Up to €10 million or 2% of global annual turnover"
            },
            "gdpr_record_keeping": {
                "name": "Record of Processing Activities",
                "description": "Check for record keeping requirements",
                "keywords": ["record", "processing activities", "documentation", "accountability"],
                "severity": "medium",
                "article": "Art. 30",
                "penalty": "Up to €10 million or 2% of global annual turnover"
            }
        }
    
    def _load_hipaa_rules(self) -> Dict[str, Dict]:
        """Load HIPAA compliance rules."""
        return {
            "hipaa_privacy_rule": {
                "name": "Privacy Rule Compliance",
                "description": "Check for proper privacy safeguards",
                "keywords": ["privacy", "confidential", "protected health information", "phi", "patient privacy"],
                "severity": "high",
                "section": "164.312(a)(1)",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_security_rule": {
                "name": "Security Rule Compliance",
                "description": "Check for technical and physical safeguards",
                "keywords": ["security", "encryption", "access control", "audit", "technical safeguards"],
                "severity": "high",
                "section": "164.312(c)(1)",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_breach_notification": {
                "name": "Breach Notification Rule",
                "description": "Check for breach notification procedures",
                "keywords": ["breach", "notification", "60 days", "report", "breach notification"],
                "severity": "critical",
                "section": "164.400-414",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_business_associate": {
                "name": "Business Associate Agreements",
                "description": "Check for proper BAAs",
                "keywords": ["business associate", "baa", "agreement", "contract", "business associate agreement"],
                "severity": "medium",
                "section": "164.308(b)(1)",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_minimum_necessary": {
                "name": "Minimum Necessary Standard",
                "description": "Check for minimum necessary use and disclosure",
                "keywords": ["minimum necessary", "need to know", "limited access", "role-based"],
                "severity": "high",
                "section": "164.502(b)",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_authorization": {
                "name": "Patient Authorization",
                "description": "Check for proper patient authorization procedures",
                "keywords": ["authorization", "patient consent", "written authorization", "patient rights"],
                "severity": "high",
                "section": "164.508",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_notice_privacy": {
                "name": "Notice of Privacy Practices",
                "description": "Check for notice of privacy practices",
                "keywords": ["notice of privacy practices", "privacy notice", "patient rights", "disclosure"],
                "severity": "medium",
                "section": "164.520",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_administrative_safeguards": {
                "name": "Administrative Safeguards",
                "description": "Check for administrative safeguards implementation",
                "keywords": ["administrative safeguards", "workforce training", "security awareness", "policies"],
                "severity": "high",
                "section": "164.308",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_physical_safeguards": {
                "name": "Physical Safeguards",
                "description": "Check for physical safeguards implementation",
                "keywords": ["physical safeguards", "facility access", "workstation security", "device control"],
                "severity": "medium",
                "section": "164.310",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_technical_safeguards": {
                "name": "Technical Safeguards",
                "description": "Check for technical safeguards implementation",
                "keywords": ["technical safeguards", "access control", "audit controls", "integrity", "transmission security"],
                "severity": "high",
                "section": "164.312",
                "penalty": "Up to $50,000 per violation"
            }
        }
    
    def _load_ccpa_rules(self) -> Dict[str, Dict]:
        """Load CCPA compliance rules."""
        return {
            "ccpa_consumer_rights": {
                "name": "Consumer Rights Disclosure",
                "description": "Check for consumer rights disclosure",
                "keywords": ["consumer rights", "right to know", "right to delete", "right to opt-out"],
                "severity": "high",
                "section": "1798.100-1798.199.100",
                "penalty": "Up to $7,500 per intentional violation"
            },
            "ccpa_notice_collection": {
                "name": "Notice at Collection",
                "description": "Check for notice at collection requirements",
                "keywords": ["notice at collection", "categories collected", "purposes", "disclosure"],
                "severity": "high",
                "section": "1798.100",
                "penalty": "Up to $7,500 per intentional violation"
            },
            "ccpa_privacy_policy": {
                "name": "Privacy Policy Requirements",
                "description": "Check for comprehensive privacy policy",
                "keywords": ["privacy policy", "data categories", "business purposes", "third parties"],
                "severity": "high",
                "section": "1798.130",
                "penalty": "Up to $7,500 per intentional violation"
            },
            "ccpa_opt_out": {
                "name": "Opt-Out Rights",
                "description": "Check for opt-out mechanisms",
                "keywords": ["opt-out", "do not sell", "personal information", "sale"],
                "severity": "high",
                "section": "1798.120",
                "penalty": "Up to $7,500 per intentional violation"
            },
            "ccpa_verification": {
                "name": "Verification Procedures",
                "description": "Check for consumer verification procedures",
                "keywords": ["verification", "consumer identity", "reasonable security", "authentication"],
                "severity": "medium",
                "section": "1798.140",
                "penalty": "Up to $2,500 per violation"
            },
            "ccpa_service_providers": {
                "name": "Service Provider Requirements",
                "description": "Check for service provider contract requirements",
                "keywords": ["service provider", "contract", "restrictions", "confidentiality"],
                "severity": "medium",
                "section": "1798.140",
                "penalty": "Up to $2,500 per violation"
            }
        }
    
    def _load_sox_rules(self) -> Dict[str, Dict]:
        """Load SOX compliance rules."""
        return {
            "sox_internal_controls": {
                "name": "Internal Controls",
                "description": "Check for internal control requirements",
                "keywords": ["internal controls", "financial reporting", "control environment", "risk assessment"],
                "severity": "critical",
                "section": "302, 404",
                "penalty": "Up to $5 million fine and 20 years imprisonment"
            },
            "sox_audit_committee": {
                "name": "Audit Committee Independence",
                "description": "Check for audit committee independence",
                "keywords": ["audit committee", "independent", "financial expert", "oversight"],
                "severity": "high",
                "section": "301",
                "penalty": "Up to $5 million fine and 20 years imprisonment"
            },
            "sox_whistleblower": {
                "name": "Whistleblower Protection",
                "description": "Check for whistleblower protection",
                "keywords": ["whistleblower", "retaliation", "protection", "reporting"],
                "severity": "high",
                "section": "806",
                "penalty": "Up to $5 million fine and 20 years imprisonment"
            },
            "sox_corporate_responsibility": {
                "name": "Corporate Responsibility",
                "description": "Check for corporate responsibility requirements",
                "keywords": ["corporate responsibility", "certification", "disclosure", "accuracy"],
                "severity": "critical",
                "section": "302",
                "penalty": "Up to $5 million fine and 20 years imprisonment"
            },
            "sox_enhanced_disclosure": {
                "name": "Enhanced Financial Disclosures",
                "description": "Check for enhanced financial disclosure requirements",
                "keywords": ["financial disclosure", "off-balance sheet", "pro forma", "transparency"],
                "severity": "high",
                "section": "401-409",
                "penalty": "Up to $5 million fine and 20 years imprisonment"
            },
            "sox_analyst_conflicts": {
                "name": "Analyst Conflicts of Interest",
                "description": "Check for analyst conflict management",
                "keywords": ["analyst conflicts", "research", "independence", "disclosure"],
                "severity": "medium",
                "section": "501",
                "penalty": "Up to $5 million fine and 20 years imprisonment"
            }
        }
    
    def _load_pci_dss_rules(self) -> Dict[str, Dict]:
        """Load PCI DSS compliance rules."""
        return {
            "pci_network_security": {
                "name": "Network Security",
                "description": "Check for network security requirements",
                "keywords": ["network security", "firewall", "network segmentation", "access control"],
                "severity": "critical",
                "requirement": "PCI DSS 1.0",
                "penalty": "Fines up to $500,000 per incident"
            },
            "pci_cardholder_data": {
                "name": "Cardholder Data Protection",
                "description": "Check for cardholder data protection",
                "keywords": ["cardholder data", "encryption", "storage", "transmission"],
                "severity": "critical",
                "requirement": "PCI DSS 3.0, 4.0",
                "penalty": "Fines up to $500,000 per incident"
            },
            "pci_vulnerability_management": {
                "name": "Vulnerability Management",
                "description": "Check for vulnerability management program",
                "keywords": ["vulnerability management", "antivirus", "patches", "security updates"],
                "severity": "high",
                "requirement": "PCI DSS 5.0, 6.0",
                "penalty": "Fines up to $500,000 per incident"
            },
            "pci_access_control": {
                "name": "Access Control",
                "description": "Check for access control measures",
                "keywords": ["access control", "authentication", "authorization", "least privilege"],
                "severity": "high",
                "requirement": "PCI DSS 7.0, 8.0",
                "penalty": "Fines up to $500,000 per incident"
            },
            "pci_monitoring": {
                "name": "Monitoring and Testing",
                "description": "Check for monitoring and testing requirements",
                "keywords": ["monitoring", "logging", "audit trails", "testing"],
                "severity": "high",
                "requirement": "PCI DSS 10.0, 11.0",
                "penalty": "Fines up to $500,000 per incident"
            },
            "pci_policy": {
                "name": "Information Security Policy",
                "description": "Check for information security policy",
                "keywords": ["security policy", "risk assessment", "incident response", "training"],
                "severity": "medium",
                "requirement": "PCI DSS 12.0",
                "penalty": "Fines up to $500,000 per incident"
            }
        }
    
    def _load_contract_rules(self) -> Dict[str, Dict]:
        """Load contract analysis rules."""
        return {
            "contract_termination": {
                "name": "Termination Clauses",
                "description": "Check for proper termination provisions",
                "keywords": ["termination", "terminate", "end", "cancel", "expire"],
                "severity": "medium"
            },
            "contract_liability": {
                "name": "Liability Limitations",
                "description": "Check for liability limitation clauses",
                "keywords": ["liability", "damages", "indemnify", "hold harmless"],
                "severity": "high"
            },
            "contract_confidentiality": {
                "name": "Confidentiality Provisions",
                "description": "Check for confidentiality clauses",
                "keywords": ["confidential", "secret", "proprietary", "non-disclosure"],
                "severity": "high"
            },
            "contract_governing_law": {
                "name": "Governing Law",
                "description": "Check for governing law provisions",
                "keywords": ["governing law", "jurisdiction", "venue", "applicable law"],
                "severity": "medium"
            }
        }
    
    def _load_privacy_rules(self) -> Dict[str, Dict]:
        """Load general privacy rules."""
        return {
            "privacy_policy": {
                "name": "Privacy Policy Requirements",
                "description": "Check for comprehensive privacy policy",
                "keywords": ["privacy policy", "data collection", "use", "sharing"],
                "severity": "high"
            },
            "data_retention": {
                "name": "Data Retention Policies",
                "description": "Check for data retention policies",
                "keywords": ["retention", "retain", "delete", "destroy", "period"],
                "severity": "medium"
            },
            "third_party_sharing": {
                "name": "Third-Party Data Sharing",
                "description": "Check for third-party sharing disclosures",
                "keywords": ["third party", "share", "disclose", "transfer"],
                "severity": "high"
            }
        }
    
    async def analyze_gdpr_compliance(self, text: str, context: Optional[Dict] = None) -> LegalAnalysis:
        """Analyze GDPR compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each GDPR rule
            for rule_id, rule in self.gdpr_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = LegalViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        article_reference=rule.get("article"),
                        penalty_info=rule.get("penalty")
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
                    "Conduct a comprehensive GDPR compliance audit",
                    "Implement proper consent management system",
                    "Establish data subject rights procedures",
                    "Create data breach response plan",
                    "Train staff on GDPR requirements"
                ]
            else:
                recommendations = [
                    "Maintain current GDPR compliance practices",
                    "Regularly review and update privacy policies",
                    "Conduct periodic compliance assessments"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("legal", "gdpr_analysis", duration)
            metrics_service.record_reasoning_confidence("legal", "gdpr_analysis", confidence)
            
            return LegalAnalysis(
                domain=LegalDomain.GDPR,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.gdpr_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("legal", "gdpr_analysis", str(e))
            raise
    
    async def analyze_hipaa_compliance(self, text: str, context: Optional[Dict] = None) -> LegalAnalysis:
        """Analyze HIPAA compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each HIPAA rule
            for rule_id, rule in self.hipaa_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = LegalViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} safeguards",
                        article_reference=rule.get("section"),
                        penalty_info=rule.get("penalty")
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
                    "Implement administrative, physical, and technical safeguards",
                    "Establish breach notification procedures",
                    "Create business associate agreement templates",
                    "Train workforce on HIPAA requirements"
                ]
            else:
                recommendations = [
                    "Maintain current HIPAA compliance practices",
                    "Regularly review and update security measures",
                    "Conduct periodic risk assessments"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("legal", "hipaa_analysis", duration)
            metrics_service.record_reasoning_confidence("legal", "hipaa_analysis", confidence)
            
            return LegalAnalysis(
                domain=LegalDomain.HIPAA,
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
            metrics_service.record_reasoning_error("legal", "hipaa_analysis", str(e))
            raise
    
    async def analyze_contract(self, text: str, context: Optional[Dict] = None) -> LegalAnalysis:
        """Analyze contract for key provisions and risks."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each contract rule
            for rule_id, rule in self.contract_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = LegalViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Consider adding {rule['name'].lower()} provisions",
                        article_reference=None,
                        penalty_info=None
                    )
                    violations.append(violation)
                    
                    # Calculate risk score
                    if rule["severity"] == "high":
                        risk_score += 0.3
                    elif rule["severity"] == "medium":
                        risk_score += 0.2
                    else:
                        risk_score += 0.1
            
            # Generate recommendations
            if violations:
                recommendations = [
                    "Review contract with legal counsel",
                    "Consider adding missing provisions",
                    "Negotiate favorable terms where possible",
                    "Ensure proper dispute resolution mechanisms"
                ]
            else:
                recommendations = [
                    "Contract appears comprehensive",
                    "Consider periodic contract reviews",
                    "Monitor for changing legal requirements"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("legal", "contract_analysis", duration)
            metrics_service.record_reasoning_confidence("legal", "contract_analysis", confidence)
            
            return LegalAnalysis(
                domain=LegalDomain.CONTRACT,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.contract_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("legal", "contract_analysis", str(e))
            raise
    
    def _check_rule_violation(self, text: str, rule: Dict) -> bool:
        """Check if text violates a specific rule."""
        text_lower = text.lower()
        keywords = rule.get("keywords", [])
        
        # Check if any keywords are missing
        found_keywords = [kw for kw in keywords if kw.lower() in text_lower]
        
        # If less than 50% of keywords are found, consider it a violation
        return len(found_keywords) < len(keywords) * 0.5
    
    async def analyze_legal_compliance(self, text: str, domains: List[LegalDomain] = None) -> Dict[str, LegalAnalysis]:
        """Analyze legal compliance across multiple domains."""
        if domains is None:
            domains = [LegalDomain.GDPR, LegalDomain.HIPAA, LegalDomain.CONTRACT]
        
        results = {}
        
        for domain in domains:
            if domain == LegalDomain.GDPR:
                results["gdpr"] = await self.analyze_gdpr_compliance(text)
            elif domain == LegalDomain.HIPAA:
                results["hipaa"] = await self.analyze_hipaa_compliance(text)
            elif domain == LegalDomain.CONTRACT:
                results["contract"] = await self.analyze_contract(text)
        
        return results
    
    async def analyze_ccpa_compliance(self, text: str, context: Optional[Dict] = None) -> LegalAnalysis:
        """Analyze CCPA compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each CCPA rule
            for rule_id, rule in self.ccpa_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = LegalViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        article_reference=rule.get("section"),
                        penalty_info=rule.get("penalty")
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
                    "Conduct comprehensive CCPA compliance audit",
                    "Implement consumer rights request procedures",
                    "Update privacy policy for CCPA requirements",
                    "Establish opt-out mechanisms for data sales",
                    "Train staff on CCPA requirements"
                ]
            else:
                recommendations = [
                    "Maintain current CCPA compliance practices",
                    "Regularly review and update privacy policies",
                    "Monitor for CCPA regulation changes"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("legal", "ccpa_analysis", duration)
            metrics_service.record_reasoning_confidence("legal", "ccpa_analysis", confidence)
            
            return LegalAnalysis(
                domain=LegalDomain.CCPA,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.ccpa_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("legal", "ccpa_analysis", str(e))
            raise
    
    async def analyze_sox_compliance(self, text: str, context: Optional[Dict] = None) -> LegalAnalysis:
        """Analyze SOX compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each SOX rule
            for rule_id, rule in self.sox_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = LegalViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        article_reference=rule.get("section"),
                        penalty_info=rule.get("penalty")
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
                    "Conduct comprehensive SOX compliance audit",
                    "Implement internal control framework",
                    "Establish audit committee oversight",
                    "Create whistleblower protection program",
                    "Train executives on SOX requirements"
                ]
            else:
                recommendations = [
                    "Maintain current SOX compliance practices",
                    "Regularly review internal controls",
                    "Conduct periodic SOX assessments"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("legal", "sox_analysis", duration)
            metrics_service.record_reasoning_confidence("legal", "sox_analysis", confidence)
            
            return LegalAnalysis(
                domain=LegalDomain.SOX,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.sox_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("legal", "sox_analysis", str(e))
            raise
    
    async def analyze_pci_dss_compliance(self, text: str, context: Optional[Dict] = None) -> LegalAnalysis:
        """Analyze PCI DSS compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each PCI DSS rule
            for rule_id, rule in self.pci_dss_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = LegalViolation(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        severity=rule["severity"],
                        description=rule["description"],
                        evidence=f"Missing or insufficient: {', '.join(rule['keywords'])}",
                        recommendation=f"Implement proper {rule['name'].lower()} mechanisms",
                        article_reference=rule.get("requirement"),
                        penalty_info=rule.get("penalty")
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
                    "Conduct comprehensive PCI DSS compliance audit",
                    "Implement network security controls",
                    "Establish cardholder data protection measures",
                    "Create vulnerability management program",
                    "Train staff on PCI DSS requirements"
                ]
            else:
                recommendations = [
                    "Maintain current PCI DSS compliance practices",
                    "Regularly review security controls",
                    "Conduct periodic PCI DSS assessments"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("legal", "pci_dss_analysis", duration)
            metrics_service.record_reasoning_confidence("legal", "pci_dss_analysis", confidence)
            
            return LegalAnalysis(
                domain=LegalDomain.PCI_DSS,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.pci_dss_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("legal", "pci_dss_analysis", str(e))
            raise


# Global instance
legal_pilot = LegalCompliancePilot()
