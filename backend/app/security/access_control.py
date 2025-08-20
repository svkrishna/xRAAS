"""
Access Control Management
Role-based access control (RBAC) and permission management for XReason.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PermissionLevel(str, Enum):
    """Permission levels."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    EXECUTE = "execute"


class ResourceType(str, Enum):
    """Types of resources that can be protected."""
    API = "api"
    DATABASE = "database"
    FILE = "file"
    SERVICE = "service"
    TENANT = "tenant"
    USER = "user"
    RULESET = "ruleset"
    GRAPH = "graph"
    BILLING = "billing"
    MARKETPLACE = "marketplace"


@dataclass
class Permission:
    """A permission definition."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    resource_type: ResourceType = ResourceType.API
    resource_id: str = ""
    permission_level: PermissionLevel = PermissionLevel.READ
    conditions: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "resource_type": self.resource_type.value,
            "resource_id": self.resource_id,
            "permission_level": self.permission_level.value,
            "conditions": self.conditions,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Permission':
        """Create from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            resource_type=ResourceType(data.get("resource_type", "api")),
            resource_id=data.get("resource_id", ""),
            permission_level=PermissionLevel(data.get("permission_level", "read")),
            conditions=data.get("conditions", {}),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat()))
        )


@dataclass
class Role:
    """A role definition with permissions."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    permissions: List[Permission] = field(default_factory=list)
    is_system_role: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "permissions": [perm.to_dict() for perm in self.permissions],
            "is_system_role": self.is_system_role,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Role':
        """Create from dictionary."""
        role = cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            is_system_role=data.get("is_system_role", False),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.utcnow().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.utcnow().isoformat()))
        )
        
        # Add permissions
        for perm_data in data.get("permissions", []):
            role.permissions.append(Permission.from_dict(perm_data))
        
        return role
    
    def add_permission(self, permission: Permission) -> None:
        """Add a permission to this role."""
        self.permissions.append(permission)
        self.updated_at = datetime.utcnow()
    
    def remove_permission(self, permission_id: str) -> bool:
        """Remove a permission from this role."""
        for i, perm in enumerate(self.permissions):
            if perm.id == permission_id:
                del self.permissions[i]
                self.updated_at = datetime.utcnow()
                return True
        return False
    
    def has_permission(self, resource_type: ResourceType, resource_id: str, 
                      permission_level: PermissionLevel) -> bool:
        """Check if this role has a specific permission."""
        for perm in self.permissions:
            if (perm.resource_type == resource_type and 
                perm.resource_id == resource_id and
                perm.permission_level == permission_level):
                return True
        return False


class AccessControlManager:
    """Manages access control and permissions."""
    
    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.user_roles: Dict[str, List[str]] = {}  # user_id -> role_ids
        self.tenant_roles: Dict[str, List[str]] = {}  # tenant_id -> role_ids
        self.logger = logging.getLogger(__name__)
        
        # Initialize default roles
        self._initialize_default_roles()
    
    def create_role(self, name: str, description: str = "", 
                   permissions: Optional[List[Permission]] = None) -> Role:
        """Create a new role."""
        try:
            role = Role(
                name=name,
                description=description,
                permissions=permissions or []
            )
            
            self.roles[role.id] = role
            
            self.logger.info(f"Created role: {name} ({role.id})")
            return role
            
        except Exception as e:
            self.logger.error(f"Error creating role: {e}")
            raise
    
    def get_role(self, role_id: str) -> Optional[Role]:
        """Get a role by ID."""
        return self.roles.get(role_id)
    
    def get_role_by_name(self, name: str) -> Optional[Role]:
        """Get a role by name."""
        for role in self.roles.values():
            if role.name == name:
                return role
        return None
    
    def update_role(self, role_id: str, **kwargs) -> bool:
        """Update a role."""
        try:
            role = self.roles.get(role_id)
            if not role:
                return False
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(role, key):
                    setattr(role, key, value)
            
            role.updated_at = datetime.utcnow()
            
            self.logger.info(f"Updated role: {role_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating role: {e}")
            return False
    
    def delete_role(self, role_id: str) -> bool:
        """Delete a role."""
        try:
            role = self.roles.get(role_id)
            if not role:
                return False
            
            if role.is_system_role:
                raise ValueError("Cannot delete system roles")
            
            # Remove role from all users and tenants
            for user_id in list(self.user_roles.keys()):
                if role_id in self.user_roles[user_id]:
                    self.user_roles[user_id].remove(role_id)
            
            for tenant_id in list(self.tenant_roles.keys()):
                if role_id in self.tenant_roles[tenant_id]:
                    self.tenant_roles[tenant_id].remove(role_id)
            
            del self.roles[role_id]
            
            self.logger.info(f"Deleted role: {role_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting role: {e}")
            return False
    
    def assign_role_to_user(self, user_id: str, role_id: str) -> bool:
        """Assign a role to a user."""
        try:
            if role_id not in self.roles:
                return False
            
            if user_id not in self.user_roles:
                self.user_roles[user_id] = []
            
            if role_id not in self.user_roles[user_id]:
                self.user_roles[user_id].append(role_id)
            
            self.logger.info(f"Assigned role {role_id} to user {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error assigning role to user: {e}")
            return False
    
    def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """Remove a role from a user."""
        try:
            if user_id in self.user_roles and role_id in self.user_roles[user_id]:
                self.user_roles[user_id].remove(role_id)
                self.logger.info(f"Removed role {role_id} from user {user_id}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error removing role from user: {e}")
            return False
    
    def assign_role_to_tenant(self, tenant_id: str, role_id: str) -> bool:
        """Assign a role to a tenant."""
        try:
            if role_id not in self.roles:
                return False
            
            if tenant_id not in self.tenant_roles:
                self.tenant_roles[tenant_id] = []
            
            if role_id not in self.tenant_roles[tenant_id]:
                self.tenant_roles[tenant_id].append(role_id)
            
            self.logger.info(f"Assigned role {role_id} to tenant {tenant_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error assigning role to tenant: {e}")
            return False
    
    def get_user_roles(self, user_id: str) -> List[Role]:
        """Get all roles assigned to a user."""
        role_ids = self.user_roles.get(user_id, [])
        return [self.roles[role_id] for role_id in role_ids if role_id in self.roles]
    
    def get_tenant_roles(self, tenant_id: str) -> List[Role]:
        """Get all roles assigned to a tenant."""
        role_ids = self.tenant_roles.get(tenant_id, [])
        return [self.roles[role_id] for role_id in role_ids if role_id in self.roles]
    
    def check_permission(self, user_id: str, resource_type: ResourceType, 
                        resource_id: str, permission_level: PermissionLevel,
                        tenant_id: Optional[str] = None) -> bool:
        """Check if a user has a specific permission."""
        try:
            # Get user roles
            user_roles = self.get_user_roles(user_id)
            
            # Get tenant roles if tenant_id is provided
            tenant_roles = []
            if tenant_id:
                tenant_roles = self.get_tenant_roles(tenant_id)
            
            # Check all roles for the permission
            all_roles = user_roles + tenant_roles
            
            for role in all_roles:
                if role.has_permission(resource_type, resource_id, permission_level):
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking permission: {e}")
            return False
    
    def get_user_permissions(self, user_id: str, tenant_id: Optional[str] = None) -> List[Permission]:
        """Get all permissions for a user."""
        try:
            permissions = []
            
            # Get user roles
            user_roles = self.get_user_roles(user_id)
            for role in user_roles:
                permissions.extend(role.permissions)
            
            # Get tenant roles if tenant_id is provided
            if tenant_id:
                tenant_roles = self.get_tenant_roles(tenant_id)
                for role in tenant_roles:
                    permissions.extend(role.permissions)
            
            # Remove duplicates based on permission ID
            unique_permissions = {}
            for perm in permissions:
                unique_permissions[perm.id] = perm
            
            return list(unique_permissions.values())
            
        except Exception as e:
            self.logger.error(f"Error getting user permissions: {e}")
            return []
    
    def _initialize_default_roles(self) -> None:
        """Initialize default system roles."""
        
        # Owner role - full access
        owner_permissions = [
            Permission(
                name="Full Access",
                description="Full access to all resources",
                resource_type=ResourceType.API,
                resource_id="*",
                permission_level=PermissionLevel.ADMIN
            )
        ]
        
        owner_role = Role(
            name="Owner",
            description="Full system access",
            permissions=owner_permissions,
            is_system_role=True
        )
        self.roles[owner_role.id] = owner_role
        
        # Admin role - administrative access
        admin_permissions = [
            Permission(
                name="Admin Access",
                description="Administrative access to most resources",
                resource_type=ResourceType.API,
                resource_id="*",
                permission_level=PermissionLevel.ADMIN
            ),
            Permission(
                name="User Management",
                description="Manage users and roles",
                resource_type=ResourceType.USER,
                resource_id="*",
                permission_level=PermissionLevel.WRITE
            )
        ]
        
        admin_role = Role(
            name="Admin",
            description="Administrative access",
            permissions=admin_permissions,
            is_system_role=True
        )
        self.roles[admin_role.id] = admin_role
        
        # Analyst role - read and execute access
        analyst_permissions = [
            Permission(
                name="Read Access",
                description="Read access to most resources",
                resource_type=ResourceType.API,
                resource_id="*",
                permission_level=PermissionLevel.READ
            ),
            Permission(
                name="Execute Reasoning",
                description="Execute reasoning operations",
                resource_type=ResourceType.SERVICE,
                resource_id="reasoning",
                permission_level=PermissionLevel.EXECUTE
            )
        ]
        
        analyst_role = Role(
            name="Analyst",
            description="Data analysis and reasoning",
            permissions=analyst_permissions,
            is_system_role=True
        )
        self.roles[analyst_role.id] = analyst_role
        
        # Viewer role - read-only access
        viewer_permissions = [
            Permission(
                name="Read Access",
                description="Read access to resources",
                resource_type=ResourceType.API,
                resource_id="*",
                permission_level=PermissionLevel.READ
            )
        ]
        
        viewer_role = Role(
            name="Viewer",
            description="Read-only access",
            permissions=viewer_permissions,
            is_system_role=True
        )
        self.roles[viewer_role.id] = viewer_role
        
        self.logger.info("Initialized default roles")


# Global access control manager instance
access_control_manager = AccessControlManager()
