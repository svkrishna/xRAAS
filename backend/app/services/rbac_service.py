"""
RBAC Service for XReason
Role-Based Access Control service for managing permissions and roles.
"""

from typing import List, Dict, Any
from app.schemas.auth import Role, Permission


class RBACService:
    """Role-Based Access Control service."""
    
    # Role hierarchy - higher roles inherit permissions from lower roles
    ROLE_HIERARCHY = {
        Role.OWNER: [Role.ADMIN, Role.ANALYST, Role.DEVELOPER, Role.VIEWER, Role.PARTNER],
        Role.ADMIN: [Role.ANALYST, Role.DEVELOPER, Role.VIEWER, Role.PARTNER],
        Role.ANALYST: [Role.VIEWER],
        Role.DEVELOPER: [Role.VIEWER],
        Role.VIEWER: [],
        Role.PARTNER: [Role.VIEWER]
    }
    
    # Permission mappings by role
    ROLE_PERMISSIONS = {
        Role.OWNER: [
            Permission.MANAGE_USERS,
            Permission.VIEW_USERS,
            Permission.MANAGE_TENANT,
            Permission.SWITCH_TENANTS,
            Permission.MANAGE_BILLING,
            Permission.VIEW_BILLING,
            Permission.VIEW_ANALYTICS,
            Permission.EXPORT_ANALYTICS,
            Permission.MANAGE_COMPLIANCE,
            Permission.VIEW_COMPLIANCE,
            Permission.UPLOAD_EVIDENCE,
            Permission.MANAGE_RULESETS,
            Permission.VIEW_RULESETS,
            Permission.PROMOTE_RULESETS,
            Permission.VIEW_AUDIT,
            Permission.EXPORT_AUDIT,
            Permission.MANAGE_PARTNERS,
            Permission.VIEW_PARTNERS,
            Permission.SUBMIT_RULESETS,
            Permission.MANAGE_API_KEYS,
            Permission.MANAGE_WEBHOOKS,
            Permission.MANAGE_FEATURE_FLAGS
        ],
        Role.ADMIN: [
            Permission.MANAGE_USERS,
            Permission.VIEW_USERS,
            Permission.MANAGE_TENANT,
            Permission.SWITCH_TENANTS,
            Permission.MANAGE_BILLING,
            Permission.VIEW_BILLING,
            Permission.VIEW_ANALYTICS,
            Permission.EXPORT_ANALYTICS,
            Permission.MANAGE_COMPLIANCE,
            Permission.VIEW_COMPLIANCE,
            Permission.UPLOAD_EVIDENCE,
            Permission.MANAGE_RULESETS,
            Permission.VIEW_RULESETS,
            Permission.PROMOTE_RULESETS,
            Permission.VIEW_AUDIT,
            Permission.EXPORT_AUDIT,
            Permission.VIEW_PARTNERS,
            Permission.MANAGE_API_KEYS,
            Permission.MANAGE_WEBHOOKS
        ],
        Role.ANALYST: [
            Permission.VIEW_USERS,
            Permission.VIEW_BILLING,
            Permission.VIEW_ANALYTICS,
            Permission.EXPORT_ANALYTICS,
            Permission.VIEW_COMPLIANCE,
            Permission.UPLOAD_EVIDENCE,
            Permission.VIEW_RULESETS,
            Permission.VIEW_AUDIT,
            Permission.EXPORT_AUDIT,
            Permission.VIEW_PARTNERS
        ],
        Role.DEVELOPER: [
            Permission.VIEW_USERS,
            Permission.VIEW_ANALYTICS,
            Permission.VIEW_RULESETS,
            Permission.PROMOTE_RULESETS,
            Permission.VIEW_AUDIT,
            Permission.MANAGE_API_KEYS,
            Permission.MANAGE_WEBHOOKS
        ],
        Role.VIEWER: [
            Permission.VIEW_ANALYTICS,
            Permission.VIEW_COMPLIANCE,
            Permission.VIEW_RULESETS,
            Permission.VIEW_AUDIT
        ],
        Role.PARTNER: [
            Permission.VIEW_ANALYTICS,
            Permission.VIEW_RULESETS,
            Permission.SUBMIT_RULESETS,
            Permission.VIEW_AUDIT
        ]
    }
    
    def get_role_permissions(self, role: Role) -> List[Permission]:
        """Get all permissions for a role (including inherited)."""
        direct_permissions = self.ROLE_PERMISSIONS.get(role, [])
        inherited_roles = self.ROLE_HIERARCHY.get(role, [])
        
        inherited_permissions = []
        for inherited_role in inherited_roles:
            inherited_permissions.extend(self.ROLE_PERMISSIONS.get(inherited_role, []))
        
        # Remove duplicates while preserving order
        all_permissions = []
        seen = set()
        for permission in direct_permissions + inherited_permissions:
            if permission not in seen:
                all_permissions.append(permission)
                seen.add(permission)
        
        return all_permissions
    
    def has_permission(self, user_permissions: List[Permission], required_permission: Permission) -> bool:
        """Check if user has a specific permission."""
        return required_permission in user_permissions
    
    def has_role(self, user_role: Role, required_role: Role) -> bool:
        """Check if user has a specific role or higher."""
        if user_role == required_role:
            return True
        
        # Check if user's role is higher in hierarchy
        user_role_index = list(Role).index(user_role)
        required_role_index = list(Role).index(required_role)
        
        return user_role_index <= required_role_index
    
    def get_role_hierarchy(self) -> Dict[Role, List[Role]]:
        """Get the complete role hierarchy."""
        return self.ROLE_HIERARCHY.copy()
    
    def get_all_permissions(self) -> Dict[Role, List[Permission]]:
        """Get all permissions for all roles."""
        return {
            role: self.get_role_permissions(role)
            for role in Role
        }
    
    def validate_permissions(self, permissions: List[Permission]) -> List[str]:
        """Validate a list of permissions and return any errors."""
        errors = []
        valid_permissions = set(Permission)
        
        for permission in permissions:
            if permission not in valid_permissions:
                errors.append(f"Invalid permission: {permission}")
        
        return errors
    
    def get_permission_groups(self) -> Dict[str, List[Permission]]:
        """Get permissions grouped by category."""
        return {
            "User Management": [
                Permission.MANAGE_USERS,
                Permission.VIEW_USERS
            ],
            "Tenant Management": [
                Permission.MANAGE_TENANT,
                Permission.SWITCH_TENANTS
            ],
            "Billing & Subscriptions": [
                Permission.MANAGE_BILLING,
                Permission.VIEW_BILLING
            ],
            "Analytics & Usage": [
                Permission.VIEW_ANALYTICS,
                Permission.EXPORT_ANALYTICS
            ],
            "Compliance": [
                Permission.MANAGE_COMPLIANCE,
                Permission.VIEW_COMPLIANCE,
                Permission.UPLOAD_EVIDENCE
            ],
            "Rulesets": [
                Permission.MANAGE_RULESETS,
                Permission.VIEW_RULESETS,
                Permission.PROMOTE_RULESETS
            ],
            "Audit": [
                Permission.VIEW_AUDIT,
                Permission.EXPORT_AUDIT
            ],
            "Partners": [
                Permission.MANAGE_PARTNERS,
                Permission.VIEW_PARTNERS,
                Permission.SUBMIT_RULESETS
            ],
            "Admin": [
                Permission.MANAGE_API_KEYS,
                Permission.MANAGE_WEBHOOKS,
                Permission.MANAGE_FEATURE_FLAGS
            ]
        }
    
    def get_role_description(self, role: Role) -> str:
        """Get description for a role."""
        descriptions = {
            Role.OWNER: "Full system access with all permissions",
            Role.ADMIN: "Organization management with most permissions",
            Role.ANALYST: "Data analysis and compliance management",
            Role.DEVELOPER: "API integration and ruleset management",
            Role.VIEWER: "Read-only access to basic features",
            Role.PARTNER: "Partner ecosystem access with limited permissions"
        }
        return descriptions.get(role, "No description available")
    
    def get_permission_description(self, permission: Permission) -> str:
        """Get description for a permission."""
        descriptions = {
            # User Management
            Permission.MANAGE_USERS: "Create, update, and delete users",
            Permission.VIEW_USERS: "View user information and lists",
            
            # Tenant Management
            Permission.MANAGE_TENANT: "Manage tenant settings and configuration",
            Permission.SWITCH_TENANTS: "Switch between different tenants",
            
            # Billing & Subscriptions
            Permission.MANAGE_BILLING: "Manage billing and subscription settings",
            Permission.VIEW_BILLING: "View billing information and invoices",
            
            # Analytics & Usage
            Permission.VIEW_ANALYTICS: "View analytics and usage reports",
            Permission.EXPORT_ANALYTICS: "Export analytics data",
            
            # Compliance
            Permission.MANAGE_COMPLIANCE: "Manage compliance frameworks and settings",
            Permission.VIEW_COMPLIANCE: "View compliance status and reports",
            Permission.UPLOAD_EVIDENCE: "Upload compliance evidence",
            
            # Rulesets
            Permission.MANAGE_RULESETS: "Create, update, and delete rulesets",
            Permission.VIEW_RULESETS: "View rulesets and their details",
            Permission.PROMOTE_RULESETS: "Promote rulesets to production",
            
            # Audit
            Permission.VIEW_AUDIT: "View audit logs and history",
            Permission.EXPORT_AUDIT: "Export audit data",
            
            # Partners
            Permission.MANAGE_PARTNERS: "Manage partner relationships",
            Permission.VIEW_PARTNERS: "View partner information",
            Permission.SUBMIT_RULESETS: "Submit rulesets to marketplace",
            
            # Admin
            Permission.MANAGE_API_KEYS: "Create and manage API keys",
            Permission.MANAGE_WEBHOOKS: "Configure webhooks",
            Permission.MANAGE_FEATURE_FLAGS: "Manage feature flags"
        }
        return descriptions.get(permission, "No description available")


# Global RBAC service instance
rbac_service = RBACService()
