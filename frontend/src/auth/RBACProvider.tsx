/**
 * RBAC Provider
 * Role-Based Access Control with permission checking
 */

import React, { createContext, useContext, useMemo } from 'react';
import { Role, Permission, User, Tenant, RBACContext } from './types';
import { useAuth } from './AuthProvider';

const RBACContext = createContext<RBACContext | undefined>(undefined);

// Role hierarchy - higher roles inherit permissions from lower roles
const roleHierarchy: Record<Role, Role[]> = {
  [Role.OWNER]: [Role.ADMIN, Role.ANALYST, Role.DEVELOPER, Role.VIEWER, Role.PARTNER],
  [Role.ADMIN]: [Role.ANALYST, Role.DEVELOPER, Role.VIEWER, Role.PARTNER],
  [Role.ANALYST]: [Role.VIEWER],
  [Role.DEVELOPER]: [Role.VIEWER],
  [Role.VIEWER]: [],
  [Role.PARTNER]: [Role.VIEWER]
};

// Permission mappings by role
const rolePermissions: Record<Role, Permission[]> = {
  [Role.OWNER]: [
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
  [Role.ADMIN]: [
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
  [Role.ANALYST]: [
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
  [Role.DEVELOPER]: [
    Permission.VIEW_USERS,
    Permission.VIEW_ANALYTICS,
    Permission.VIEW_RULESETS,
    Permission.PROMOTE_RULESETS,
    Permission.VIEW_AUDIT,
    Permission.MANAGE_API_KEYS,
    Permission.MANAGE_WEBHOOKS
  ],
  [Role.VIEWER]: [
    Permission.VIEW_ANALYTICS,
    Permission.VIEW_COMPLIANCE,
    Permission.VIEW_RULESETS,
    Permission.VIEW_AUDIT
  ],
  [Role.PARTNER]: [
    Permission.VIEW_ANALYTICS,
    Permission.VIEW_RULESETS,
    Permission.SUBMIT_RULESETS,
    Permission.VIEW_AUDIT
  ]
};

interface RBACProviderProps {
  children: React.ReactNode;
}

export function RBACProvider({ children }: RBACProviderProps) {
  const { user, session } = useAuth();

  const rbacContext = useMemo((): RBACContext | null => {
    if (!user || !session) return null;

    // Get all permissions for the user's role (including inherited)
    const getUserPermissions = (userRole: Role): Permission[] => {
      const directPermissions = rolePermissions[userRole] || [];
      const inheritedRoles = roleHierarchy[userRole] || [];
      
      const inheritedPermissions = inheritedRoles.flatMap(role => 
        rolePermissions[role] || []
      );
      
      return [...new Set([...directPermissions, ...inheritedPermissions])];
    };

    const permissions = getUserPermissions(user.role);

    return {
      user,
      tenant: session.tenant,
      permissions,
      hasPermission: (permission: Permission) => permissions.includes(permission),
      hasRole: (role: Role) => {
        // Check if user has the exact role or a higher role
        const userRoleIndex = Object.values(Role).indexOf(user.role);
        const requiredRoleIndex = Object.values(Role).indexOf(role);
        return userRoleIndex <= requiredRoleIndex;
      }
    };
  }, [user, session]);

  if (!rbacContext) {
    return <>{children}</>;
  }

  return (
    <RBACContext.Provider value={rbacContext}>
      {children}
    </RBACContext.Provider>
  );
}

export function useRBAC(): RBACContext {
  const context = useContext(RBACContext);
  if (context === undefined) {
    throw new Error('useRBAC must be used within an RBACProvider');
  }
  return context;
}

// Higher-order component for permission-based rendering
export function withPermission(
  WrappedComponent: React.ComponentType<any>,
  requiredPermission: Permission
) {
  return function PermissionWrapper(props: any) {
    const { hasPermission } = useRBAC();
    
    if (!hasPermission(requiredPermission)) {
      return null; // Or render an access denied component
    }
    
    return <WrappedComponent {...props} />;
  };
}

// Higher-order component for role-based rendering
export function withRole(
  WrappedComponent: React.ComponentType<any>,
  requiredRole: Role
) {
  return function RoleWrapper(props: any) {
    const { hasRole } = useRBAC();
    
    if (!hasRole(requiredRole)) {
      return null; // Or render an access denied component
    }
    
    return <WrappedComponent {...props} />;
  };
}
