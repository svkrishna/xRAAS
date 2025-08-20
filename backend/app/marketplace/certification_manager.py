"""
Certification Manager for XReason Marketplace
Handles partner and plugin certification processes.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class CertificationLevel(str, Enum):
    """Certification levels for partners and plugins."""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    VERIFIED = "verified"


class CertificationStatus(str, Enum):
    """Certification status."""
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REVOKED = "revoked"


class CertificationType(str, Enum):
    """Types of certification."""
    PARTNER = "partner"
    PLUGIN = "plugin"
    RULESET = "ruleset"
    INTEGRATION = "integration"
    COMPLIANCE = "compliance"


class ReviewStatus(str, Enum):
    """Review status for certification."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    TECHNICAL_REVIEW = "technical_review"
    SECURITY_REVIEW = "security_review"
    COMPLIANCE_REVIEW = "compliance_review"
    FINAL_REVIEW = "final_review"
    COMPLETED = "completed"


@dataclass
class CertificationRequirement:
    """A requirement for certification."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    category: str = ""
    is_mandatory: bool = True
    weight: float = 1.0
    criteria: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "is_mandatory": self.is_mandatory,
            "weight": self.weight,
            "criteria": self.criteria
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CertificationRequirement':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            category=data.get("category", ""),
            is_mandatory=data.get("is_mandatory", True),
            weight=data.get("weight", 1.0),
            criteria=data.get("criteria", {})
        )


@dataclass
class CertificationReview:
    """A review for certification."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reviewer_id: str = ""
    reviewer_name: str = ""
    status: ReviewStatus = ReviewStatus.NOT_STARTED
    comments: str = ""
    score: float = 0.0
    max_score: float = 100.0
    requirements_met: List[str] = field(default_factory=list)
    requirements_failed: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    review_date: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "reviewer_id": self.reviewer_id,
            "reviewer_name": self.reviewer_name,
            "status": self.status.value,
            "comments": self.comments,
            "score": self.score,
            "max_score": self.max_score,
            "requirements_met": self.requirements_met,
            "requirements_failed": self.requirements_failed,
            "recommendations": self.recommendations,
            "review_date": self.review_date.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CertificationReview':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            reviewer_id=data.get("reviewer_id", ""),
            reviewer_name=data.get("reviewer_name", ""),
            status=ReviewStatus(data.get("status", "not_started")),
            comments=data.get("comments", ""),
            score=data.get("score", 0.0),
            max_score=data.get("max_score", 100.0),
            requirements_met=data.get("requirements_met", []),
            requirements_failed=data.get("requirements_failed", []),
            recommendations=data.get("recommendations", []),
            review_date=datetime.fromisoformat(data.get("review_date", datetime.utcnow().isoformat())),
            metadata=data.get("metadata", {})
        )


@dataclass
class Certification:
    """A certification record."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: str = ""  # Partner ID, Plugin ID, etc.
    entity_type: CertificationType = CertificationType.PARTNER
    level: CertificationLevel = CertificationLevel.BASIC
    status: CertificationStatus = CertificationStatus.PENDING
    issued_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    issued_by: str = ""
    certificate_number: str = ""
    
    # Requirements and reviews
    requirements: List[CertificationRequirement] = field(default_factory=list)
    reviews: List[CertificationReview] = field(default_factory=list)
    
    # Metadata
    description: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type.value,
            "level": self.level.value,
            "status": self.status.value,
            "issued_date": self.issued_date.isoformat() if self.issued_date else None,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "issued_by": self.issued_by,
            "certificate_number": self.certificate_number,
            "requirements": [req.to_dict() for req in self.requirements],
            "reviews": [review.to_dict() for review in self.reviews],
            "description": self.description,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Certification':
        """Create from dictionary."""
        certification = cls(
            id=data.get("id", str(uuid.uuid4())),
            entity_id=data.get("entity_id", ""),
            entity_type=CertificationType(data.get("entity_type", "partner")),
            level=CertificationLevel(data.get("level", "basic")),
            status=CertificationStatus(data.get("status", "pending")),
            issued_by=data.get("issued_by", ""),
            certificate_number=data.get("certificate_number", ""),
            description=data.get("description", ""),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.utcnow().isoformat()))
        )
        
        # Set dates if provided
        if data.get("issued_date"):
            certification.issued_date = datetime.fromisoformat(data["issued_date"])
        if data.get("expiry_date"):
            certification.expiry_date = datetime.fromisoformat(data["expiry_date"])
        
        # Add requirements
        for req_data in data.get("requirements", []):
            certification.requirements.append(CertificationRequirement.from_dict(req_data))
        
        # Add reviews
        for review_data in data.get("reviews", []):
            certification.reviews.append(CertificationReview.from_dict(review_data))
        
        return certification
    
    def is_valid(self) -> bool:
        """Check if certification is valid (not expired or revoked)."""
        if self.status in [CertificationStatus.REVOKED, CertificationStatus.SUSPENDED]:
            return False
        
        if self.expiry_date and datetime.utcnow() > self.expiry_date:
            return False
        
        return True
    
    def get_overall_score(self) -> float:
        """Calculate overall score from reviews."""
        if not self.reviews:
            return 0.0
        
        total_score = sum(review.score for review in self.reviews)
        return total_score / len(self.reviews)
    
    def get_requirements_completion(self) -> Dict[str, Any]:
        """Get requirements completion statistics."""
        total_requirements = len(self.requirements)
        mandatory_requirements = [req for req in self.requirements if req.is_mandatory]
        
        met_requirements = set()
        failed_requirements = set()
        
        for review in self.reviews:
            met_requirements.update(review.requirements_met)
            failed_requirements.update(review.requirements_failed)
        
        return {
            "total": total_requirements,
            "mandatory": len(mandatory_requirements),
            "met": len(met_requirements),
            "failed": len(failed_requirements),
            "completion_percentage": (len(met_requirements) / total_requirements * 100) if total_requirements > 0 else 0,
            "mandatory_completion": all(req.id in met_requirements for req in mandatory_requirements)
        }


class CertificationManager:
    """Manages certification processes for partners and plugins."""
    
    def __init__(self):
        self.certifications: Dict[str, Certification] = {}
        self.requirements_templates: Dict[CertificationType, List[CertificationRequirement]] = {}
        self.reviewers: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize default requirements templates
        self._initialize_default_requirements()
    
    def create_certification_request(self, entity_id: str, entity_type: CertificationType,
                                   level: CertificationLevel, description: str = "",
                                   tags: Optional[List[str]] = None) -> Certification:
        """Create a new certification request."""
        try:
            # Check if certification already exists
            existing = self.get_certification(entity_id, entity_type)
            if existing:
                raise ValueError(f"Certification already exists for {entity_type.value} {entity_id}")
            
            # Create certification
            certification = Certification(
                entity_id=entity_id,
                entity_type=entity_type,
                level=level,
                description=description,
                tags=tags or [],
                certificate_number=self._generate_certificate_number()
            )
            
            # Add default requirements for the type and level
            requirements = self.get_requirements_template(entity_type, level)
            certification.requirements = requirements
            
            # Store certification
            self.certifications[certification.id] = certification
            
            self.logger.info(f"Created certification request for {entity_type.value} {entity_id}")
            return certification
            
        except Exception as e:
            self.logger.error(f"Error creating certification request: {e}")
            raise
    
    def get_certification(self, entity_id: str, entity_type: CertificationType) -> Optional[Certification]:
        """Get certification for an entity."""
        for cert in self.certifications.values():
            if cert.entity_id == entity_id and cert.entity_type == entity_type:
                return cert
        return None
    
    def get_certifications_by_type(self, entity_type: CertificationType) -> List[Certification]:
        """Get all certifications of a specific type."""
        return [cert for cert in self.certifications.values() if cert.entity_type == entity_type]
    
    def get_certifications_by_status(self, status: CertificationStatus) -> List[Certification]:
        """Get all certifications with a specific status."""
        return [cert for cert in self.certifications.values() if cert.status == status]
    
    def add_review(self, certification_id: str, reviewer_id: str, reviewer_name: str,
                  status: ReviewStatus, comments: str = "", score: float = 0.0,
                  requirements_met: Optional[List[str]] = None,
                  requirements_failed: Optional[List[str]] = None,
                  recommendations: Optional[List[str]] = None) -> bool:
        """Add a review to a certification."""
        try:
            certification = self.certifications.get(certification_id)
            if not certification:
                return False
            
            review = CertificationReview(
                reviewer_id=reviewer_id,
                reviewer_name=reviewer_name,
                status=status,
                comments=comments,
                score=score,
                requirements_met=requirements_met or [],
                requirements_failed=requirements_failed or [],
                recommendations=recommendations or []
            )
            
            certification.reviews.append(review)
            certification.updated_at = datetime.utcnow()
            
            # Update certification status based on reviews
            self._update_certification_status(certification)
            
            self.logger.info(f"Added review to certification {certification_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding review: {e}")
            return False
    
    def approve_certification(self, certification_id: str, issued_by: str,
                            expiry_days: int = 365) -> bool:
        """Approve a certification."""
        try:
            certification = self.certifications.get(certification_id)
            if not certification:
                return False
            
            # Check if all mandatory requirements are met
            completion = certification.get_requirements_completion()
            if not completion["mandatory_completion"]:
                raise ValueError("Cannot approve: mandatory requirements not met")
            
            # Approve certification
            certification.status = CertificationStatus.APPROVED
            certification.issued_date = datetime.utcnow()
            certification.expiry_date = datetime.utcnow() + timedelta(days=expiry_days)
            certification.issued_by = issued_by
            certification.updated_at = datetime.utcnow()
            
            self.logger.info(f"Approved certification {certification_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error approving certification: {e}")
            return False
    
    def reject_certification(self, certification_id: str, reason: str) -> bool:
        """Reject a certification."""
        try:
            certification = self.certifications.get(certification_id)
            if not certification:
                return False
            
            certification.status = CertificationStatus.REJECTED
            certification.updated_at = datetime.utcnow()
            
            # Add rejection comment
            rejection_review = CertificationReview(
                reviewer_id="system",
                reviewer_name="System",
                status=ReviewStatus.COMPLETED,
                comments=f"Certification rejected: {reason}",
                score=0.0
            )
            certification.reviews.append(rejection_review)
            
            self.logger.info(f"Rejected certification {certification_id}: {reason}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error rejecting certification: {e}")
            return False
    
    def revoke_certification(self, certification_id: str, reason: str) -> bool:
        """Revoke an approved certification."""
        try:
            certification = self.certifications.get(certification_id)
            if not certification:
                return False
            
            certification.status = CertificationStatus.REVOKED
            certification.updated_at = datetime.utcnow()
            
            # Add revocation comment
            revocation_review = CertificationReview(
                reviewer_id="system",
                reviewer_name="System",
                status=ReviewStatus.COMPLETED,
                comments=f"Certification revoked: {reason}",
                score=0.0
            )
            certification.reviews.append(revocation_review)
            
            self.logger.info(f"Revoked certification {certification_id}: {reason}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error revoking certification: {e}")
            return False
    
    def get_requirements_template(self, entity_type: CertificationType, 
                                level: CertificationLevel) -> List[CertificationRequirement]:
        """Get requirements template for certification type and level."""
        key = f"{entity_type.value}_{level.value}"
        return self.requirements_templates.get(key, [])
    
    def add_requirements_template(self, entity_type: CertificationType, level: CertificationLevel,
                                requirements: List[CertificationRequirement]) -> None:
        """Add a requirements template."""
        key = f"{entity_type.value}_{level.value}"
        self.requirements_templates[key] = requirements
        self.logger.info(f"Added requirements template for {key}")
    
    def get_certification_summary(self, entity_id: str, entity_type: CertificationType) -> Dict[str, Any]:
        """Get certification summary for an entity."""
        certification = self.get_certification(entity_id, entity_type)
        if not certification:
            return {"status": "not_certified"}
        
        return {
            "certification_id": certification.id,
            "level": certification.level.value,
            "status": certification.status.value,
            "is_valid": certification.is_valid(),
            "issued_date": certification.issued_date.isoformat() if certification.issued_date else None,
            "expiry_date": certification.expiry_date.isoformat() if certification.expiry_date else None,
            "overall_score": certification.get_overall_score(),
            "requirements_completion": certification.get_requirements_completion(),
            "review_count": len(certification.reviews)
        }
    
    def _update_certification_status(self, certification: Certification) -> None:
        """Update certification status based on reviews."""
        if not certification.reviews:
            return
        
        # Check if all reviews are completed
        all_completed = all(review.status == ReviewStatus.COMPLETED for review in certification.reviews)
        
        if all_completed and certification.status == CertificationStatus.IN_REVIEW:
            # Check if ready for approval
            completion = certification.get_requirements_completion()
            if completion["mandatory_completion"]:
                certification.status = CertificationStatus.PENDING  # Ready for approval
            else:
                certification.status = CertificationStatus.REJECTED
    
    def _generate_certificate_number(self) -> str:
        """Generate a unique certificate number."""
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        random_suffix = str(uuid.uuid4())[:8].upper()
        return f"CERT-{timestamp}-{random_suffix}"
    
    def _initialize_default_requirements(self) -> None:
        """Initialize default requirements templates."""
        
        # Partner certification requirements
        partner_basic_requirements = [
            CertificationRequirement(
                name="Business Registration",
                description="Valid business registration and legal entity",
                category="legal",
                is_mandatory=True
            ),
            CertificationRequirement(
                name="Contact Information",
                description="Valid contact information and address",
                category="business",
                is_mandatory=True
            ),
            CertificationRequirement(
                name="Terms of Service",
                description="Acceptance of XReason terms of service",
                category="legal",
                is_mandatory=True
            )
        ]
        
        partner_standard_requirements = partner_basic_requirements + [
            CertificationRequirement(
                name="Technical Capability",
                description="Demonstrated technical capability",
                category="technical",
                is_mandatory=True
            ),
            CertificationRequirement(
                name="Support Infrastructure",
                description="Customer support infrastructure",
                category="business",
                is_mandatory=False
            )
        ]
        
        # Plugin certification requirements
        plugin_basic_requirements = [
            CertificationRequirement(
                name="Code Quality",
                description="Code quality and best practices",
                category="technical",
                is_mandatory=True
            ),
            CertificationRequirement(
                name="Security Review",
                description="Security review and vulnerability assessment",
                category="security",
                is_mandatory=True
            ),
            CertificationRequirement(
                name="Documentation",
                description="Comprehensive documentation",
                category="technical",
                is_mandatory=True
            )
        ]
        
        # Add templates
        self.add_requirements_template(CertificationType.PARTNER, CertificationLevel.BASIC, partner_basic_requirements)
        self.add_requirements_template(CertificationType.PARTNER, CertificationLevel.STANDARD, partner_standard_requirements)
        self.add_requirements_template(CertificationType.PLUGIN, CertificationLevel.BASIC, plugin_basic_requirements)


# Global certification manager instance
certification_manager = CertificationManager()
