/**
 * Tenant Provider
 * Multi-tenant management with tenant switching and context
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import { Tenant, TenantContext as ITenantContext } from './types';
import { useAuth } from './AuthProvider';
import { tenantService } from '../services/tenantService';

const TenantContext = createContext<ITenantContext | undefined>(undefined);

interface TenantProviderProps {
  children: React.ReactNode;
}

export function TenantProvider({ children }: TenantProviderProps) {
  const { user, session } = useAuth();
  const [currentTenant, setCurrentTenant] = useState<Tenant | null>(null);
  const [availableTenants, setAvailableTenants] = useState<Tenant[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Load user's available tenants
  useEffect(() => {
    const loadTenants = async () => {
      if (!user) return;

      try {
        setIsLoading(true);
        const tenants = await tenantService.getUserTenants(user.id);
        setAvailableTenants(tenants);

        // Set current tenant from session or default to first available
        if (session?.tenant) {
          setCurrentTenant(session.tenant);
        } else if (tenants.length > 0) {
          setCurrentTenant(tenants[0]);
        }
      } catch (error) {
        console.error('Failed to load tenants:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadTenants();
  }, [user, session]);

  const switchTenant = async (tenantId: string) => {
    try {
      const tenant = availableTenants.find(t => t.id === tenantId);
      if (!tenant) {
        throw new Error('Tenant not found');
      }

      // Call backend to switch tenant context
      await tenantService.switchTenant(tenantId);
      setCurrentTenant(tenant);

      // Update session context
      if (session) {
        session.tenant = tenant;
      }
    } catch (error) {
      console.error('Failed to switch tenant:', error);
      throw error;
    }
  };

  const createTenant = async (tenantData: Partial<Tenant>): Promise<Tenant> => {
    try {
      const newTenant = await tenantService.createTenant(tenantData);
      setAvailableTenants(prev => [...prev, newTenant]);
      return newTenant;
    } catch (error) {
      console.error('Failed to create tenant:', error);
      throw error;
    }
  };

  const updateTenant = async (tenantId: string, updates: Partial<Tenant>): Promise<Tenant> => {
    try {
      const updatedTenant = await tenantService.updateTenant(tenantId, updates);
      
      setAvailableTenants(prev => 
        prev.map(t => t.id === tenantId ? updatedTenant : t)
      );
      
      if (currentTenant?.id === tenantId) {
        setCurrentTenant(updatedTenant);
      }
      
      return updatedTenant;
    } catch (error) {
      console.error('Failed to update tenant:', error);
      throw error;
    }
  };

  const deleteTenant = async (tenantId: string): Promise<void> => {
    try {
      await tenantService.deleteTenant(tenantId);
      
      setAvailableTenants(prev => prev.filter(t => t.id !== tenantId));
      
      // If current tenant is deleted, switch to first available
      if (currentTenant?.id === tenantId && availableTenants.length > 1) {
        const remainingTenants = availableTenants.filter(t => t.id !== tenantId);
        if (remainingTenants.length > 0) {
          await switchTenant(remainingTenants[0].id);
        }
      }
    } catch (error) {
      console.error('Failed to delete tenant:', error);
      throw error;
    }
  };

  const value: ITenantContext = {
    currentTenant: currentTenant!,
    availableTenants,
    isLoading,
    switchTenant,
    createTenant,
    updateTenant,
    deleteTenant
  };

  if (isLoading) {
    return <div>Loading tenants...</div>; // Replace with proper loading component
  }

  if (!currentTenant) {
    return <div>No tenants available</div>; // Replace with proper error component
  }

  return (
    <TenantContext.Provider value={value}>
      {children}
    </TenantContext.Provider>
  );
}

export function useTenant(): ITenantContext {
  const context = useContext(TenantContext);
  if (context === undefined) {
    throw new Error('useTenant must be used within a TenantProvider');
  }
  return context;
}
