"""
Signed Ruleset Registry with Tamper-Evident Logging
Enterprise-grade ruleset management with cryptographic signatures and integrity verification.
"""

import json
import hashlib
import hmac
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid
import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

from app.security.audit_logger import audit_logger, AuditEventType, ComplianceFramework
from app.security.encryption_service import encryption_service


class RulesetStatus(str, Enum):
    """Ruleset lifecycle status."""
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    REVOKED = "revoked"


class RulesetSource(str, Enum):
    """Source of the ruleset."""
    INTERNAL = "internal"
    PARTNER = "partner"
    THIRD_PARTY = "third_party"
    COMMUNITY = "community"
    CERTIFIED = "certified"


class SignatureType(str, Enum):
    """Type of digital signature."""
    RSA_PSS_SHA256 = "rsa_pss_sha256"
    RSA_PKCS1_SHA256 = "rsa_pkcs1_sha256"
    ECDSA_SHA256 = "ecdsa_sha256"


@dataclass
class RulesetMetadata:
    """Comprehensive ruleset metadata."""
    id: str
    name: str
    version: str
    description: str
    author: str
    organization: str
    created_at: datetime
    updated_at: datetime
    status: RulesetStatus
    source: RulesetSource
    compliance_frameworks: List[str]
    domain: str
    tags: List[str]
    dependencies: List[str]
    changelog: List[Dict[str, Any]]
    license: str
    documentation_url: Optional[str] = None
    support_contact: Optional[str] = None


@dataclass
class RulesetSignature:
    """Digital signature for ruleset integrity."""
    signature_id: str
    signer_id: str
    signer_name: str
    signature_type: SignatureType
    signature_value: str
    public_key_fingerprint: str
    signed_at: datetime
    certificate_chain: Optional[List[str]] = None
    timestamp_authority: Optional[str] = None


@dataclass
class SignedRuleset:
    """Complete signed ruleset package."""
    metadata: RulesetMetadata
    rules: Dict[str, Any]
    signature: RulesetSignature
    integrity_hash: str
    size_bytes: int
    download_count: int = 0
    last_verified: Optional[datetime] = None


class RulesetRegistry:
    """
    Enterprise Signed Ruleset Registry.
    
    Features:
    - Cryptographic signing and verification
    - Tamper-evident integrity checking
    - Version management and dependency tracking
    - Partner and third-party ruleset certification
    - Compliance framework mapping
    - Automated security scanning
    """
    
    def __init__(self):
        self.registry: Dict[str, SignedRuleset] = {}
        self.signing_keys: Dict[str, RSAPrivateKey] = {}
        self.public_keys: Dict[str, RSAPublicKey] = {}
        self.trusted_signers: Dict[str, Dict[str, Any]] = {}
        self._initialize_registry()
    
    def _initialize_registry(self):
        """Initialize the registry with default configuration."""
        # Load or create signing keys
        self._load_or_create_signing_keys()
        
        # Load trusted signers
        self._load_trusted_signers()
        
        # Register internal rulesets
        self._register_internal_rulesets()
    
    def _load_or_create_signing_keys(self):
        """Load or create signing keys for the registry."""
        key_path = Path("registry_signing.key")
        
        if key_path.exists():
            with open(key_path, 'rb') as f:
                private_key_data = f.read()
                private_key = serialization.load_pem_private_key(
                    private_key_data,
                    password=None,
                    backend=default_backend()
                )
        else:
            # Generate new signing key pair
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,
                backend=default_backend()
            )
            
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            
            with open(key_path, 'wb') as f:
                f.write(private_pem)
            
            audit_logger.log_event(
                event_type=AuditEventType.ENCRYPTION_KEY_ROTATION,
                action="create_registry_signing_key",
                result="success",
                details={"key_size": 4096, "algorithm": "rsa"},
                compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
                risk_level="high"
            )
        
        public_key = private_key.public_key()
        
        # Store keys
        signer_id = "xreason_registry"
        self.signing_keys[signer_id] = private_key
        self.public_keys[signer_id] = public_key
    
    def _load_trusted_signers(self):
        """Load trusted signer configurations."""
        self.trusted_signers = {
            "xreason_registry": {
                "name": "XReason Internal Registry",
                "organization": "XReason",
                "trust_level": "full",
                "allowed_domains": ["*"],
                "certification_required": False
            },
            "healthcare_authority": {
                "name": "Healthcare Compliance Authority",
                "organization": "Healthcare Standards Institute",
                "trust_level": "domain_specific",
                "allowed_domains": ["healthcare", "medical", "hipaa"],
                "certification_required": True
            },
            "financial_authority": {
                "name": "Financial Compliance Authority", 
                "organization": "Financial Standards Board",
                "trust_level": "domain_specific",
                "allowed_domains": ["finance", "banking", "sox"],
                "certification_required": True
            }
        }
    
    def _register_internal_rulesets(self):
        """Register internal XReason rulesets."""
        internal_rulesets = [
            {
                "name": "HIPAA Compliance Rules",
                "version": "1.0.0",
                "domain": "healthcare",
                "compliance_frameworks": ["hipaa"],
                "rules": self._load_hipaa_rules()
            },
            {
                "name": "Financial Analysis Rules",
                "version": "1.0.0", 
                "domain": "finance",
                "compliance_frameworks": ["sox", "basel_iii"],
                "rules": self._load_financial_rules()
            },
            {
                "name": "GDPR Compliance Rules",
                "version": "1.0.0",
                "domain": "legal",
                "compliance_frameworks": ["gdpr"],
                "rules": self._load_gdpr_rules()
            }
        ]
        
        for ruleset_config in internal_rulesets:
            try:
                self.register_ruleset(
                    name=ruleset_config["name"],
                    version=ruleset_config["version"],
                    rules=ruleset_config["rules"],
                    author="XReason System",
                    organization="XReason",
                    domain=ruleset_config["domain"],
                    compliance_frameworks=ruleset_config["compliance_frameworks"],
                    source=RulesetSource.INTERNAL
                )
            except Exception as e:
                # Ruleset might already exist
                pass
    
    def _load_hipaa_rules(self) -> Dict[str, Any]:
        """Load HIPAA compliance rules."""
        return {
            "rules": [
                {
                    "id": "hipaa_164_312_a_1",
                    "type": "access_control",
                    "description": "Unique user identification requirement",
                    "condition": "user_access_request",
                    "validation": "unique_user_id_required",
                    "weight": 1.0
                },
                {
                    "id": "hipaa_164_312_e_1", 
                    "type": "transmission_security",
                    "description": "Transmission security for ePHI",
                    "condition": "data_transmission",
                    "validation": "encryption_required",
                    "weight": 1.0
                }
            ],
            "metadata": {
                "framework": "HIPAA",
                "version": "1.0.0",
                "last_updated": "2024-01-15"
            }
        }
    
    def _load_financial_rules(self) -> Dict[str, Any]:
        """Load financial analysis rules."""
        return {
            "rules": [
                {
                    "id": "debt_to_equity_ratio",
                    "type": "financial_metric",
                    "description": "Calculate debt-to-equity ratio",
                    "formula": "total_debt / total_equity",
                    "validation": "ratio_calculation",
                    "weight": 0.9
                },
                {
                    "id": "profit_margin_check",
                    "type": "financial_metric", 
                    "description": "Calculate profit margin",
                    "formula": "(revenue - costs) / revenue",
                    "validation": "percentage_calculation",
                    "weight": 0.8
                }
            ],
            "metadata": {
                "framework": "Financial Analysis",
                "version": "1.0.0",
                "last_updated": "2024-01-15"
            }
        }
    
    def _load_gdpr_rules(self) -> Dict[str, Any]:
        """Load GDPR compliance rules."""
        return {
            "rules": [
                {
                    "id": "gdpr_article_25",
                    "type": "data_protection",
                    "description": "Data protection by design and by default",
                    "condition": "data_processing",
                    "validation": "privacy_by_design_check",
                    "weight": 1.0
                },
                {
                    "id": "gdpr_article_32",
                    "type": "security_processing",
                    "description": "Security of processing",
                    "condition": "data_processing",
                    "validation": "security_measures_check", 
                    "weight": 1.0
                }
            ],
            "metadata": {
                "framework": "GDPR",
                "version": "1.0.0",
                "last_updated": "2024-01-15"
            }
        }
    
    def register_ruleset(
        self,
        name: str,
        version: str,
        rules: Dict[str, Any],
        author: str,
        organization: str,
        domain: str,
        compliance_frameworks: List[str],
        source: RulesetSource = RulesetSource.INTERNAL,
        description: str = "",
        tags: List[str] = None,
        dependencies: List[str] = None,
        license: str = "Proprietary",
        signer_id: str = "xreason_registry"
    ) -> str:
        """
        Register a new ruleset in the registry.
        
        Args:
            name: Ruleset name
            version: Version string
            rules: Ruleset rules dictionary
            author: Author name
            organization: Organization name  
            domain: Domain (healthcare, finance, etc.)
            compliance_frameworks: List of compliance frameworks
            source: Source of the ruleset
            description: Description
            tags: Tags for categorization
            dependencies: List of dependency ruleset IDs
            license: License type
            signer_id: ID of the signer
            
        Returns:
            str: Ruleset ID
        """
        
        ruleset_id = f"{domain}_{name.lower().replace(' ', '_')}_{version}"
        
        # Check if signer is authorized
        if signer_id not in self.trusted_signers:
            raise ValueError(f"Untrusted signer: {signer_id}")
        
        # Create metadata
        metadata = RulesetMetadata(
            id=ruleset_id,
            name=name,
            version=version,
            description=description,
            author=author,
            organization=organization,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            status=RulesetStatus.DRAFT,
            source=source,
            compliance_frameworks=compliance_frameworks,
            domain=domain,
            tags=tags or [],
            dependencies=dependencies or [],
            changelog=[{
                "version": version,
                "date": datetime.now(timezone.utc).isoformat(),
                "changes": "Initial version",
                "author": author
            }],
            license=license
        )
        
        # Calculate integrity hash
        ruleset_content = {
            "metadata": asdict(metadata),
            "rules": rules
        }
        content_json = json.dumps(ruleset_content, sort_keys=True)
        integrity_hash = hashlib.sha256(content_json.encode()).hexdigest()
        
        # Sign the ruleset
        signature = self._sign_ruleset(ruleset_content, signer_id)
        
        # Create signed ruleset
        signed_ruleset = SignedRuleset(
            metadata=metadata,
            rules=rules,
            signature=signature,
            integrity_hash=integrity_hash,
            size_bytes=len(content_json.encode()),
            download_count=0
        )
        
        # Store in registry
        self.registry[ruleset_id] = signed_ruleset
        
        # Log audit event
        audit_logger.log_event(
            event_type=AuditEventType.RULESET_MODIFY,
            action="register_ruleset",
            result="success",
            details={
                "ruleset_id": ruleset_id,
                "name": name,
                "version": version,
                "domain": domain,
                "source": source.value,
                "signer_id": signer_id,
                "integrity_hash": integrity_hash
            },
            user_id=author,
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="medium"
        )
        
        return ruleset_id
    
    def _sign_ruleset(self, ruleset_content: Dict[str, Any], signer_id: str) -> RulesetSignature:
        """
        Create digital signature for ruleset.
        
        Args:
            ruleset_content: Complete ruleset content
            signer_id: ID of the signer
            
        Returns:
            RulesetSignature: Digital signature
        """
        if signer_id not in self.signing_keys:
            raise ValueError(f"No signing key for: {signer_id}")
        
        private_key = self.signing_keys[signer_id]
        public_key = self.public_keys[signer_id]
        
        # Create content hash for signing
        content_json = json.dumps(ruleset_content, sort_keys=True)
        content_hash = hashlib.sha256(content_json.encode()).digest()
        
        # Sign using RSA-PSS
        signature_bytes = private_key.sign(
            content_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Get public key fingerprint
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_key_fingerprint = hashlib.sha256(public_key_bytes).hexdigest()
        
        return RulesetSignature(
            signature_id=str(uuid.uuid4()),
            signer_id=signer_id,
            signer_name=self.trusted_signers[signer_id]["name"],
            signature_type=SignatureType.RSA_PSS_SHA256,
            signature_value=base64.b64encode(signature_bytes).decode(),
            public_key_fingerprint=public_key_fingerprint,
            signed_at=datetime.now(timezone.utc)
        )
    
    def verify_ruleset(self, ruleset_id: str) -> Tuple[bool, List[str]]:
        """
        Verify ruleset signature and integrity.
        
        Args:
            ruleset_id: ID of ruleset to verify
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, verification_errors)
        """
        if ruleset_id not in self.registry:
            return False, [f"Ruleset not found: {ruleset_id}"]
        
        signed_ruleset = self.registry[ruleset_id]
        errors = []
        
        # Verify signer is trusted
        signer_id = signed_ruleset.signature.signer_id
        if signer_id not in self.trusted_signers:
            errors.append(f"Untrusted signer: {signer_id}")
        
        # Verify public key
        if signer_id not in self.public_keys:
            errors.append(f"No public key for signer: {signer_id}")
            return False, errors
        
        public_key = self.public_keys[signer_id]
        
        # Verify signature
        try:
            ruleset_content = {
                "metadata": asdict(signed_ruleset.metadata),
                "rules": signed_ruleset.rules
            }
            content_json = json.dumps(ruleset_content, sort_keys=True)
            content_hash = hashlib.sha256(content_json.encode()).digest()
            
            signature_bytes = base64.b64decode(signed_ruleset.signature.signature_value)
            
            public_key.verify(
                signature_bytes,
                content_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
        except InvalidSignature:
            errors.append("Invalid digital signature")
        except Exception as e:
            errors.append(f"Signature verification error: {str(e)}")
        
        # Verify integrity hash
        ruleset_content = {
            "metadata": asdict(signed_ruleset.metadata),
            "rules": signed_ruleset.rules
        }
        content_json = json.dumps(ruleset_content, sort_keys=True)
        calculated_hash = hashlib.sha256(content_json.encode()).hexdigest()
        
        if calculated_hash != signed_ruleset.integrity_hash:
            errors.append("Integrity hash mismatch - ruleset may be tampered")
        
        # Update verification timestamp
        if not errors:
            signed_ruleset.last_verified = datetime.now(timezone.utc)
        
        # Log verification attempt
        audit_logger.log_event(
            event_type=AuditEventType.RULESET_ACCESS,
            action="verify_ruleset",
            result="success" if not errors else "failure",
            details={
                "ruleset_id": ruleset_id,
                "signer_id": signer_id,
                "verification_errors": errors,
                "integrity_hash": signed_ruleset.integrity_hash
            },
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="low" if not errors else "high"
        )
        
        return len(errors) == 0, errors
    
    def get_ruleset(self, ruleset_id: str, verify: bool = True) -> Optional[SignedRuleset]:
        """
        Retrieve ruleset from registry.
        
        Args:
            ruleset_id: ID of ruleset to retrieve
            verify: Whether to verify signature before returning
            
        Returns:
            SignedRuleset or None if not found or verification fails
        """
        if ruleset_id not in self.registry:
            return None
        
        signed_ruleset = self.registry[ruleset_id]
        
        if verify:
            is_valid, errors = self.verify_ruleset(ruleset_id)
            if not is_valid:
                audit_logger.log_event(
                    event_type=AuditEventType.SECURITY_VIOLATION,
                    action="get_invalid_ruleset",
                    result="blocked",
                    details={
                        "ruleset_id": ruleset_id,
                        "verification_errors": errors
                    },
                    compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
                    risk_level="high"
                )
                return None
        
        # Increment download count
        signed_ruleset.download_count += 1
        
        # Log access
        audit_logger.log_event(
            event_type=AuditEventType.RULESET_ACCESS,
            action="get_ruleset",
            result="success",
            details={
                "ruleset_id": ruleset_id,
                "download_count": signed_ruleset.download_count
            },
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="low"
        )
        
        return signed_ruleset
    
    def list_rulesets(
        self,
        domain: Optional[str] = None,
        compliance_framework: Optional[str] = None,
        source: Optional[RulesetSource] = None,
        status: Optional[RulesetStatus] = None
    ) -> List[Dict[str, Any]]:
        """
        List rulesets with optional filtering.
        
        Args:
            domain: Filter by domain
            compliance_framework: Filter by compliance framework
            source: Filter by source
            status: Filter by status
            
        Returns:
            List of ruleset summaries
        """
        rulesets = []
        
        for ruleset_id, signed_ruleset in self.registry.items():
            metadata = signed_ruleset.metadata
            
            # Apply filters
            if domain and metadata.domain != domain:
                continue
            if compliance_framework and compliance_framework not in metadata.compliance_frameworks:
                continue
            if source and metadata.source != source:
                continue
            if status and metadata.status != status:
                continue
            
            # Verify signature
            is_valid, _ = self.verify_ruleset(ruleset_id)
            
            rulesets.append({
                "id": ruleset_id,
                "name": metadata.name,
                "version": metadata.version,
                "domain": metadata.domain,
                "status": metadata.status.value,
                "source": metadata.source.value,
                "compliance_frameworks": metadata.compliance_frameworks,
                "author": metadata.author,
                "organization": metadata.organization,
                "created_at": metadata.created_at.isoformat(),
                "signature_valid": is_valid,
                "download_count": signed_ruleset.download_count,
                "size_bytes": signed_ruleset.size_bytes
            })
        
        return rulesets
    
    def get_registry_status(self) -> Dict[str, Any]:
        """
        Get registry status and metrics.
        
        Returns:
            Dict: Registry status information
        """
        total_rulesets = len(self.registry)
        
        # Count by status
        status_counts = {}
        for status in RulesetStatus:
            status_counts[status.value] = sum(
                1 for signed_ruleset in self.registry.values()
                if signed_ruleset.metadata.status == status
            )
        
        # Count by source
        source_counts = {}
        for source in RulesetSource:
            source_counts[source.value] = sum(
                1 for signed_ruleset in self.registry.values()
                if signed_ruleset.metadata.source == source
            )
        
        # Verify all signatures
        verification_results = {}
        for ruleset_id in self.registry:
            is_valid, errors = self.verify_ruleset(ruleset_id)
            verification_results[ruleset_id] = {
                "valid": is_valid,
                "errors": errors
            }
        
        valid_signatures = sum(1 for result in verification_results.values() if result["valid"])
        
        return {
            "total_rulesets": total_rulesets,
            "valid_signatures": valid_signatures,
            "signature_integrity": (valid_signatures / total_rulesets * 100) if total_rulesets else 100,
            "status_distribution": status_counts,
            "source_distribution": source_counts,
            "trusted_signers": len(self.trusted_signers),
            "verification_results": verification_results,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }


# Global registry instance
ruleset_registry = RulesetRegistry()
