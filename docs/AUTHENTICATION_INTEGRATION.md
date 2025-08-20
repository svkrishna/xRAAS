# 🔐 **Authentication Integration Guide**

This document provides a comprehensive guide to the authentication system integration between the XReason frontend and backend.

## 📋 **Table of Contents**

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Backend Implementation](#backend-implementation)
4. [Frontend Integration](#frontend-integration)
5. [API Endpoints](#api-endpoints)
6. [Database Schema](#database-schema)
7. [Security Features](#security-features)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

## 🎯 **Overview**

The authentication system provides:

- **User Authentication**: Login/logout with JWT tokens
- **Role-Based Access Control (RBAC)**: 6 roles with 20+ permissions
- **Multi-Tenancy**: Organization management and switching
- **Session Management**: Secure token-based sessions
- **API Key Management**: Programmatic access control
- **Password Security**: Bcrypt hashing with salt

## 🏗️ **Architecture**

### **Backend Components**

```
app/
├── models/auth.py          # Database models
├── schemas/auth.py         # Pydantic schemas
├── services/
│   ├── auth_service.py     # Authentication logic
│   └── rbac_service.py     # Role/permission management
└── api/auth.py            # FastAPI endpoints
```

### **Frontend Components**

```
src/
├── auth/
│   ├── AuthProvider.tsx    # Authentication context
│   ├── RBACProvider.tsx    # Role-based access control
│   ├── TenantProvider.tsx  # Multi-tenancy management
│   └── types.ts           # TypeScript interfaces
├── services/
│   ├── authService.ts     # Authentication API calls
│   └── tenantService.ts   # Tenant management API calls
└── components/
    ├── ProtectedRoute.tsx # Route protection
    └── LoginPage.tsx      # Login interface
```

## 🔧 **Backend Implementation**

### **Database Models**

#### **User Model**
```python
class User(Base):
    id = Column(UUID, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="viewer")
    permissions = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
```

#### **Tenant Model**
```python
class Tenant(Base):
    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)
    subscription_tier = Column(String, default="starter")
    status = Column(String, default="active")
```

#### **Session Model**
```python
class UserSession(Base):
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    token_hash = Column(String, index=True)
    refresh_token_hash = Column(String)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
```

### **Authentication Service**

The `AuthService` provides:

- **User Authentication**: Email/password verification
- **Session Management**: JWT token creation and validation
- **Password Security**: Bcrypt hashing and verification
- **Multi-Tenancy**: Tenant switching and management
- **API Key Management**: Programmatic access tokens

### **RBAC Service**

The `RBACService` manages:

- **Role Hierarchy**: 6 roles with inheritance
- **Permission Mapping**: 20+ granular permissions
- **Access Control**: Permission checking functions
- **Role Descriptions**: Human-readable role information

## 🎨 **Frontend Integration**

### **Authentication Provider**

```typescript
function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(authReducer, initialState);
  
  const login = async (credentials) => {
    const session = await authService.login(credentials);
    localStorage.setItem('auth_token', session.token);
    dispatch({ type: 'AUTH_SUCCESS', payload: session });
  };
  
  const logout = async () => {
    await authService.logout();
    localStorage.removeItem('auth_token');
    dispatch({ type: 'AUTH_LOGOUT' });
  };
  
  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

### **RBAC Provider**

```typescript
function RBACProvider({ children }) {
  const { user } = useAuth();
  
  const hasPermission = (permission) => {
    return user?.permissions?.includes(permission) || false;
  };
  
  const hasRole = (role) => {
    return user?.role === role || false;
  };
  
  return (
    <RBACContext.Provider value={{ hasPermission, hasRole }}>
      {children}
    </RBACContext.Provider>
  );
}
```

### **Protected Routes**

```typescript
function ProtectedRoute({ children, permission }) {
  const { hasPermission } = useRBAC();
  
  if (!hasPermission(permission)) {
    return <Navigate to="/login" />;
  }
  
  return children;
}
```

## 🌐 **API Endpoints**

### **Authentication Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/login` | User login |
| `POST` | `/api/v1/auth/register` | User registration |
| `POST` | `/api/v1/auth/refresh` | Token refresh |
| `POST` | `/api/v1/auth/logout` | User logout |
| `GET` | `/api/v1/auth/status` | Authentication status |
| `GET` | `/api/v1/auth/tenants` | User tenants |
| `POST` | `/api/v1/auth/tenants/switch` | Switch tenant |
| `POST` | `/api/v1/auth/tenants` | Create tenant |
| `PUT` | `/api/v1/auth/users/me` | Update user |
| `POST` | `/api/v1/auth/api-keys` | Create API key |
| `GET` | `/api/v1/auth/roles` | Get roles |
| `GET` | `/api/v1/auth/permissions` | Get permissions |

### **Request/Response Examples**

#### **Login Request**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "tenant_id": "optional-tenant-id"
}
```

#### **Login Response**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "rt_abc123...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "admin",
    "permissions": ["view_analytics", "manage_users"]
  },
  "tenant": {
    "id": "tenant-uuid",
    "name": "Example Corp",
    "subscription_tier": "enterprise"
  }
}
```

## 🗄️ **Database Schema**

### **Tables Overview**

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `users` | User accounts | id, email, password, role |
| `tenants` | Organizations | id, name, slug, tier |
| `tenant_memberships` | User-tenant relationships | user_id, tenant_id, role |
| `user_sessions` | Active sessions | user_id, token_hash, expires_at |
| `api_keys` | Programmatic access | user_id, key_hash, permissions |
| `password_resets` | Password recovery | user_id, token_hash, expires_at |

### **Relationships**

```
users (1) ←→ (many) tenant_memberships (many) ←→ (1) tenants
users (1) ←→ (many) user_sessions
users (1) ←→ (many) api_keys
users (1) ←→ (many) password_resets
```

## 🔒 **Security Features**

### **Password Security**
- **Bcrypt Hashing**: Secure password storage with salt
- **Minimum Length**: 8 characters required
- **Password Reset**: Secure token-based reset flow

### **Token Security**
- **JWT Tokens**: Signed with secret key
- **Token Expiration**: Configurable expiry times
- **Refresh Tokens**: Secure token renewal
- **Token Invalidation**: Logout removes tokens

### **Session Security**
- **IP Tracking**: Store client IP addresses
- **User Agent**: Track browser information
- **Session Limits**: Maximum sessions per user
- **Automatic Cleanup**: Expired session removal

### **API Security**
- **Rate Limiting**: Prevent abuse
- **CORS Configuration**: Cross-origin restrictions
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM

## 🧪 **Testing**

### **Integration Testing**

Run the authentication integration tests:

```bash
# From the backend directory
python scripts/test_auth_integration.py
```

### **Manual Testing**

1. **Start the backend**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Create database tables**:
   ```bash
   python scripts/create_auth_tables.py
   ```

3. **Test login with default admin**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@xreason.com", "password": "admin123"}'
   ```

### **Frontend Testing**

1. **Start the frontend**:
   ```bash
   cd frontend
   npm start
   ```

2. **Navigate to login page**:
   - Go to `http://localhost:3000/login`
   - Use credentials: `admin@xreason.com` / `admin123`

3. **Test authentication flow**:
   - Login should redirect to dashboard
   - Protected routes should work
   - Logout should clear session

## 🚀 **Deployment**

### **Environment Variables**

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/xreason

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenAI (for reasoning features)
OPENAI_API_KEY=your-openai-api-key
```

### **Database Setup**

1. **Create PostgreSQL database**:
   ```sql
   CREATE DATABASE xreason;
   CREATE USER xreason WITH PASSWORD 'xreason';
   GRANT ALL PRIVILEGES ON DATABASE xreason TO xreason;
   ```

2. **Run migrations**:
   ```bash
   python scripts/create_auth_tables.py
   ```

### **Production Considerations**

- **Secret Key**: Use a strong, random secret key
- **HTTPS**: Always use HTTPS in production
- **CORS**: Configure CORS for your domain
- **Rate Limiting**: Implement rate limiting
- **Monitoring**: Add authentication metrics
- **Backup**: Regular database backups

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. Database Connection Errors**
```
Error: (psycopg2.OperationalError) connection to server at "localhost" failed
```
**Solution**: Check PostgreSQL is running and DATABASE_URL is correct.

#### **2. JWT Token Errors**
```
Error: Invalid token
```
**Solution**: Check SECRET_KEY is set and consistent.

#### **3. CORS Errors**
```
Error: CORS policy: No 'Access-Control-Allow-Origin' header
```
**Solution**: Update CORS settings in backend configuration.

#### **4. Password Hashing Errors**
```
Error: ModuleNotFoundError: No module named 'bcrypt'
```
**Solution**: Install bcrypt: `pip install passlib[bcrypt]`

### **Debug Mode**

Enable debug mode for detailed error messages:

```python
# In backend/app/core/config.py
debug: bool = True
log_level: str = "DEBUG"
```

### **Logging**

Check logs for authentication issues:

```bash
# Backend logs
tail -f backend/logs/app.log

# Frontend logs (browser console)
F12 → Console tab
```

## 📚 **Additional Resources**

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/) - JWT token debugger
- [Bcrypt](https://bcrypt.readthedocs.io/) - Password hashing
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/) - Database ORM

## 🤝 **Support**

For authentication-related issues:

1. Check the troubleshooting section above
2. Review the integration test output
3. Check backend logs for detailed error messages
4. Verify environment variables are set correctly
5. Ensure database is running and accessible

---

**🎉 Congratulations!** Your authentication system is now fully integrated and ready for production use.
