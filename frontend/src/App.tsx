/**
 * Main App Component
 * Updated for Iteration 4 with authentication, theming, and new layout
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './theme/ThemeProvider';
import { AuthProvider, useAuth } from './auth/AuthProvider';
import { RBACProvider } from './auth/RBACProvider';
import { TenantProvider } from './auth/TenantProvider';
import { AppShell } from './layout/AppShell';
import { LoginPage } from './pages/LoginPage';
import { Dashboard } from './pages/Dashboard';
import { ReasoningDemo } from './pages/ReasoningDemo';
import { GraphDemo } from './pages/GraphDemo';
import { ApiDocs } from './pages/ApiDocs';
import { Home } from './pages/Home';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoadingScreen } from './components/LoadingScreen';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <RBACProvider>
          <TenantProvider>
            <Router>
              <AppContent />
            </Router>
          </TenantProvider>
        </RBACProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

function AppContent() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    return (
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/reasoning" element={<ReasoningDemo />} />
        <Route path="/graphs" element={<GraphDemo />} />
        <Route path="/api-docs" element={<ApiDocs />} />
        <Route path="/home" element={<Home />} />
        
        {/* Protected routes with RBAC */}
        <Route 
          path="/analytics" 
          element={
            <ProtectedRoute permission="view_analytics">
              <AnalyticsPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/compliance" 
          element={
            <ProtectedRoute permission="view_compliance">
              <CompliancePage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/rulesets" 
          element={
            <ProtectedRoute permission="view_rulesets">
              <RulesetsPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/audit" 
          element={
            <ProtectedRoute permission="view_audit">
              <AuditPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/partners" 
          element={
            <ProtectedRoute permission="view_partners">
              <PartnersPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/billing" 
          element={
            <ProtectedRoute permission="view_billing">
              <BillingPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/admin" 
          element={
            <ProtectedRoute permission="manage_users">
              <AdminPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/settings" 
          element={<SettingsPage />} 
        />
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppShell>
  );
}

// Placeholder components for new pages
function AnalyticsPage() {
  return <div>Analytics Page - Coming Soon</div>;
}

function CompliancePage() {
  return <div>Compliance Page - Coming Soon</div>;
}

function RulesetsPage() {
  return <div>Rulesets Page - Coming Soon</div>;
}

function AuditPage() {
  return <div>Audit Page - Coming Soon</div>;
}

function PartnersPage() {
  return <div>Partners Page - Coming Soon</div>;
}

function BillingPage() {
  return <div>Billing Page - Coming Soon</div>;
}

function AdminPage() {
  return <div>Admin Page - Coming Soon</div>;
}

function SettingsPage() {
  return <div>Settings Page - Coming Soon</div>;
}

export default App;
