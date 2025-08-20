/**
 * Tenant Service
 * Handles tenant management API calls
 */

import { Tenant } from '../auth/types';
import { apiClient } from './api';

export const tenantService = {
  async getUserTenants(userId: string): Promise<Tenant[]> {
    const response = await apiClient.get('/api/v1/auth/tenants');
    return response.data.tenants;
  },

  async switchTenant(tenantId: string): Promise<void> {
    await apiClient.post('/api/v1/auth/tenants/switch', { tenant_id: tenantId });
  },

  async createTenant(tenantData: Partial<Tenant>): Promise<Tenant> {
    const response = await apiClient.post('/api/v1/auth/tenants', tenantData);
    return response.data;
  },

  async updateTenant(tenantId: string, updates: Partial<Tenant>): Promise<Tenant> {
    const response = await apiClient.put(`/api/v1/auth/tenants/${tenantId}`, updates);
    return response.data;
  },

  async deleteTenant(tenantId: string): Promise<void> {
    await apiClient.delete(`/api/v1/auth/tenants/${tenantId}`);
  },

  async getTenantDetails(tenantId: string): Promise<Tenant> {
    const response = await apiClient.get(`/api/v1/auth/tenants/${tenantId}`);
    return response.data;
  }
};
