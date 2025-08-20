"""
Authentication Service for XReason
Handles user authentication, session management, and authorization.
"""

import logging
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session as DBSession
from sqlalchemy.exc import IntegrityError
import jwt

from app.models.auth import User, Tenant, TenantMembership, UserSession, APIKey, PasswordReset
from app.schemas.auth import (
    Role, Permission, SubscriptionTier, TenantStatus,
    LoginRequest, RegisterRequest, UpdateUserRequest,
    CreateTenantRequest, UpdateTenantRequest, CreateAPIKeyRequest
)
from app.core.config import settings
from app.services.rbac_service import RBACService

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service for user and session management."""
    
    def __init__(self):
        self.rbac_service = RBACService()
    
    def authenticate_user(self, db: DBSession, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password."""
        try:
            user = db.query(User).filter(User.email == email).first()
            if user and user.verify_password(password):
                return user
            return None
        except Exception as e:
            logger.error(f"Authentication error for {email}: {e}")
            return None
    
    def create_user(self, db: DBSession, user_data: RegisterRequest) -> Optional[User]:
        """Create a new user."""
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise ValueError("User with this email already exists")
            
            # Create user
            user = User(
                email=user_data.email,
                name=user_data.name,
                role=Role.VIEWER,
                permissions=self.rbac_service.get_role_permissions(Role.VIEWER)
            )
            user.password = user_data.password
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info(f"Created user: {user.email}")
            return user
            
        except IntegrityError:
            db.rollback()
            raise ValueError("User with this email already exists")
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {e}")
            raise
    
    def create_tenant(self, db: DBSession, tenant_data: CreateTenantRequest, owner_user: User) -> Optional[Tenant]:
        """Create a new tenant."""
        try:
            # Check if tenant slug already exists
            existing_tenant = db.query(Tenant).filter(Tenant.slug == tenant_data.slug).first()
            if existing_tenant:
                raise ValueError("Tenant with this slug already exists")
            
            # Create tenant
            tenant = Tenant(
                name=tenant_data.name,
                slug=tenant_data.slug,
                domain=tenant_data.domain,
                subscription_tier=tenant_data.subscription_tier,
                status=TenantStatus.ACTIVE
            )
            
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            
            # Create membership for owner
            membership = TenantMembership(
                user_id=owner_user.id,
                tenant_id=tenant.id,
                role=Role.OWNER,
                permissions=self.rbac_service.get_role_permissions(Role.OWNER)
            )
            
            db.add(membership)
            db.commit()
            
            logger.info(f"Created tenant: {tenant.name} with owner: {owner_user.email}")
            return tenant
            
        except IntegrityError:
            db.rollback()
            raise ValueError("Tenant with this slug already exists")
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating tenant: {e}")
            raise
    
    def create_session(self, db: DBSession, user: User, tenant_id: Optional[str] = None, 
                      ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Dict[str, Any]:
        """Create a new user session."""
        try:
            # Generate tokens
            access_token = user.generate_token()
            refresh_token = self._generate_refresh_token()
            
            # Hash tokens for storage
            token_hash = hashlib.sha256(access_token.encode()).hexdigest()
            refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
            
            # Create session
            session = UserSession(
                user_id=user.id,
                tenant_id=tenant_id,
                token_hash=token_hash,
                refresh_token_hash=refresh_token_hash,
                expires_at=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            db.add(session)
            db.commit()
            db.refresh(session)
            
            # Update user last login
            user.last_login = datetime.utcnow()
            db.commit()
            
            # Get tenant if specified
            tenant = None
            if tenant_id:
                tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                "user": user,
                "tenant": tenant,
                "permissions": user.permissions or []
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating session: {e}")
            raise
    
    def validate_token(self, db: DBSession, token: str) -> Optional[User]:
        """Validate JWT token and return user."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                return None
            
            user = db.query(User).filter(User.id == user_id).first()
            if not user or not user.is_active:
                return None
            
            return user
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.JWTError as e:
            logger.error(f"JWT validation error: {e}")
            return None
    
    def refresh_session(self, db: DBSession, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh user session with refresh token."""
        try:
            refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
            
            session = db.query(UserSession).filter(
                UserSession.refresh_token_hash == refresh_token_hash,
                UserSession.is_active == True
            ).first()
            
            if not session or session.is_expired():
                return None
            
            user = db.query(User).filter(User.id == session.user_id).first()
            if not user or not user.is_active:
                return None
            
            # Generate new tokens
            new_access_token = user.generate_token()
            new_refresh_token = self._generate_refresh_token()
            
            # Update session
            session.token_hash = hashlib.sha256(new_access_token.encode()).hexdigest()
            session.refresh_token_hash = hashlib.sha256(new_refresh_token.encode()).hexdigest()
            session.expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            session.last_activity = datetime.utcnow()
            
            db.commit()
            
            # Get tenant
            tenant = None
            if session.tenant_id:
                tenant = db.query(Tenant).filter(Tenant.id == session.tenant_id).first()
            
            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer",
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                "user": user,
                "tenant": tenant,
                "permissions": user.permissions or []
            }
            
        except Exception as e:
            logger.error(f"Error refreshing session: {e}")
            return None
    
    def logout(self, db: DBSession, token: str) -> bool:
        """Logout user by invalidating session."""
        try:
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            
            session = db.query(UserSession).filter(
                UserSession.token_hash == token_hash,
                UserSession.is_active == True
            ).first()
            
            if session:
                session.is_active = False
                db.commit()
                logger.info(f"User logged out: {session.user_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return False
    
    def get_user_tenants(self, db: DBSession, user_id: str) -> List[Tenant]:
        """Get all tenants for a user."""
        try:
            memberships = db.query(TenantMembership).filter(
                TenantMembership.user_id == user_id,
                TenantMembership.is_active == True
            ).all()
            
            tenant_ids = [membership.tenant_id for membership in memberships]
            tenants = db.query(Tenant).filter(Tenant.id.in_(tenant_ids)).all()
            
            return tenants
            
        except Exception as e:
            logger.error(f"Error getting user tenants: {e}")
            return []
    
    def switch_tenant(self, db: DBSession, user_id: str, tenant_id: str) -> bool:
        """Switch user's active tenant."""
        try:
            # Check if user has membership in tenant
            membership = db.query(TenantMembership).filter(
                TenantMembership.user_id == user_id,
                TenantMembership.tenant_id == tenant_id,
                TenantMembership.is_active == True
            ).first()
            
            if not membership:
                return False
            
            # Update user's active tenant in session
            # This would typically be stored in the session or user preferences
            logger.info(f"User {user_id} switched to tenant {tenant_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error switching tenant: {e}")
            return False
    
    def update_user(self, db: DBSession, user_id: str, user_data: UpdateUserRequest) -> Optional[User]:
        """Update user information."""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            if user_data.name is not None:
                user.name = user_data.name
            if user_data.avatar is not None:
                user.avatar = user_data.avatar
            if user_data.role is not None:
                user.role = user_data.role
                user.permissions = self.rbac_service.get_role_permissions(user_data.role)
            
            user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(user)
            
            logger.info(f"Updated user: {user.email}")
            return user
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user: {e}")
            raise
    
    def create_api_key(self, db: DBSession, user_id: str, api_key_data: CreateAPIKeyRequest, 
                      tenant_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a new API key for a user."""
        try:
            # Generate API key
            api_key = f"xr_{uuid.uuid4().hex}"
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            
            # Create API key record
            api_key_record = APIKey(
                user_id=user_id,
                tenant_id=tenant_id,
                name=api_key_data.name,
                key_hash=key_hash,
                permissions=api_key_data.permissions,
                expires_at=api_key_data.expires_at
            )
            
            db.add(api_key_record)
            db.commit()
            db.refresh(api_key_record)
            
            logger.info(f"Created API key for user: {user_id}")
            
            return {
                "id": str(api_key_record.id),
                "name": api_key_record.name,
                "key": api_key,  # Only returned once
                "permissions": api_key_record.permissions,
                "expires_at": api_key_record.expires_at,
                "created_at": api_key_record.created_at
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating API key: {e}")
            raise
    
    def validate_api_key(self, db: DBSession, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return user/tenant information."""
        try:
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            
            api_key_record = db.query(APIKey).filter(
                APIKey.key_hash == key_hash,
                APIKey.is_active == True
            ).first()
            
            if not api_key_record or api_key_record.is_expired():
                return None
            
            # Update last used
            api_key_record.last_used = datetime.utcnow()
            db.commit()
            
            user = db.query(User).filter(User.id == api_key_record.user_id).first()
            tenant = None
            if api_key_record.tenant_id:
                tenant = db.query(Tenant).filter(Tenant.id == api_key_record.tenant_id).first()
            
            return {
                "user": user,
                "tenant": tenant,
                "permissions": api_key_record.permissions or []
            }
            
        except Exception as e:
            logger.error(f"Error validating API key: {e}")
            return None
    
    def _generate_refresh_token(self) -> str:
        """Generate a refresh token."""
        return f"rt_{uuid.uuid4().hex}"


# Global auth service instance
auth_service = AuthService()
