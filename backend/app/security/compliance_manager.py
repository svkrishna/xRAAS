"""
Enterprise Compliance Management System
Comprehensive compliance framework for SOC2, ISO27001, HIPAA, GDPR, and other regulations.
"""

from typing import Dict, Any, List, Optional, Set
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import json
import asyncio
from pathlib import Path

from app.security.audit_logger import ComplianceFramework, audit_logger, AuditEventType


class ComplianceStatus(str, Enum):
    """Compliance status levels."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    AT_RISK = "at_risk"
    PENDING_REVIEW = "pending_review"
    REMEDIATION_REQUIRED = "remediation_required"


class DataProcessingPurpose(str, Enum):
    """GDPR Article 6 lawful basis for processing."""
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"
    VITAL_INTERESTS = "vital_interests"
    PUBLIC_TASK = "public_task"
    LEGITIMATE_INTERESTS = "legitimate_interests"


@dataclass
class ComplianceRequirement:
    """Individual compliance requirement definition."""
    id: str
    framework: ComplianceFramework
    category: str
    title: str
    description: str
    implementation_guide: str
    verification_method: str
    required_evidence: List[str]
    risk_level: str
    automation_possible: bool


@dataclass
class ComplianceAssessment:
    """Compliance assessment result."""
    requirement_id: str
    status: ComplianceStatus
    last_assessed: datetime
    evidence: List[str]
    findings: List[str]
    remediation_plan: Optional[str]
    next_review_date: datetime
    assessor: str


class ComplianceManager:
    """
    Enterprise compliance management system.
    
    Manages compliance across multiple frameworks:
    - SOC2 Type II
    - ISO27001
    - HIPAA
    - GDPR
    - CCPA
    - SOX
    - PCI DSS
    """
    
    def __init__(self):
        self.requirements = self._load_compliance_requirements()
        self.assessments: Dict[str, ComplianceAssessment] = {}
        self.data_retention_policies = self._load_retention_policies()
        self.consent_records: Dict[str, Dict[str, Any]] = {}
    
    def _load_compliance_requirements(self) -> Dict[str, ComplianceRequirement]:
        """Load compliance requirements from configuration."""
        requirements = {}
        
        # SOC2 Type II Requirements
        soc2_requirements = [
            {
                "id": "CC1.1",
                "framework": ComplianceFramework.SOC2_TYPE_II,
                "category": "Control Environment",
                "title": "Organizational Structure",
                "description": "The entity demonstrates a commitment to integrity and ethical values",
                "implementation_guide": "Establish code of conduct and ethical guidelines",
                "verification_method": "Policy review and employee attestation",
                "required_evidence": ["code_of_conduct", "ethics_training_records"],
                "risk_level": "high",
                "automation_possible": True
            },
            {
                "id": "CC2.1", 
                "framework": ComplianceFramework.SOC2_TYPE_II,
                "category": "Communication and Information",
                "title": "Information Requirements",
                "description": "The entity obtains or generates and uses relevant, quality information",
                "implementation_guide": "Implement information governance framework",
                "verification_method": "Information flow documentation",
                "required_evidence": ["data_classification", "information_governance_policy"],
                "risk_level": "medium",
                "automation_possible": True
            }
        ]
        
        # HIPAA Requirements
        hipaa_requirements = [
            {
                "id": "164.312(a)(1)",
                "framework": ComplianceFramework.HIPAA,
                "category": "Access Control",
                "title": "Unique User Identification",
                "description": "Assign a unique name and/or number for identifying and tracking user identity",
                "implementation_guide": "Implement unique user IDs for all system access",
                "verification_method": "User access audit and review",
                "required_evidence": ["user_access_logs", "identity_management_system"],
                "risk_level": "high",
                "automation_possible": True
            },
            {
                "id": "164.312(e)(1)",
                "framework": ComplianceFramework.HIPAA,
                "category": "Transmission Security",
                "title": "Transmission Security",
                "description": "Implement technical safeguards to guard against unauthorized access to ePHI",
                "implementation_guide": "Encrypt all ePHI transmissions",
                "verification_method": "Encryption audit and penetration testing",
                "required_evidence": ["encryption_certificates", "transmission_logs"],
                "risk_level": "critical",
                "automation_possible": True
            }
        ]
        
        # GDPR Requirements
        gdpr_requirements = [
            {
                "id": "Article_25",
                "framework": ComplianceFramework.GDPR,
                "category": "Data Protection by Design",
                "title": "Data Protection by Design and by Default",
                "description": "Implement appropriate technical and organisational measures",
                "implementation_guide": "Embed data protection principles in system design",
                "verification_method": "Privacy impact assessment",
                "required_evidence": ["privacy_impact_assessments", "data_protection_policies"],
                "risk_level": "high",
                "automation_possible": False
            },
            {
                "id": "Article_32",
                "framework": ComplianceFramework.GDPR,
                "category": "Security of Processing",
                "title": "Security of Processing",
                "description": "Implement appropriate technical and organisational measures",
                "implementation_guide": "Implement encryption, pseudonymisation, and access controls",
                "verification_method": "Security audit and penetration testing",
                "required_evidence": ["security_controls", "encryption_implementation"],
                "risk_level": "critical",
                "automation_possible": True
            }
        ]
        
        all_requirements = soc2_requirements + hipaa_requirements + gdpr_requirements
        
        for req_data in all_requirements:
            req = ComplianceRequirement(**req_data)
            requirements[req.id] = req
        
        return requirements
    
    def _load_retention_policies(self) -> Dict[str, Dict[str, Any]]:
        """Load data retention policies for compliance."""
        return {
            "audit_logs": {
                "retention_period_days": 2557,  # 7 years for SOC2
                "framework": [ComplianceFramework.SOC2_TYPE_II, ComplianceFramework.ISO27001],
                "auto_deletion": True,
                "backup_required": True
            },
            "user_data": {
                "retention_period_days": 1095,  # 3 years default
                "framework": [ComplianceFramework.GDPR],
                "auto_deletion": False,  # Requires consent verification
                "backup_required": True
            },
            "health_data": {
                "retention_period_days": 2190,  # 6 years for HIPAA
                "framework": [ComplianceFramework.HIPAA],
                "auto_deletion": False,
                "backup_required": True
            },
            "financial_data": {
                "retention_period_days": 2557,  # 7 years for SOX
                "framework": [ComplianceFramework.SOX],
                "auto_deletion": False,
                "backup_required": True
            }
        }
    
    async def assess_compliance_requirement(
        self,
        requirement_id: str,
        assessor: str,
        evidence: List[str],
        findings: List[str]
    ) -> ComplianceAssessment:
        """
        Assess a specific compliance requirement.
        
        Args:
            requirement_id: ID of the requirement to assess
            assessor: Person conducting the assessment
            evidence: List of evidence items
            findings: Assessment findings
            
        Returns:
            ComplianceAssessment: Assessment result
        """
        requirement = self.requirements.get(requirement_id)
        if not requirement:
            raise ValueError(f"Unknown requirement: {requirement_id}")
        
        # Determine compliance status based on findings
        status = ComplianceStatus.COMPLIANT
        if any("non-compliant" in finding.lower() for finding in findings):
            status = ComplianceStatus.NON_COMPLIANT
        elif any("risk" in finding.lower() for finding in findings):
            status = ComplianceStatus.AT_RISK
        
        # Create assessment
        assessment = ComplianceAssessment(
            requirement_id=requirement_id,
            status=status,
            last_assessed=datetime.now(timezone.utc),
            evidence=evidence,
            findings=findings,
            remediation_plan=None,
            next_review_date=datetime.now(timezone.utc) + timedelta(days=90),
            assessor=assessor
        )
        
        # Store assessment
        self.assessments[requirement_id] = assessment
        
        # Log audit event
        audit_logger.log_event(
            event_type=AuditEventType.COMPLIANCE_CHECK,
            action=f"assess_requirement_{requirement_id}",
            result="success",
            details={
                "requirement_id": requirement_id,
                "status": status.value,
                "findings_count": len(findings),
                "evidence_count": len(evidence)
            },
            user_id=assessor,
            compliance_frameworks=[requirement.framework],
            risk_level="medium"
        )
        
        return assessment
    
    def get_compliance_dashboard(self) -> Dict[str, Any]:
        """
        Generate compliance dashboard with overall status.
        
        Returns:
            Dict containing compliance metrics and status
        """
        total_requirements = len(self.requirements)
        assessed_requirements = len(self.assessments)
        
        status_counts = {}
        for status in ComplianceStatus:
            status_counts[status.value] = sum(
                1 for assessment in self.assessments.values()
                if assessment.status == status
            )
        
        framework_status = {}
        for framework in ComplianceFramework:
            framework_reqs = [req for req in self.requirements.values() 
                            if req.framework == framework]
            framework_assessments = [assessment for assessment in self.assessments.values()
                                   if self.requirements[assessment.requirement_id].framework == framework]
            
            compliant_count = sum(
                1 for assessment in framework_assessments
                if assessment.status == ComplianceStatus.COMPLIANT
            )
            
            framework_status[framework.value] = {
                "total_requirements": len(framework_reqs),
                "assessed": len(framework_assessments),
                "compliant": compliant_count,
                "compliance_percentage": (compliant_count / len(framework_reqs) * 100) if framework_reqs else 0
            }
        
        return {
            "overall_status": {
                "total_requirements": total_requirements,
                "assessed_requirements": assessed_requirements,
                "assessment_coverage": (assessed_requirements / total_requirements * 100) if total_requirements else 0
            },
            "status_distribution": status_counts,
            "framework_status": framework_status,
            "high_risk_items": [
                assessment.requirement_id for assessment in self.assessments.values()
                if assessment.status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.REMEDIATION_REQUIRED]
            ],
            "upcoming_reviews": [
                {
                    "requirement_id": assessment.requirement_id,
                    "next_review": assessment.next_review_date.isoformat(),
                    "framework": self.requirements[assessment.requirement_id].framework.value
                }
                for assessment in self.assessments.values()
                if assessment.next_review_date <= datetime.now(timezone.utc) + timedelta(days=30)
            ]
        }
    
    def record_consent(
        self,
        user_id: str,
        purpose: DataProcessingPurpose,
        consent_given: bool,
        consent_text: str,
        source_ip: str,
        user_agent: str
    ) -> str:
        """
        Record user consent for GDPR compliance.
        
        Args:
            user_id: User providing consent
            purpose: Purpose of data processing
            consent_given: Whether consent was given
            consent_text: Text of consent request
            source_ip: IP address of consent
            user_agent: User agent string
            
        Returns:
            str: Consent record ID
        """
        consent_id = f"consent_{user_id}_{purpose.value}_{datetime.now().timestamp()}"
        
        consent_record = {
            "consent_id": consent_id,
            "user_id": user_id,
            "purpose": purpose.value,
            "consent_given": consent_given,
            "consent_text": consent_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": source_ip,
            "user_agent": user_agent,
            "withdrawal_date": None,
            "valid": True
        }
        
        if user_id not in self.consent_records:
            self.consent_records[user_id] = {}
        
        self.consent_records[user_id][purpose.value] = consent_record
        
        # Log audit event
        audit_logger.log_event(
            event_type=AuditEventType.DATA_ACCESS,
            action=f"record_consent",
            result="success",
            details={
                "consent_id": consent_id,
                "purpose": purpose.value,
                "consent_given": consent_given
            },
            user_id=user_id,
            source_ip=source_ip,
            user_agent=user_agent,
            compliance_frameworks=[ComplianceFramework.GDPR],
            risk_level="medium"
        )
        
        return consent_id
    
    def check_consent(self, user_id: str, purpose: DataProcessingPurpose) -> bool:
        """
        Check if user has given valid consent for specific purpose.
        
        Args:
            user_id: User to check consent for
            purpose: Purpose of data processing
            
        Returns:
            bool: True if valid consent exists
        """
        if user_id not in self.consent_records:
            return False
        
        consent_record = self.consent_records[user_id].get(purpose.value)
        if not consent_record:
            return False
        
        return consent_record["consent_given"] and consent_record["valid"]
    
    def generate_compliance_report(
        self,
        framework: ComplianceFramework,
        include_remediation: bool = True
    ) -> Dict[str, Any]:
        """
        Generate comprehensive compliance report for specific framework.
        
        Args:
            framework: Compliance framework to report on
            include_remediation: Include remediation recommendations
            
        Returns:
            Dict: Comprehensive compliance report
        """
        framework_requirements = [
            req for req in self.requirements.values()
            if req.framework == framework
        ]
        
        framework_assessments = [
            assessment for assessment in self.assessments.values()
            if self.requirements[assessment.requirement_id].framework == framework
        ]
        
        compliance_score = 0
        if framework_requirements:
            compliant_count = sum(
                1 for assessment in framework_assessments
                if assessment.status == ComplianceStatus.COMPLIANT
            )
            compliance_score = (compliant_count / len(framework_requirements)) * 100
        
        report = {
            "framework": framework.value,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "compliance_score": compliance_score,
            "total_requirements": len(framework_requirements),
            "assessed_requirements": len(framework_assessments),
            "status_summary": {
                "compliant": sum(1 for a in framework_assessments if a.status == ComplianceStatus.COMPLIANT),
                "non_compliant": sum(1 for a in framework_assessments if a.status == ComplianceStatus.NON_COMPLIANT),
                "at_risk": sum(1 for a in framework_assessments if a.status == ComplianceStatus.AT_RISK),
                "pending_review": sum(1 for a in framework_assessments if a.status == ComplianceStatus.PENDING_REVIEW)
            },
            "requirement_details": [
                {
                    "requirement_id": req.id,
                    "title": req.title,
                    "category": req.category,
                    "risk_level": req.risk_level,
                    "status": self.assessments.get(req.id, {}).get("status", "not_assessed"),
                    "last_assessed": self.assessments.get(req.id, {}).get("last_assessed"),
                    "findings": self.assessments.get(req.id, {}).get("findings", [])
                }
                for req in framework_requirements
            ]
        }
        
        if include_remediation:
            report["remediation_recommendations"] = self._generate_remediation_recommendations(framework)
        
        return report
    
    def _generate_remediation_recommendations(self, framework: ComplianceFramework) -> List[Dict[str, Any]]:
        """Generate remediation recommendations for non-compliant items."""
        recommendations = []
        
        non_compliant_assessments = [
            assessment for assessment in self.assessments.values()
            if (self.requirements[assessment.requirement_id].framework == framework and
                assessment.status in [ComplianceStatus.NON_COMPLIANT, ComplianceStatus.AT_RISK])
        ]
        
        for assessment in non_compliant_assessments:
            requirement = self.requirements[assessment.requirement_id]
            
            recommendations.append({
                "requirement_id": requirement.id,
                "title": requirement.title,
                "priority": "high" if assessment.status == ComplianceStatus.NON_COMPLIANT else "medium",
                "recommended_actions": [
                    requirement.implementation_guide,
                    "Conduct thorough review of current controls",
                    "Implement monitoring and alerting",
                    "Schedule regular compliance assessments"
                ],
                "estimated_effort": "medium",
                "deadline": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
            })
        
        return recommendations


# Global compliance manager instance
compliance_manager = ComplianceManager()
