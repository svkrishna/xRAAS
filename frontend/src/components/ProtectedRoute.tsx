/**
 * Protected Route Component
 * Route protection with RBAC permission checking
 */

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useRBAC } from '../auth/RBACProvider';
import { Permission } from '../auth/types';

interface ProtectedRouteProps {
  children: React.ReactNode;
  permission?: Permission;
  role?: string;
  fallback?: React.ReactNode;
}

export function ProtectedRoute({ 
  children, 
  permission, 
  role, 
  fallback 
}: ProtectedRouteProps) {
  const { hasPermission, hasRole } = useRBAC();

  // Check permission if specified
  if (permission && !hasPermission(permission)) {
    if (fallback) {
      return <>{fallback}</>;
    }
    return <Navigate to="/unauthorized" replace />;
  }

  // Check role if specified
  if (role && !hasRole(role as any)) {
    if (fallback) {
      return <>{fallback}</>;
    }
    return <Navigate to="/unauthorized" replace />;
  }

  return <>{children}</>;
}
