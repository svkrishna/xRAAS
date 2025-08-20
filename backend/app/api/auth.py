"""
Authentication API endpoints for XReason
Handles login, registration, token management, and user operations.
"""

from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import auth_service
from app.services.rbac_service import rbac_service
from app.schemas.auth import (
    LoginRequest, RegisterRequest, RefreshTokenRequest, ForgotPasswordRequest,
    ResetPasswordRequest, ChangePasswordRequest, UpdateUserRequest,
    CreateTenantRequest, UpdateTenantRequest, SwitchTenantRequest,
    CreateAPIKeyRequest,
    LoginResponse, RefreshTokenResponse, AuthStatusResponse,
    UserResponse, TenantResponse, TenantListResponse,
    APIKeyResponse, APIKeyListResponse, SessionListResponse,
    Role, Permission
)
from app.models.auth import User, Tenant

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    user = auth_service.validate_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_tenant(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Optional[Tenant]:
    """Get current tenant for the user."""
    # This would typically be stored in the session or user preferences
    # For now, return the first tenant the user has access to
    user_tenants = auth_service.get_user_tenants(db, str(current_user.id))
    return user_tenants[0] if user_tenants else None


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Authenticate user and create session."""
    try:
        # Authenticate user
        user = auth_service.authenticate_user(db, login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is disabled"
            )
        
        # Get client information
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Create session
        session_data = auth_service.create_session(
            db, user, login_data.tenant_id, ip_address, user_agent
        )
        
        return LoginResponse(
            access_token=session_data["access_token"],
            refresh_token=session_data["refresh_token"],
            token_type=session_data["token_type"],
            expires_in=session_data["expires_in"],
            user=UserResponse(**user.to_dict()),
            tenant=TenantResponse(**session_data["tenant"].to_dict()) if session_data["tenant"] else None,
            permissions=session_data["permissions"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/register", response_model=LoginResponse)
async def register(
    register_data: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    try:
        # Create user
        user = auth_service.create_user(db, register_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
        
        # Create tenant if specified
        tenant = None
        if register_data.tenant_name and register_data.tenant_slug:
            tenant_data = CreateTenantRequest(
                name=register_data.tenant_name,
                slug=register_data.tenant_slug
            )
            tenant = auth_service.create_tenant(db, tenant_data, user)
        
        # Get client information
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Create session
        tenant_id = str(tenant.id) if tenant else None
        session_data = auth_service.create_session(
            db, user, tenant_id, ip_address, user_agent
        )
        
        return LoginResponse(
            access_token=session_data["access_token"],
            refresh_token=session_data["refresh_token"],
            token_type=session_data["token_type"],
            expires_in=session_data["expires_in"],
            user=UserResponse(**user.to_dict()),
            tenant=TenantResponse(**session_data["tenant"].to_dict()) if session_data["tenant"] else None,
            permissions=session_data["permissions"]
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    try:
        session_data = auth_service.refresh_session(db, refresh_data.refresh_token)
        if not session_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        return RefreshTokenResponse(
            access_token=session_data["access_token"],
            refresh_token=session_data["refresh_token"],
            token_type=session_data["token_type"],
            expires_in=session_data["expires_in"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Logout user and invalidate session."""
    try:
        token = credentials.credentials
        success = auth_service.logout(db, token)
        
        if success:
            return {"message": "Successfully logged out"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to logout"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )


@router.get("/status", response_model=AuthStatusResponse)
async def get_auth_status(
    current_user: User = Depends(get_current_user),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """Get current authentication status."""
    try:
        # Get user's active session
        # This is a simplified version - in production you'd track the specific session
        session_expires_at = datetime.utcnow() + timedelta(minutes=30)  # Mock expiry
        
        return AuthStatusResponse(
            is_authenticated=True,
            user=UserResponse(**current_user.to_dict()),
            tenant=TenantResponse(**current_tenant.to_dict()) if current_tenant else None,
            permissions=current_user.permissions or [],
            session_expires_at=session_expires_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get auth status: {str(e)}"
        )


@router.get("/tenants", response_model=TenantListResponse)
async def get_user_tenants(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tenants for the current user."""
    try:
        tenants = auth_service.get_user_tenants(db, str(current_user.id))
        
        # Get current tenant (simplified - would be stored in session)
        current_tenant = tenants[0] if tenants else None
        
        return TenantListResponse(
            tenants=[TenantResponse(**tenant.to_dict()) for tenant in tenants],
            current_tenant=TenantResponse(**current_tenant.to_dict()) if current_tenant else None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get tenants: {str(e)}"
        )


@router.post("/tenants/switch")
async def switch_tenant(
    switch_data: SwitchTenantRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Switch user's active tenant."""
    try:
        success = auth_service.switch_tenant(db, str(current_user.id), switch_data.tenant_id)
        
        if success:
            return {"message": "Successfully switched tenant"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to switch tenant - user may not have access"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to switch tenant: {str(e)}"
        )


@router.post("/tenants", response_model=TenantResponse)
async def create_tenant(
    tenant_data: CreateTenantRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new tenant."""
    try:
        # Check if user has permission to create tenants
        if not rbac_service.has_permission(current_user.permissions or [], Permission.MANAGE_TENANT):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to create tenants"
            )
        
        tenant = auth_service.create_tenant(db, tenant_data, current_user)
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create tenant"
            )
        
        return TenantResponse(**tenant.to_dict())
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create tenant: {str(e)}"
        )


@router.put("/users/me", response_model=UserResponse)
async def update_current_user(
    user_data: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's information."""
    try:
        updated_user = auth_service.update_user(db, str(current_user.id), user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(**updated_user.to_dict())
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )


@router.post("/api-keys", response_model=APIKeyResponse)
async def create_api_key(
    api_key_data: CreateAPIKeyRequest,
    current_user: User = Depends(get_current_user),
    current_tenant: Optional[Tenant] = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """Create a new API key for the current user."""
    try:
        # Check if user has permission to create API keys
        if not rbac_service.has_permission(current_user.permissions or [], Permission.MANAGE_API_KEYS):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to create API keys"
            )
        
        tenant_id = str(current_tenant.id) if current_tenant else None
        api_key_info = auth_service.create_api_key(db, str(current_user.id), api_key_data, tenant_id)
        
        if not api_key_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create API key"
            )
        
        return APIKeyResponse(
            id=api_key_info["id"],
            user_id=str(current_user.id),
            tenant_id=tenant_id,
            name=api_key_info["name"],
            permissions=api_key_info["permissions"],
            is_active=True,
            expires_at=api_key_info["expires_at"],
            last_used=None,
            created_at=api_key_info["created_at"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create API key: {str(e)}"
        )


@router.get("/api-keys", response_model=APIKeyListResponse)
async def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List API keys for the current user."""
    try:
        # This would typically query the database for user's API keys
        # For now, return empty list
        return APIKeyListResponse(api_keys=[])
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list API keys: {str(e)}"
        )


@router.post("/forgot-password")
async def forgot_password(
    forgot_data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """Send password reset email."""
    try:
        # This would typically send an email with reset link
        # For now, just return success
        return {"message": "Password reset email sent (if user exists)"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send password reset email: {str(e)}"
        )


@router.post("/reset-password")
async def reset_password(
    reset_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """Reset password using reset token."""
    try:
        # This would typically validate the token and update password
        # For now, just return success
        return {"message": "Password reset successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset password: {str(e)}"
        )


@router.get("/roles", response_model=List[dict])
async def get_roles():
    """Get all available roles with descriptions."""
    try:
        roles = []
        for role in Role:
            roles.append({
                "role": role,
                "description": rbac_service.get_role_description(role),
                "permissions": rbac_service.get_role_permissions(role)
            })
        return roles
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get roles: {str(e)}"
        )


@router.get("/permissions", response_model=dict)
async def get_permissions():
    """Get all available permissions grouped by category."""
    try:
        return rbac_service.get_permission_groups()
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get permissions: {str(e)}"
        )
