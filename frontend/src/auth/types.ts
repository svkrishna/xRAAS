/**
 * Authentication and Authorization Types
 * Type definitions for XReason's enterprise auth system
 */

export enum Role {
  OWNER = 'owner',
  ADMIN = 'admin',
  ANALYST = 'analyst',
  DEVELOPER = 'developer',
  VIEWER = 'viewer',
  PARTNER = 'partner'
}

export enum Permission {
  // User Management
  MANAGE_USERS = 'manage_users',
  VIEW_USERS = 'view_users',
  
  // Tenant Management
  MANAGE_TENANT = 'manage_tenant',
  SWITCH_TENANTS = 'switch_tenants',
  
  // Billing & Subscriptions
  MANAGE_BILLING = 'manage_billing',
  VIEW_BILLING = 'view_billing',
  
  // Analytics & Usage
  VIEW_ANALYTICS = 'view_analytics',
  EXPORT_ANALYTICS = 'export_analytics',
  
  // Compliance
  MANAGE_COMPLIANCE = 'manage_compliance',
  VIEW_COMPLIANCE = 'view_compliance',
  UPLOAD_EVIDENCE = 'upload_evidence',
  
  // Rulesets
  MANAGE_RULESETS = 'manage_rulesets',
  VIEW_RULESETS = 'view_rulesets',
  PROMOTE_RULESETS = 'promote_rulesets',
  
  // Audit
  VIEW_AUDIT = 'view_audit',
  EXPORT_AUDIT = 'export_audit',
  
  // Partners
  MANAGE_PARTNERS = 'manage_partners',
  VIEW_PARTNERS = 'view_partners',
  SUBMIT_RULESETS = 'submit_rulesets',
  
  // Admin
  MANAGE_API_KEYS = 'manage_api_keys',
  MANAGE_WEBHOOKS = 'manage_webhooks',
  MANAGE_FEATURE_FLAGS = 'manage_feature_flags'
}

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: Role;
  permissions: Permission[];
  tenantId: string;
  lastLogin?: Date;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface Tenant {
  id: string;
  name: string;
  slug: string;
  domain?: string;
  subscriptionTier: 'starter' | 'professional' | 'enterprise' | 'mission_critical';
  status: 'active' | 'suspended' | 'cancelled';
  createdAt: Date;
  updatedAt: Date;
}

export interface Session {
  user: User;
  tenant: Tenant;
  token: string;
  expiresAt: Date;
  permissions: Permission[];
}

export interface AuthState {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: User | null;
  session: Session | null;
  error: string | null;
}

export interface LoginCredentials {
  email: string;
  password: string;
  tenantId?: string;
}

export interface SSOConfig {
  provider: 'google' | 'azure' | 'okta' | 'onelogin';
  clientId: string;
  redirectUri: string;
  scopes: string[];
}

export interface RBACContext {
  user: User;
  tenant: Tenant;
  permissions: Permission[];
  hasPermission: (permission: Permission) => boolean;
  hasRole: (role: Role) => boolean;
}

export interface TenantContext {
  currentTenant: Tenant;
  availableTenants: Tenant[];
  switchTenant: (tenantId: string) => Promise<void>;
  createTenant: (tenant: Partial<Tenant>) => Promise<Tenant>;
}
