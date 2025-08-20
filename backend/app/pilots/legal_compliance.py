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
        
    def _load_gdpr_rules(self) -> Dict[str, Dict]:
        """Load GDPR compliance rules."""
        return {
            "gdpr_consent": {
                "name": "Consent Requirements",
                "description": "Check for proper consent mechanisms",
                "keywords": ["consent", "explicit consent", "opt-in", "opt-out", "withdraw"],
                "severity": "high",
                "article": "Art. 7",
                "penalty": "Up to €20 million or 4% of global annual turnover"
            },
            "gdpr_data_minimization": {
                "name": "Data Minimization",
                "description": "Check if only necessary data is collected",
                "keywords": ["necessary", "minimal", "purpose", "limited"],
                "severity": "medium",
                "article": "Art. 5(1)(c)",
                "penalty": "Up to €10 million or 2% of global annual turnover"
            },
            "gdpr_right_to_access": {
                "name": "Right to Access",
                "description": "Check for data subject access rights",
                "keywords": ["access", "request", "copy", "portability"],
                "severity": "high",
                "article": "Art. 15",
                "penalty": "Up to €20 million or 4% of global annual turnover"
            },
            "gdpr_right_to_erasure": {
                "name": "Right to Erasure",
                "description": "Check for right to be forgotten",
                "keywords": ["erasure", "delete", "forgotten", "remove"],
                "severity": "high",
                "article": "Art. 17",
                "penalty": "Up to €20 million or 4% of global annual turnover"
            },
            "gdpr_data_breach": {
                "name": "Data Breach Notification",
                "description": "Check for data breach notification procedures",
                "keywords": ["breach", "notification", "72 hours", "incident"],
                "severity": "critical",
                "article": "Art. 33-34",
                "penalty": "Up to €20 million or 4% of global annual turnover"
            }
        }
    
    def _load_hipaa_rules(self) -> Dict[str, Dict]:
        """Load HIPAA compliance rules."""
        return {
            "hipaa_privacy_rule": {
                "name": "Privacy Rule Compliance",
                "description": "Check for proper privacy safeguards",
                "keywords": ["privacy", "confidential", "protected health information", "phi"],
                "severity": "high",
                "section": "164.312(a)(1)",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_security_rule": {
                "name": "Security Rule Compliance",
                "description": "Check for technical and physical safeguards",
                "keywords": ["security", "encryption", "access control", "audit"],
                "severity": "high",
                "section": "164.312(c)(1)",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_breach_notification": {
                "name": "Breach Notification Rule",
                "description": "Check for breach notification procedures",
                "keywords": ["breach", "notification", "60 days", "report"],
                "severity": "critical",
                "section": "164.400-414",
                "penalty": "Up to $50,000 per violation"
            },
            "hipaa_business_associate": {
                "name": "Business Associate Agreements",
                "description": "Check for proper BAAs",
                "keywords": ["business associate", "baa", "agreement", "contract"],
                "severity": "medium",
                "section": "164.308(b)(1)",
                "penalty": "Up to $50,000 per violation"
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


# Global instance
legal_pilot = LegalCompliancePilot()
