/**
 * Authentication Service
 * Handles authentication API calls
 */

import { LoginCredentials, User, Session } from '../auth/types';
import { apiClient } from './api';

export const authService = {
  async login(credentials: LoginCredentials): Promise<Session> {
    const response = await apiClient.post('/api/v1/auth/login', credentials);
    return response.data;
  },

  async logout(token: string): Promise<void> {
    await apiClient.post('/api/v1/auth/logout', {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
  },

  async validateSession(token: string): Promise<Session> {
    const response = await apiClient.get('/api/v1/auth/status', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },

  async refreshSession(token: string): Promise<Session> {
    const response = await apiClient.post('/api/v1/auth/refresh', {
      refresh_token: token
    });
    return response.data;
  },

  async updateUser(userId: string, updates: Partial<User>): Promise<User> {
    const response = await apiClient.put(`/api/v1/auth/users/${userId}`, updates);
    return response.data;
  },

  async forgotPassword(email: string): Promise<void> {
    await apiClient.post('/api/v1/auth/forgot-password', { email });
  },

  async resetPassword(token: string, newPassword: string): Promise<void> {
    await apiClient.post('/api/v1/auth/reset-password', { token, newPassword });
  }
};
