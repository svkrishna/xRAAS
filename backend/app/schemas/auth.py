"""
Authentication Schemas for XReason
Pydantic models for authentication requests and responses.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum


class Role(str, Enum):
    """User roles in the system."""
    OWNER = "owner"
    ADMIN = "admin"
    ANALYST = "analyst"
    DEVELOPER = "developer"
    VIEWER = "viewer"
    PARTNER = "partner"


class Permission(str, Enum):
    """System permissions."""
    # User Management
    MANAGE_USERS = "manage_users"
    VIEW_USERS = "view_users"
    
    # Tenant Management
    MANAGE_TENANT = "manage_tenant"
    SWITCH_TENANTS = "switch_tenants"
    
    # Billing & Subscriptions
    MANAGE_BILLING = "manage_billing"
    VIEW_BILLING = "view_billing"
    
    # Analytics & Usage
    VIEW_ANALYTICS = "view_analytics"
    EXPORT_ANALYTICS = "export_analytics"
    
    # Compliance
    MANAGE_COMPLIANCE = "manage_compliance"
    VIEW_COMPLIANCE = "view_compliance"
    UPLOAD_EVIDENCE = "upload_evidence"
    
    # Rulesets
    MANAGE_RULESETS = "manage_rulesets"
    VIEW_RULESETS = "view_rulesets"
    PROMOTE_RULESETS = "promote_rulesets"
    
    # Audit
    VIEW_AUDIT = "view_audit"
    EXPORT_AUDIT = "export_audit"
    
    # Partners
    MANAGE_PARTNERS = "manage_partners"
    VIEW_PARTNERS = "view_partners"
    SUBMIT_RULESETS = "submit_rulesets"
    
    # Admin
    MANAGE_API_KEYS = "manage_api_keys"
    MANAGE_WEBHOOKS = "manage_webhooks"
    MANAGE_FEATURE_FLAGS = "manage_feature_flags"


class SubscriptionTier(str, Enum):
    """Subscription tiers."""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    MISSION_CRITICAL = "mission_critical"


class TenantStatus(str, Enum):
    """Tenant status."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


# Request Models
class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    tenant_id: Optional[str] = Field(None, description="Optional tenant ID for multi-tenancy")


class RegisterRequest(BaseModel):
    """User registration request model."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    name: str = Field(..., min_length=2, max_length=255, description="User full name")
    tenant_name: Optional[str] = Field(None, description="Organization name for new tenant")
    tenant_slug: Optional[str] = Field(None, description="Organization slug for new tenant")


class RefreshTokenRequest(BaseModel):
    """Token refresh request model."""
    refresh_token: str = Field(..., description="Refresh token")


class ForgotPasswordRequest(BaseModel):
    """Forgot password request model."""
    email: EmailStr = Field(..., description="User email address")


class ResetPasswordRequest(BaseModel):
    """Reset password request model."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password")


class ChangePasswordRequest(BaseModel):
    """Change password request model."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")


class UpdateUserRequest(BaseModel):
    """Update user request model."""
    name: Optional[str] = Field(None, min_length=2, max_length=255, description="User full name")
    avatar: Optional[str] = Field(None, description="Avatar URL")
    role: Optional[Role] = Field(None, description="User role")


class CreateTenantRequest(BaseModel):
    """Create tenant request model."""
    name: str = Field(..., min_length=2, max_length=255, description="Tenant name")
    slug: str = Field(..., min_length=2, max_length=100, description="Tenant slug")
    domain: Optional[str] = Field(None, description="Tenant domain")
    subscription_tier: SubscriptionTier = Field(SubscriptionTier.STARTER, description="Subscription tier")


class UpdateTenantRequest(BaseModel):
    """Update tenant request model."""
    name: Optional[str] = Field(None, min_length=2, max_length=255, description="Tenant name")
    domain: Optional[str] = Field(None, description="Tenant domain")
    subscription_tier: Optional[SubscriptionTier] = Field(None, description="Subscription tier")
    status: Optional[TenantStatus] = Field(None, description="Tenant status")
    settings: Optional[Dict[str, Any]] = Field(None, description="Tenant settings")


class SwitchTenantRequest(BaseModel):
    """Switch tenant request model."""
    tenant_id: str = Field(..., description="Tenant ID to switch to")


class CreateAPIKeyRequest(BaseModel):
    """Create API key request model."""
    name: str = Field(..., min_length=2, max_length=255, description="API key name")
    permissions: List[Permission] = Field(default=[], description="API key permissions")
    expires_at: Optional[datetime] = Field(None, description="API key expiration date")


# Response Models
class UserResponse(BaseModel):
    """User response model."""
    id: str
    email: str
    name: str
    avatar: Optional[str]
    role: Role
    permissions: List[Permission]
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TenantResponse(BaseModel):
    """Tenant response model."""
    id: str
    name: str
    slug: str
    domain: Optional[str]
    subscription_tier: SubscriptionTier
    status: TenantStatus
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TenantMembershipResponse(BaseModel):
    """Tenant membership response model."""
    id: str
    user_id: str
    tenant_id: str
    role: str
    permissions: List[Permission]
    is_active: bool
    joined_at: datetime

    class Config:
        from_attributes = True


class SessionResponse(BaseModel):
    """Session response model."""
    id: str
    user_id: str
    tenant_id: Optional[str]
    expires_at: datetime
    is_active: bool
    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: datetime
    last_activity: datetime

    class Config:
        from_attributes = True


class APIKeyResponse(BaseModel):
    """API key response model."""
    id: str
    user_id: str
    tenant_id: Optional[str]
    name: str
    permissions: List[Permission]
    is_active: bool
    expires_at: Optional[datetime]
    last_used: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Login response model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
    tenant: Optional[TenantResponse]
    permissions: List[Permission]


class RefreshTokenResponse(BaseModel):
    """Token refresh response model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthStatusResponse(BaseModel):
    """Authentication status response model."""
    is_authenticated: bool
    user: Optional[UserResponse]
    tenant: Optional[TenantResponse]
    permissions: List[Permission]
    session_expires_at: Optional[datetime]


class TenantListResponse(BaseModel):
    """Tenant list response model."""
    tenants: List[TenantResponse]
    current_tenant: Optional[TenantResponse]


class APIKeyListResponse(BaseModel):
    """API key list response model."""
    api_keys: List[APIKeyResponse]


class SessionListResponse(BaseModel):
    """Session list response model."""
    sessions: List[SessionResponse]


# Error Models
class AuthError(BaseModel):
    """Authentication error model."""
    error: str
    error_description: Optional[str] = None
    error_code: Optional[str] = None


class ValidationError(BaseModel):
    """Validation error model."""
    field: str
    message: str
    code: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    message: str
    details: Optional[List[ValidationError]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None
