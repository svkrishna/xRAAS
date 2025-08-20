"""
Finance Compliance Pilot for XReason
Handles banking regulations, investment compliance, AML, Basel, and financial reporting standards.
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from app.services.metrics_service import metrics_service


class FinanceDomain(Enum):
    BANKING = "banking"
    INVESTMENT = "investment"
    AML_KYC = "aml_kyc"
    BASEL = "basel"
    FINANCIAL_REPORTING = "financial_reporting"
    INSURANCE = "insurance"
    CRYPTO = "crypto"
    FINTECH = "fintech"


@dataclass
class FinanceViolation:
    """Represents a finance compliance violation found in analysis."""
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
class FinanceAnalysis:
    """Result of finance compliance analysis."""
    domain: FinanceDomain
    is_compliant: bool
    confidence: float
    violations: List[FinanceViolation]
    recommendations: List[str]
    risk_score: float
    analysis_timestamp: datetime
    metadata: Dict[str, Any]


class FinanceCompliancePilot:
    """Finance compliance analysis pilot for XReason."""
    
    def __init__(self):
        self.banking_rules = self._load_banking_rules()
        self.investment_rules = self._load_investment_rules()
        self.aml_kyc_rules = self._load_aml_kyc_rules()
        self.basel_rules = self._load_basel_rules()
        self.financial_reporting_rules = self._load_financial_reporting_rules()
        self.insurance_rules = self._load_insurance_rules()
        self.crypto_rules = self._load_crypto_rules()
        self.fintech_rules = self._load_fintech_rules()
    
    def _load_banking_rules(self) -> Dict[str, Dict]:
        """Load banking compliance rules."""
        return {
            "capital_adequacy": {
                "name": "Capital Adequacy Requirements",
                "description": "Check for capital adequacy requirements",
                "keywords": ["capital adequacy", "capital ratio", "tier 1", "tier 2", "risk-weighted assets"],
                "severity": "critical",
                "regulation": "Basel III",
                "penalty": "Regulatory action and fines",
                "risk_level": "critical"
            },
            "liquidity_requirements": {
                "name": "Liquidity Requirements",
                "description": "Check for liquidity requirements",
                "keywords": ["liquidity", "lcr", "nsfr", "liquidity coverage ratio", "net stable funding ratio"],
                "severity": "high",
                "regulation": "Basel III",
                "penalty": "Regulatory restrictions",
                "risk_level": "high"
            },
            "lending_standards": {
                "name": "Lending Standards",
                "description": "Check for proper lending standards",
                "keywords": ["lending standards", "credit assessment", "underwriting", "loan origination"],
                "severity": "high",
                "regulation": "Various banking regulations",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "interest_rate_risk": {
                "name": "Interest Rate Risk Management",
                "description": "Check for interest rate risk management",
                "keywords": ["interest rate risk", "irr", "duration", "gap analysis", "hedging"],
                "severity": "medium",
                "regulation": "Banking regulations",
                "penalty": "Financial losses",
                "risk_level": "medium"
            },
            "operational_risk": {
                "name": "Operational Risk Management",
                "description": "Check for operational risk management",
                "keywords": ["operational risk", "internal controls", "fraud prevention", "cybersecurity"],
                "severity": "high",
                "regulation": "Various banking regulations",
                "penalty": "Financial and reputational losses",
                "risk_level": "high"
            }
        }
    
    def _load_investment_rules(self) -> Dict[str, Dict]:
        """Load investment compliance rules."""
        return {
            "fiduciary_duty": {
                "name": "Fiduciary Duty",
                "description": "Check for fiduciary duty compliance",
                "keywords": ["fiduciary duty", "best interest", "client interest", "conflict of interest"],
                "severity": "critical",
                "regulation": "Investment Advisers Act",
                "penalty": "Legal liability and fines",
                "risk_level": "critical"
            },
            "suitability": {
                "name": "Suitability Requirements",
                "description": "Check for suitability requirements",
                "keywords": ["suitability", "know your customer", "risk tolerance", "investment objectives"],
                "severity": "high",
                "regulation": "FINRA Rule 2111",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "disclosure_requirements": {
                "name": "Disclosure Requirements",
                "description": "Check for proper disclosure requirements",
                "keywords": ["disclosure", "prospectus", "form adv", "material information"],
                "severity": "high",
                "regulation": "Securities laws",
                "penalty": "SEC enforcement",
                "risk_level": "high"
            },
            "insider_trading": {
                "name": "Insider Trading Prevention",
                "description": "Check for insider trading prevention",
                "keywords": ["insider trading", "material nonpublic information", "tipping", "trading restrictions"],
                "severity": "critical",
                "regulation": "Securities Exchange Act",
                "penalty": "Criminal charges",
                "risk_level": "critical"
            },
            "portfolio_management": {
                "name": "Portfolio Management Standards",
                "description": "Check for portfolio management standards",
                "keywords": ["portfolio management", "diversification", "risk management", "rebalancing"],
                "severity": "medium",
                "regulation": "Investment management standards",
                "penalty": "Client losses",
                "risk_level": "medium"
            }
        }
    
    def _load_aml_kyc_rules(self) -> Dict[str, Dict]:
        """Load AML/KYC compliance rules."""
        return {
            "customer_identification": {
                "name": "Customer Identification Program",
                "description": "Check for customer identification requirements",
                "keywords": ["customer identification", "cip", "identity verification", "documentation"],
                "severity": "critical",
                "regulation": "USA PATRIOT Act",
                "penalty": "Criminal and civil penalties",
                "risk_level": "critical"
            },
            "suspicious_activity": {
                "name": "Suspicious Activity Reporting",
                "description": "Check for suspicious activity reporting",
                "keywords": ["suspicious activity", "sar", "suspicious transaction", "red flags"],
                "severity": "critical",
                "regulation": "Bank Secrecy Act",
                "penalty": "Criminal and civil penalties",
                "risk_level": "critical"
            },
            "enhanced_due_diligence": {
                "name": "Enhanced Due Diligence",
                "description": "Check for enhanced due diligence requirements",
                "keywords": ["enhanced due diligence", "edd", "high-risk customer", "politically exposed person"],
                "severity": "high",
                "regulation": "BSA/AML regulations",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "transaction_monitoring": {
                "name": "Transaction Monitoring",
                "description": "Check for transaction monitoring systems",
                "keywords": ["transaction monitoring", "aml monitoring", "unusual activity", "thresholds"],
                "severity": "high",
                "regulation": "BSA/AML regulations",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "record_keeping": {
                "name": "Record Keeping Requirements",
                "description": "Check for record keeping requirements",
                "keywords": ["record keeping", "documentation", "retention", "audit trail"],
                "severity": "medium",
                "regulation": "BSA/AML regulations",
                "penalty": "Regulatory action",
                "risk_level": "medium"
            }
        }
    
    def _load_basel_rules(self) -> Dict[str, Dict]:
        """Load Basel compliance rules."""
        return {
            "basel_iii_capital": {
                "name": "Basel III Capital Requirements",
                "description": "Check for Basel III capital requirements",
                "keywords": ["basel iii", "capital requirements", "common equity tier 1", "cet1", "capital buffer"],
                "severity": "critical",
                "regulation": "Basel III",
                "penalty": "Regulatory restrictions",
                "risk_level": "critical"
            },
            "leverage_ratio": {
                "name": "Leverage Ratio Requirements",
                "description": "Check for leverage ratio requirements",
                "keywords": ["leverage ratio", "tier 1 leverage ratio", "supplementary leverage ratio"],
                "severity": "high",
                "regulation": "Basel III",
                "penalty": "Regulatory restrictions",
                "risk_level": "high"
            },
            "liquidity_coverage": {
                "name": "Liquidity Coverage Ratio",
                "description": "Check for liquidity coverage ratio requirements",
                "keywords": ["liquidity coverage ratio", "lcr", "high quality liquid assets", "hqla"],
                "severity": "high",
                "regulation": "Basel III",
                "penalty": "Regulatory restrictions",
                "risk_level": "high"
            },
            "net_stable_funding": {
                "name": "Net Stable Funding Ratio",
                "description": "Check for net stable funding ratio requirements",
                "keywords": ["net stable funding ratio", "nsfr", "stable funding", "available stable funding"],
                "severity": "high",
                "regulation": "Basel III",
                "penalty": "Regulatory restrictions",
                "risk_level": "high"
            },
            "stress_testing": {
                "name": "Stress Testing Requirements",
                "description": "Check for stress testing requirements",
                "keywords": ["stress testing", "scenario analysis", "capital planning", "ccar"],
                "severity": "medium",
                "regulation": "Basel III",
                "penalty": "Regulatory oversight",
                "risk_level": "medium"
            }
        }
    
    def _load_financial_reporting_rules(self) -> Dict[str, Dict]:
        """Load financial reporting compliance rules."""
        return {
            "gaap_compliance": {
                "name": "GAAP Compliance",
                "description": "Check for GAAP compliance",
                "keywords": ["gaap", "generally accepted accounting principles", "accounting standards", "financial statements"],
                "severity": "high",
                "regulation": "GAAP",
                "penalty": "SEC enforcement",
                "risk_level": "high"
            },
            "ifrs_compliance": {
                "name": "IFRS Compliance",
                "description": "Check for IFRS compliance",
                "keywords": ["ifrs", "international financial reporting standards", "accounting standards"],
                "severity": "high",
                "regulation": "IFRS",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "internal_controls": {
                "name": "Internal Controls",
                "description": "Check for internal controls over financial reporting",
                "keywords": ["internal controls", "sox", "sarbanes-oxley", "control environment"],
                "severity": "high",
                "regulation": "SOX",
                "penalty": "SEC enforcement",
                "risk_level": "high"
            },
            "audit_requirements": {
                "name": "Audit Requirements",
                "description": "Check for audit requirements",
                "keywords": ["audit", "independent auditor", "audit opinion", "audit committee"],
                "severity": "high",
                "regulation": "Various securities laws",
                "penalty": "SEC enforcement",
                "risk_level": "high"
            },
            "disclosure_controls": {
                "name": "Disclosure Controls",
                "description": "Check for disclosure controls and procedures",
                "keywords": ["disclosure controls", "material information", "timely disclosure", "materiality"],
                "severity": "medium",
                "regulation": "Securities laws",
                "penalty": "SEC enforcement",
                "risk_level": "medium"
            }
        }
    
    def _load_insurance_rules(self) -> Dict[str, Dict]:
        """Load insurance compliance rules."""
        return {
            "solvency_requirements": {
                "name": "Solvency Requirements",
                "description": "Check for solvency requirements",
                "keywords": ["solvency", "capital requirements", "risk-based capital", "rbc"],
                "severity": "critical",
                "regulation": "State insurance laws",
                "penalty": "Regulatory action",
                "risk_level": "critical"
            },
            "reserve_requirements": {
                "name": "Reserve Requirements",
                "description": "Check for reserve requirements",
                "keywords": ["reserves", "loss reserves", "claim reserves", "actuarial reserves"],
                "severity": "high",
                "regulation": "State insurance laws",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "underwriting_standards": {
                "name": "Underwriting Standards",
                "description": "Check for underwriting standards",
                "keywords": ["underwriting", "risk assessment", "pricing", "policy terms"],
                "severity": "high",
                "regulation": "State insurance laws",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "claims_handling": {
                "name": "Claims Handling",
                "description": "Check for claims handling requirements",
                "keywords": ["claims handling", "claim investigation", "settlement", "bad faith"],
                "severity": "medium",
                "regulation": "State insurance laws",
                "penalty": "Legal liability",
                "risk_level": "medium"
            },
            "market_conduct": {
                "name": "Market Conduct",
                "description": "Check for market conduct requirements",
                "keywords": ["market conduct", "fair practices", "consumer protection", "sales practices"],
                "severity": "medium",
                "regulation": "State insurance laws",
                "penalty": "Regulatory action",
                "risk_level": "medium"
            }
        }
    
    def _load_crypto_rules(self) -> Dict[str, Dict]:
        """Load cryptocurrency compliance rules."""
        return {
            "aml_crypto": {
                "name": "Crypto AML Requirements",
                "description": "Check for cryptocurrency AML requirements",
                "keywords": ["crypto aml", "virtual currency", "digital asset", "blockchain", "aml"],
                "severity": "critical",
                "regulation": "BSA/AML regulations",
                "penalty": "Criminal and civil penalties",
                "risk_level": "critical"
            },
            "kyc_crypto": {
                "name": "Crypto KYC Requirements",
                "description": "Check for cryptocurrency KYC requirements",
                "keywords": ["crypto kyc", "customer identification", "identity verification", "wallet verification"],
                "severity": "critical",
                "regulation": "BSA/AML regulations",
                "penalty": "Criminal and civil penalties",
                "risk_level": "critical"
            },
            "travel_rule": {
                "name": "Travel Rule Compliance",
                "description": "Check for travel rule compliance",
                "keywords": ["travel rule", "funds transfer", "originator", "beneficiary", "vasp"],
                "severity": "high",
                "regulation": "BSA regulations",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "custody_requirements": {
                "name": "Crypto Custody Requirements",
                "description": "Check for crypto custody requirements",
                "keywords": ["crypto custody", "digital asset custody", "custodial services", "safekeeping"],
                "severity": "high",
                "regulation": "Various regulations",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "securities_laws": {
                "name": "Securities Laws Compliance",
                "description": "Check for securities laws compliance",
                "keywords": ["securities laws", "howey test", "investment contract", "token offering"],
                "severity": "high",
                "regulation": "Securities laws",
                "penalty": "SEC enforcement",
                "risk_level": "high"
            }
        }
    
    def _load_fintech_rules(self) -> Dict[str, Dict]:
        """Load fintech compliance rules."""
        return {
            "digital_banking": {
                "name": "Digital Banking Compliance",
                "description": "Check for digital banking compliance",
                "keywords": ["digital banking", "online banking", "mobile banking", "digital channels"],
                "severity": "high",
                "regulation": "Various banking regulations",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "payment_systems": {
                "name": "Payment Systems Compliance",
                "description": "Check for payment systems compliance",
                "keywords": ["payment systems", "ach", "wire transfers", "payment processing"],
                "severity": "high",
                "regulation": "Various payment regulations",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "data_protection": {
                "name": "Data Protection Requirements",
                "description": "Check for data protection requirements",
                "keywords": ["data protection", "privacy", "cybersecurity", "data security"],
                "severity": "high",
                "regulation": "Various privacy laws",
                "penalty": "Regulatory action",
                "risk_level": "high"
            },
            "api_security": {
                "name": "API Security Requirements",
                "description": "Check for API security requirements",
                "keywords": ["api security", "open banking", "api standards", "authentication"],
                "severity": "medium",
                "regulation": "Various regulations",
                "penalty": "Security breaches",
                "risk_level": "medium"
            },
            "regulatory_sandbox": {
                "name": "Regulatory Sandbox Compliance",
                "description": "Check for regulatory sandbox compliance",
                "keywords": ["regulatory sandbox", "innovation", "testing", "pilot program"],
                "severity": "medium",
                "regulation": "Various sandbox programs",
                "penalty": "Program termination",
                "risk_level": "medium"
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
    
    async def analyze_banking_compliance(self, text: str, context: Optional[Dict] = None) -> FinanceAnalysis:
        """Analyze banking compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each banking rule
            for rule_id, rule in self.banking_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = FinanceViolation(
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
                    "Conduct comprehensive banking compliance audit",
                    "Implement capital adequacy monitoring",
                    "Establish liquidity management framework",
                    "Train staff on banking regulations",
                    "Review and update risk management policies"
                ]
            else:
                recommendations = [
                    "Maintain current banking compliance practices",
                    "Regularly review banking regulations",
                    "Conduct periodic compliance training"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("finance", "banking_analysis", duration)
            metrics_service.record_reasoning_confidence("finance", "banking_analysis", confidence)
            
            return FinanceAnalysis(
                domain=FinanceDomain.BANKING,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.banking_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("finance", "banking_analysis", str(e))
            raise
    
    async def analyze_investment_compliance(self, text: str, context: Optional[Dict] = None) -> FinanceAnalysis:
        """Analyze investment compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each investment rule
            for rule_id, rule in self.investment_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = FinanceViolation(
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
                    "Conduct comprehensive investment compliance audit",
                    "Implement fiduciary duty framework",
                    "Establish suitability assessment procedures",
                    "Train staff on investment regulations",
                    "Review and update disclosure procedures"
                ]
            else:
                recommendations = [
                    "Maintain current investment compliance practices",
                    "Regularly review investment regulations",
                    "Conduct periodic compliance training"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("finance", "investment_analysis", duration)
            metrics_service.record_reasoning_confidence("finance", "investment_analysis", confidence)
            
            return FinanceAnalysis(
                domain=FinanceDomain.INVESTMENT,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.investment_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("finance", "investment_analysis", str(e))
            raise
    
    async def analyze_aml_kyc_compliance(self, text: str, context: Optional[Dict] = None) -> FinanceAnalysis:
        """Analyze AML/KYC compliance of given text."""
        start_time = datetime.now()
        
        try:
            violations = []
            recommendations = []
            risk_score = 0.0
            
            # Check each AML/KYC rule
            for rule_id, rule in self.aml_kyc_rules.items():
                if self._check_rule_violation(text, rule):
                    violation = FinanceViolation(
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
                    "Conduct comprehensive AML/KYC compliance audit",
                    "Implement customer identification program",
                    "Establish suspicious activity monitoring",
                    "Train staff on AML/KYC requirements",
                    "Review and update due diligence procedures"
                ]
            else:
                recommendations = [
                    "Maintain current AML/KYC compliance practices",
                    "Regularly review AML/KYC regulations",
                    "Conduct periodic AML/KYC training"
                ]
            
            is_compliant = len(violations) == 0
            confidence = max(0.1, 1.0 - risk_score)
            
            # Record metrics
            duration = (datetime.now() - start_time).total_seconds()
            metrics_service.record_reasoning_response_time("finance", "aml_kyc_analysis", duration)
            metrics_service.record_reasoning_confidence("finance", "aml_kyc_analysis", confidence)
            
            return FinanceAnalysis(
                domain=FinanceDomain.AML_KYC,
                is_compliant=is_compliant,
                confidence=confidence,
                violations=violations,
                recommendations=recommendations,
                risk_score=min(1.0, risk_score),
                analysis_timestamp=datetime.now(),
                metadata={
                    "rules_checked": len(self.aml_kyc_rules),
                    "violations_found": len(violations),
                    "analysis_duration": duration
                }
            )
            
        except Exception as e:
            metrics_service.record_reasoning_error("finance", "aml_kyc_analysis", str(e))
            raise
    
    async def analyze_comprehensive_finance(self, text: str, context: Optional[Dict] = None) -> Dict[str, FinanceAnalysis]:
        """Analyze comprehensive finance compliance across all domains."""
        results = {}
        
        # Analyze each domain
        results["banking"] = await self.analyze_banking_compliance(text, context)
        results["investment"] = await self.analyze_investment_compliance(text, context)
        results["aml_kyc"] = await self.analyze_aml_kyc_compliance(text, context)
        
        return results


# Global instance
finance_pilot = FinanceCompliancePilot()
