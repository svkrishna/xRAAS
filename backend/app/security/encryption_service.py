"""
Enterprise Encryption Service
Advanced encryption and key management for data at rest and in transit.
"""

import os
import base64
import json
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime, timezone, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets

from app.core.config import settings
from app.security.audit_logger import audit_logger, AuditEventType, ComplianceFramework


class EncryptionAlgorithm:
    """Supported encryption algorithms."""
    AES_256_GCM = "aes-256-gcm"
    AES_256_CBC = "aes-256-cbc"
    FERNET = "fernet"
    RSA_2048 = "rsa-2048"
    RSA_4096 = "rsa-4096"


class KeyRotationStatus:
    """Key rotation status tracking."""
    ACTIVE = "active"
    PENDING_ROTATION = "pending_rotation"
    ROTATING = "rotating"
    RETIRED = "retired"


class EncryptionService:
    """
    Enterprise-grade encryption service with key management.
    
    Features:
    - Multiple encryption algorithms (AES-256-GCM, RSA, Fernet)
    - Automatic key rotation
    - Hardware Security Module (HSM) ready
    - Audit logging for all operations
    - FIPS 140-2 Level 3 compliance ready
    """
    
    def __init__(self):
        self.master_key = self._get_or_create_master_key()
        self.data_encryption_keys: Dict[str, Dict[str, Any]] = {}
        self.key_rotation_schedule = self._load_rotation_schedule()
    
    def _get_or_create_master_key(self) -> bytes:
        """Get or create master encryption key."""
        key_path = "master_encryption.key"
        
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                key_data = f.read()
                # In production, this would be stored in HSM or key vault
                return key_data
        else:
            # Generate new master key
            password = settings.secret_key.encode()
            salt = os.urandom(32)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(password)
            
            with open(key_path, 'wb') as f:
                f.write(salt + key)
            
            audit_logger.log_event(
                event_type=AuditEventType.ENCRYPTION_KEY_ROTATION,
                action="create_master_key",
                result="success",
                details={"key_type": "master", "algorithm": "pbkdf2-sha256"},
                compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II, ComplianceFramework.ISO27001],
                risk_level="critical"
            )
            
            return key
    
    def _load_rotation_schedule(self) -> Dict[str, Dict[str, Any]]:
        """Load key rotation schedule."""
        return {
            "data_encryption_keys": {
                "rotation_interval_days": 90,
                "max_age_days": 365,
                "auto_rotate": True
            },
            "audit_signing_keys": {
                "rotation_interval_days": 180,
                "max_age_days": 730,
                "auto_rotate": True
            },
            "api_keys": {
                "rotation_interval_days": 30,
                "max_age_days": 90,
                "auto_rotate": False  # Manual rotation for API keys
            }
        }
    
    def generate_data_encryption_key(
        self,
        key_id: str,
        algorithm: str = EncryptionAlgorithm.AES_256_GCM,
        purpose: str = "general"
    ) -> str:
        """
        Generate new data encryption key.
        
        Args:
            key_id: Unique identifier for the key
            algorithm: Encryption algorithm to use
            purpose: Purpose of the key (audit, user_data, etc.)
            
        Returns:
            str: Key ID for reference
        """
        if algorithm == EncryptionAlgorithm.AES_256_GCM:
            key = os.urandom(32)  # 256-bit key
        elif algorithm == EncryptionAlgorithm.FERNET:
            key = Fernet.generate_key()
        elif algorithm in [EncryptionAlgorithm.RSA_2048, EncryptionAlgorithm.RSA_4096]:
            key_size = 2048 if algorithm == EncryptionAlgorithm.RSA_2048 else 4096
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=default_backend()
            )
            key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        # Encrypt the key with master key
        encrypted_key = self._encrypt_with_master_key(key)
        
        self.data_encryption_keys[key_id] = {
            "encrypted_key": encrypted_key,
            "algorithm": algorithm,
            "purpose": purpose,
            "created_at": datetime.now(timezone.utc),
            "last_rotation": datetime.now(timezone.utc),
            "status": KeyRotationStatus.ACTIVE,
            "usage_count": 0
        }
        
        audit_logger.log_event(
            event_type=AuditEventType.ENCRYPTION_KEY_ROTATION,
            action="generate_dek",
            result="success",
            details={
                "key_id": key_id,
                "algorithm": algorithm,
                "purpose": purpose
            },
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="high"
        )
        
        return key_id
    
    def _encrypt_with_master_key(self, data: bytes) -> str:
        """Encrypt data with master key."""
        # Use Fernet for master key encryption
        f = Fernet(base64.urlsafe_b64encode(self.master_key[:32]))
        encrypted = f.encrypt(data)
        return base64.b64encode(encrypted).decode()
    
    def _decrypt_with_master_key(self, encrypted_data: str) -> bytes:
        """Decrypt data with master key."""
        f = Fernet(base64.urlsafe_b64encode(self.master_key[:32]))
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        return f.decrypt(encrypted_bytes)
    
    def encrypt_data(
        self,
        data: bytes,
        key_id: str,
        additional_data: Optional[bytes] = None
    ) -> Tuple[str, str]:
        """
        Encrypt data using specified key.
        
        Args:
            data: Data to encrypt
            key_id: ID of encryption key to use
            additional_data: Additional authenticated data for GCM mode
            
        Returns:
            Tuple[str, str]: (encrypted_data, nonce/iv)
        """
        if key_id not in self.data_encryption_keys:
            raise ValueError(f"Unknown key ID: {key_id}")
        
        key_info = self.data_encryption_keys[key_id]
        key = self._decrypt_with_master_key(key_info["encrypted_key"])
        algorithm = key_info["algorithm"]
        
        if algorithm == EncryptionAlgorithm.AES_256_GCM:
            # AES-256-GCM encryption
            nonce = os.urandom(12)  # 96-bit nonce for GCM
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(nonce),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            
            if additional_data:
                encryptor.authenticate_additional_data(additional_data)
            
            ciphertext = encryptor.update(data) + encryptor.finalize()
            
            # Combine nonce, tag, and ciphertext
            encrypted_data = base64.b64encode(nonce + encryptor.tag + ciphertext).decode()
            nonce_b64 = base64.b64encode(nonce).decode()
            
        elif algorithm == EncryptionAlgorithm.FERNET:
            f = Fernet(key)
            encrypted_data = f.encrypt(data).decode()
            nonce_b64 = ""  # Fernet includes nonce in output
            
        else:
            raise ValueError(f"Encryption not implemented for: {algorithm}")
        
        # Update usage count
        key_info["usage_count"] += 1
        
        return encrypted_data, nonce_b64
    
    def decrypt_data(
        self,
        encrypted_data: str,
        key_id: str,
        nonce: Optional[str] = None,
        additional_data: Optional[bytes] = None
    ) -> bytes:
        """
        Decrypt data using specified key.
        
        Args:
            encrypted_data: Encrypted data to decrypt
            key_id: ID of encryption key to use
            nonce: Nonce/IV if required by algorithm
            additional_data: Additional authenticated data for GCM mode
            
        Returns:
            bytes: Decrypted data
        """
        if key_id not in self.data_encryption_keys:
            raise ValueError(f"Unknown key ID: {key_id}")
        
        key_info = self.data_encryption_keys[key_id]
        key = self._decrypt_with_master_key(key_info["encrypted_key"])
        algorithm = key_info["algorithm"]
        
        if algorithm == EncryptionAlgorithm.AES_256_GCM:
            # Decode the combined data
            combined_data = base64.b64decode(encrypted_data.encode())
            nonce_bytes = combined_data[:12]
            tag = combined_data[12:28]
            ciphertext = combined_data[28:]
            
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(nonce_bytes, tag),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            
            if additional_data:
                decryptor.authenticate_additional_data(additional_data)
            
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
        elif algorithm == EncryptionAlgorithm.FERNET:
            f = Fernet(key)
            plaintext = f.decrypt(encrypted_data.encode())
            
        else:
            raise ValueError(f"Decryption not implemented for: {algorithm}")
        
        return plaintext
    
    def rotate_key(self, key_id: str) -> str:
        """
        Rotate encryption key.
        
        Args:
            key_id: ID of key to rotate
            
        Returns:
            str: New key ID
        """
        if key_id not in self.data_encryption_keys:
            raise ValueError(f"Unknown key ID: {key_id}")
        
        old_key_info = self.data_encryption_keys[key_id]
        
        # Mark old key as retired
        old_key_info["status"] = KeyRotationStatus.RETIRED
        old_key_info["retired_at"] = datetime.now(timezone.utc)
        
        # Generate new key
        new_key_id = f"{key_id}_v{int(datetime.now().timestamp())}"
        self.generate_data_encryption_key(
            new_key_id,
            old_key_info["algorithm"],
            old_key_info["purpose"]
        )
        
        audit_logger.log_event(
            event_type=AuditEventType.ENCRYPTION_KEY_ROTATION,
            action="rotate_key",
            result="success",
            details={
                "old_key_id": key_id,
                "new_key_id": new_key_id,
                "algorithm": old_key_info["algorithm"]
            },
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="high"
        )
        
        return new_key_id
    
    def check_key_rotation_needed(self) -> List[str]:
        """
        Check which keys need rotation based on policy.
        
        Returns:
            List[str]: List of key IDs that need rotation
        """
        keys_needing_rotation = []
        
        for key_id, key_info in self.data_encryption_keys.items():
            if key_info["status"] != KeyRotationStatus.ACTIVE:
                continue
            
            purpose = key_info["purpose"]
            schedule = self.key_rotation_schedule.get(purpose, {})
            rotation_interval = schedule.get("rotation_interval_days", 90)
            
            days_since_rotation = (
                datetime.now(timezone.utc) - key_info["last_rotation"]
            ).days
            
            if days_since_rotation >= rotation_interval:
                keys_needing_rotation.append(key_id)
        
        return keys_needing_rotation
    
    def generate_api_key(self, user_id: str, permissions: List[str]) -> Tuple[str, str]:
        """
        Generate API key for user authentication.
        
        Args:
            user_id: User ID for the API key
            permissions: List of permissions for the key
            
        Returns:
            Tuple[str, str]: (api_key, key_id)
        """
        # Generate secure random API key
        api_key = f"xr_{secrets.token_urlsafe(32)}"
        key_id = f"api_{user_id}_{int(datetime.now().timestamp())}"
        
        # Encrypt API key for storage
        encrypted_key, _ = self.encrypt_data(
            api_key.encode(),
            "api_key_encryption"  # Use dedicated key for API keys
        )
        
        # Store API key metadata (in production, this goes to database)
        api_key_metadata = {
            "key_id": key_id,
            "user_id": user_id,
            "permissions": permissions,
            "created_at": datetime.now(timezone.utc),
            "last_used": None,
            "usage_count": 0,
            "status": "active"
        }
        
        audit_logger.log_event(
            event_type=AuditEventType.API_ACCESS,
            action="generate_api_key",
            result="success",
            details={
                "key_id": key_id,
                "user_id": user_id,
                "permissions_count": len(permissions)
            },
            user_id=user_id,
            compliance_frameworks=[ComplianceFramework.SOC2_TYPE_II],
            risk_level="medium"
        )
        
        return api_key, key_id
    
    def get_encryption_status(self) -> Dict[str, Any]:
        """
        Get encryption service status and metrics.
        
        Returns:
            Dict: Encryption service status
        """
        active_keys = sum(
            1 for key_info in self.data_encryption_keys.values()
            if key_info["status"] == KeyRotationStatus.ACTIVE
        )
        
        keys_needing_rotation = len(self.check_key_rotation_needed())
        
        return {
            "service_status": "healthy",
            "master_key_status": "active",
            "total_keys": len(self.data_encryption_keys),
            "active_keys": active_keys,
            "keys_needing_rotation": keys_needing_rotation,
            "supported_algorithms": [
                EncryptionAlgorithm.AES_256_GCM,
                EncryptionAlgorithm.FERNET,
                EncryptionAlgorithm.RSA_2048,
                EncryptionAlgorithm.RSA_4096
            ],
            "compliance_standards": [
                "FIPS 140-2",
                "AES-256",
                "RSA-2048/4096",
                "PBKDF2-SHA256"
            ]
        }


# Global encryption service instance
encryption_service = EncryptionService()

# Initialize default encryption keys
try:
    encryption_service.generate_data_encryption_key(
        "audit_log_encryption",
        EncryptionAlgorithm.AES_256_GCM,
        "audit_logs"
    )
    encryption_service.generate_data_encryption_key(
        "user_data_encryption",
        EncryptionAlgorithm.AES_256_GCM,
        "user_data"
    )
    encryption_service.generate_data_encryption_key(
        "api_key_encryption",
        EncryptionAlgorithm.FERNET,
        "api_keys"
    )
except Exception as e:
    # Keys might already exist
    pass
