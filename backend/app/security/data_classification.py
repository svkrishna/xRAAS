"""
Data Classification Management
Data sensitivity classification and handling for compliance and security.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)


class DataSensitivityLevel(str, Enum):
    """Data sensitivity levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    HIGHLY_RESTRICTED = "highly_restricted"


class DataCategory(str, Enum):
    """Data categories."""
    PERSONAL = "personal"
    FINANCIAL = "financial"
    HEALTH = "health"
    LEGAL = "legal"
    TECHNICAL = "technical"
    BUSINESS = "business"
    OPERATIONAL = "operational"


class ComplianceFramework(str, Enum):
    """Compliance frameworks."""
    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOX = "sox"
    PCI_DSS = "pci_dss"
    CCPA = "ccpa"
    ISO27001 = "iso27001"


@dataclass
class DataPattern:
    """Pattern for identifying sensitive data."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    pattern: str = ""
    category: DataCategory = DataCategory.PERSONAL
    sensitivity_level: DataSensitivityLevel = DataSensitivityLevel.CONFIDENTIAL
    compliance_frameworks: List[ComplianceFramework] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "pattern": self.pattern,
            "category": self.category.value,
            "sensitivity_level": self.sensitivity_level.value,
            "compliance_frameworks": [fw.value for fw in self.compliance_frameworks],
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataPattern':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            pattern=data.get("pattern", ""),
            category=DataCategory(data.get("category", "personal")),
            sensitivity_level=DataSensitivityLevel(data.get("sensitivity_level", "confidential")),
            compliance_frameworks=[ComplianceFramework(fw) for fw in data.get("compliance_frameworks", [])],
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat()))
        )


@dataclass
class DataClassification:
    """Data classification result."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    data_id: str = ""
    content: str = ""
    sensitivity_level: DataSensitivityLevel = DataSensitivityLevel.PUBLIC
    categories: List[DataCategory] = field(default_factory=list)
    patterns_found: List[DataPattern] = field(default_factory=list)
    compliance_frameworks: List[ComplianceFramework] = field(default_factory=list)
    classification_date: datetime = field(default_factory=datetime.utcnow)
    confidence_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "data_id": self.data_id,
            "content": self.content,
            "sensitivity_level": self.sensitivity_level.value,
            "categories": [cat.value for cat in self.categories],
            "patterns_found": [pattern.to_dict() for pattern in self.patterns_found],
            "compliance_frameworks": [fw.value for fw in self.compliance_frameworks],
            "classification_date": self.classification_date.isoformat(),
            "confidence_score": self.confidence_score,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataClassification':
        """Create from dictionary."""
        classification = cls(
            id=data.get("id", str(uuid.uuid4())),
            data_id=data.get("data_id", ""),
            content=data.get("content", ""),
            sensitivity_level=DataSensitivityLevel(data.get("sensitivity_level", "public")),
            categories=[DataCategory(cat) for cat in data.get("categories", [])],
            compliance_frameworks=[ComplianceFramework(fw) for fw in data.get("compliance_frameworks", [])],
            classification_date=datetime.fromisoformat(data.get("classification_date", datetime.utcnow().isoformat())),
            confidence_score=data.get("confidence_score", 0.0),
            metadata=data.get("metadata", {})
        )
        
        # Add patterns found
        for pattern_data in data.get("patterns_found", []):
            classification.patterns_found.append(DataPattern.from_dict(pattern_data))
        
        return classification


class DataClassifier:
    """Classifies data based on sensitivity and compliance requirements."""
    
    def __init__(self):
        self.patterns: List[DataPattern] = []
        self.logger = logging.getLogger(__name__)
        
        # Initialize default patterns
        self._initialize_default_patterns()
    
    def add_pattern(self, pattern: DataPattern) -> None:
        """Add a data pattern for classification."""
        self.patterns.append(pattern)
        self.logger.info(f"Added data pattern: {pattern.name}")
    
    def remove_pattern(self, pattern_id: str) -> bool:
        """Remove a data pattern."""
        for i, pattern in enumerate(self.patterns):
            if pattern.id == pattern_id:
                del self.patterns[i]
                self.logger.info(f"Removed data pattern: {pattern.name}")
                return True
        return False
    
    def classify_data(self, content: str, data_id: str = "") -> DataClassification:
        """Classify data based on content analysis."""
        try:
            patterns_found = []
            categories = set()
            compliance_frameworks = set()
            max_sensitivity = DataSensitivityLevel.PUBLIC
            
            # Analyze content against patterns
            for pattern in self.patterns:
                if re.search(pattern.pattern, content, re.IGNORECASE):
                    patterns_found.append(pattern)
                    categories.add(pattern.category)
                    compliance_frameworks.update(pattern.compliance_frameworks)
                    
                    # Update sensitivity level
                    if self._get_sensitivity_level_value(pattern.sensitivity_level) > self._get_sensitivity_level_value(max_sensitivity):
                        max_sensitivity = pattern.sensitivity_level
            
            # Calculate confidence score
            confidence_score = min(1.0, len(patterns_found) * 0.3)
            
            classification = DataClassification(
                data_id=data_id,
                content=content,
                sensitivity_level=max_sensitivity,
                categories=list(categories),
                patterns_found=patterns_found,
                compliance_frameworks=list(compliance_frameworks),
                confidence_score=confidence_score
            )
            
            self.logger.info(f"Classified data {data_id} as {max_sensitivity.value}")
            return classification
            
        except Exception as e:
            self.logger.error(f"Error classifying data: {e}")
            # Return default classification
            return DataClassification(
                data_id=data_id,
                content=content,
                sensitivity_level=DataSensitivityLevel.PUBLIC,
                confidence_score=0.0
            )
    
    def get_handling_requirements(self, classification: DataClassification) -> Dict[str, Any]:
        """Get handling requirements for classified data."""
        requirements = {
            "encryption_required": classification.sensitivity_level in [
                DataSensitivityLevel.CONFIDENTIAL,
                DataSensitivityLevel.RESTRICTED,
                DataSensitivityLevel.HIGHLY_RESTRICTED
            ],
            "access_controls": classification.sensitivity_level in [
                DataSensitivityLevel.RESTRICTED,
                DataSensitivityLevel.HIGHLY_RESTRICTED
            ],
            "audit_logging": True,  # Always log access
            "retention_policy": self._get_retention_policy(classification),
            "compliance_requirements": self._get_compliance_requirements(classification)
        }
        
        return requirements
    
    def _get_sensitivity_level_value(self, level: DataSensitivityLevel) -> int:
        """Get numeric value for sensitivity level comparison."""
        values = {
            DataSensitivityLevel.PUBLIC: 1,
            DataSensitivityLevel.INTERNAL: 2,
            DataSensitivityLevel.CONFIDENTIAL: 3,
            DataSensitivityLevel.RESTRICTED: 4,
            DataSensitivityLevel.HIGHLY_RESTRICTED: 5
        }
        return values.get(level, 1)
    
    def _get_retention_policy(self, classification: DataClassification) -> Dict[str, Any]:
        """Get retention policy for classified data."""
        policies = {
            DataSensitivityLevel.PUBLIC: {"retention_days": 365, "auto_delete": True},
            DataSensitivityLevel.INTERNAL: {"retention_days": 730, "auto_delete": True},
            DataSensitivityLevel.CONFIDENTIAL: {"retention_days": 1825, "auto_delete": False},
            DataSensitivityLevel.RESTRICTED: {"retention_days": 2555, "auto_delete": False},
            DataSensitivityLevel.HIGHLY_RESTRICTED: {"retention_days": 3650, "auto_delete": False}
        }
        return policies.get(classification.sensitivity_level, policies[DataSensitivityLevel.PUBLIC])
    
    def _get_compliance_requirements(self, classification: DataClassification) -> List[str]:
        """Get compliance requirements for classified data."""
        requirements = []
        
        for framework in classification.compliance_frameworks:
            if framework == ComplianceFramework.GDPR:
                requirements.extend([
                    "Data subject consent required",
                    "Right to be forgotten",
                    "Data portability"
                ])
            elif framework == ComplianceFramework.HIPAA:
                requirements.extend([
                    "PHI protection required",
                    "Access controls mandatory",
                    "Audit trail required"
                ])
            elif framework == ComplianceFramework.SOX:
                requirements.extend([
                    "Financial data protection",
                    "Audit trail required",
                    "Access controls mandatory"
                ])
            elif framework == ComplianceFramework.PCI_DSS:
                requirements.extend([
                    "Cardholder data protection",
                    "Encryption required",
                    "Access controls mandatory"
                ])
        
        return requirements
    
    def _initialize_default_patterns(self) -> None:
        """Initialize default data patterns."""
        
        # Email patterns
        email_pattern = DataPattern(
            name="Email Address",
            description="Email address pattern",
            pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            category=DataCategory.PERSONAL,
            sensitivity_level=DataSensitivityLevel.CONFIDENTIAL,
            compliance_frameworks=[ComplianceFramework.GDPR, ComplianceFramework.CCPA]
        )
        self.patterns.append(email_pattern)
        
        # Credit card patterns
        credit_card_pattern = DataPattern(
            name="Credit Card Number",
            description="Credit card number pattern",
            pattern=r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            category=DataCategory.FINANCIAL,
            sensitivity_level=DataSensitivityLevel.HIGHLY_RESTRICTED,
            compliance_frameworks=[ComplianceFramework.PCI_DSS]
        )
        self.patterns.append(credit_card_pattern)
        
        # SSN patterns
        ssn_pattern = DataPattern(
            name="Social Security Number",
            description="US Social Security Number pattern",
            pattern=r'\b\d{3}-\d{2}-\d{4}\b',
            category=DataCategory.PERSONAL,
            sensitivity_level=DataSensitivityLevel.HIGHLY_RESTRICTED,
            compliance_frameworks=[ComplianceFramework.GDPR, ComplianceFramework.CCPA]
        )
        self.patterns.append(ssn_pattern)
        
        # Phone number patterns
        phone_pattern = DataPattern(
            name="Phone Number",
            description="Phone number pattern",
            pattern=r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            category=DataCategory.PERSONAL,
            sensitivity_level=DataSensitivityLevel.CONFIDENTIAL,
            compliance_frameworks=[ComplianceFramework.GDPR, ComplianceFramework.CCPA]
        )
        self.patterns.append(phone_pattern)
        
        # IP address patterns
        ip_pattern = DataPattern(
            name="IP Address",
            description="IP address pattern",
            pattern=r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            category=DataCategory.TECHNICAL,
            sensitivity_level=DataSensitivityLevel.INTERNAL,
            compliance_frameworks=[]
        )
        self.patterns.append(ip_pattern)
        
        self.logger.info(f"Initialized {len(self.patterns)} default data patterns")


# Global data classifier instance
data_classifier = DataClassifier()
