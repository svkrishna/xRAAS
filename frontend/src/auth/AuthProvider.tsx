/**
 * Authentication Provider
 * Main authentication context provider with session management
 */

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { AuthState, User, Session, LoginCredentials } from './types';
import { authService } from '../services/authService';

interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => Promise<void>;
  refreshSession: () => Promise<void>;
  updateUser: (user: Partial<User>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Initial state
const initialState: AuthState = {
  isAuthenticated: false,
  isLoading: true,
  user: null,
  session: null,
  error: null
};

// Action types
type AuthAction =
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; payload: { user: User; session: Session } }
  | { type: 'AUTH_FAILURE'; payload: string }
  | { type: 'AUTH_LOGOUT' }
  | { type: 'UPDATE_USER'; payload: User }
  | { type: 'CLEAR_ERROR' };

// Reducer
function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'AUTH_START':
      return { ...state, isLoading: true, error: null };
    
    case 'AUTH_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        isLoading: false,
        user: action.payload.user,
        session: action.payload.session,
        error: null
      };
    
    case 'AUTH_FAILURE':
      return {
        ...state,
        isAuthenticated: false,
        isLoading: false,
        user: null,
        session: null,
        error: action.payload
      };
    
    case 'AUTH_LOGOUT':
      return {
        ...state,
        isAuthenticated: false,
        isLoading: false,
        user: null,
        session: null,
        error: null
      };
    
    case 'UPDATE_USER':
      return {
        ...state,
        user: action.payload
      };
    
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null
      };
    
    default:
      return state;
  }
}

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check for existing session on mount
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        if (token) {
          const session = await authService.validateSession(token);
          dispatch({
            type: 'AUTH_SUCCESS',
            payload: { user: session.user, session }
          });
        } else {
          dispatch({ type: 'AUTH_FAILURE', payload: 'No session found' });
        }
      } catch (error) {
        dispatch({ type: 'AUTH_FAILURE', payload: 'Session validation failed' });
      }
    };

    initializeAuth();
  }, []);

  // Auto-refresh session before expiry
  useEffect(() => {
    if (!state.session) return;

    const timeUntilExpiry = state.session.expiresAt.getTime() - Date.now();
    const refreshTime = Math.max(timeUntilExpiry - 5 * 60 * 1000, 0); // 5 minutes before expiry

    const refreshTimer = setTimeout(() => {
      refreshSession();
    }, refreshTime);

    return () => clearTimeout(refreshTimer);
  }, [state.session]);

  const login = async (credentials: LoginCredentials) => {
    try {
      dispatch({ type: 'AUTH_START' });
      const session = await authService.login(credentials);
      localStorage.setItem('auth_token', session.token);
      dispatch({
        type: 'AUTH_SUCCESS',
        payload: { user: session.user, session }
      });
    } catch (error) {
      dispatch({ type: 'AUTH_FAILURE', payload: error.message });
      throw error;
    }
  };

  const logout = async () => {
    try {
      if (state.session) {
        await authService.logout(state.session.token);
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('auth_token');
      dispatch({ type: 'AUTH_LOGOUT' });
    }
  };

  const refreshSession = async () => {
    try {
      if (!state.session) return;
      
      const newSession = await authService.refreshSession(state.session.token);
      localStorage.setItem('auth_token', newSession.token);
      dispatch({
        type: 'AUTH_SUCCESS',
        payload: { user: newSession.user, session: newSession }
      });
    } catch (error) {
      dispatch({ type: 'AUTH_FAILURE', payload: 'Session refresh failed' });
    }
  };

  const updateUser = async (userUpdates: Partial<User>) => {
    try {
      if (!state.user) return;
      
      const updatedUser = await authService.updateUser(state.user.id, userUpdates);
      dispatch({ type: 'UPDATE_USER', payload: updatedUser });
    } catch (error) {
      console.error('User update error:', error);
      throw error;
    }
  };

  const value: AuthContextType = {
    ...state,
    login,
    logout,
    refreshSession,
    updateUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
