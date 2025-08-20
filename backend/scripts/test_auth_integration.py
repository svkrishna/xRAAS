#!/usr/bin/env python3
"""
Authentication Integration Test Script
Tests the complete authentication flow from frontend to backend.
"""

import sys
import os
import asyncio
import httpx
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings


class AuthIntegrationTest:
    """Test class for authentication integration."""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.client = httpx.AsyncClient()
        self.access_token = None
        self.refresh_token = None
    
    async def test_health_check(self):
        """Test if the backend is running."""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            if response.status_code == 200:
                print("✅ Backend is running")
                return True
            else:
                print(f"❌ Backend health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Backend connection failed: {e}")
            return False
    
    async def test_registration(self):
        """Test user registration."""
        try:
            register_data = {
                "email": "test@xreason.com",
                "password": "testpassword123",
                "name": "Test User",
                "tenant_name": "Test Organization",
                "tenant_slug": "test-org"
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/auth/register",
                json=register_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                print("✅ User registration successful")
                return True
            else:
                print(f"❌ Registration failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Registration test failed: {e}")
            return False
    
    async def test_login(self):
        """Test user login."""
        try:
            login_data = {
                "email": "admin@xreason.com",
                "password": "admin123"
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/auth/login",
                json=login_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                print("✅ User login successful")
                return True
            else:
                print(f"❌ Login failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login test failed: {e}")
            return False
    
    async def test_auth_status(self):
        """Test authentication status endpoint."""
        try:
            if not self.access_token:
                print("❌ No access token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.get(
                f"{self.base_url}/api/v1/auth/status",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Auth status successful - User: {data['user']['name']}")
                return True
            else:
                print(f"❌ Auth status failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Auth status test failed: {e}")
            return False
    
    async def test_tenants(self):
        """Test tenant listing endpoint."""
        try:
            if not self.access_token:
                print("❌ No access token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.get(
                f"{self.base_url}/api/v1/auth/tenants",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                tenant_count = len(data["tenants"])
                print(f"✅ Tenants retrieved successfully - {tenant_count} tenants")
                return True
            else:
                print(f"❌ Tenants retrieval failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Tenants test failed: {e}")
            return False
    
    async def test_token_refresh(self):
        """Test token refresh endpoint."""
        try:
            if not self.refresh_token:
                print("❌ No refresh token available")
                return False
            
            refresh_data = {"refresh_token": self.refresh_token}
            response = await self.client.post(
                f"{self.base_url}/api/v1/auth/refresh",
                json=refresh_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                print("✅ Token refresh successful")
                return True
            else:
                print(f"❌ Token refresh failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Token refresh test failed: {e}")
            return False
    
    async def test_logout(self):
        """Test logout endpoint."""
        try:
            if not self.access_token:
                print("❌ No access token available")
                return False
            
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await self.client.post(
                f"{self.base_url}/api/v1/auth/logout",
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ Logout successful")
                return True
            else:
                print(f"❌ Logout failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Logout test failed: {e}")
            return False
    
    async def test_roles_permissions(self):
        """Test roles and permissions endpoints."""
        try:
            # Test roles endpoint
            response = await self.client.get(f"{self.base_url}/api/v1/auth/roles")
            if response.status_code == 200:
                data = response.json()
                role_count = len(data)
                print(f"✅ Roles retrieved successfully - {role_count} roles")
            else:
                print(f"❌ Roles retrieval failed: {response.status_code}")
                return False
            
            # Test permissions endpoint
            response = await self.client.get(f"{self.base_url}/api/v1/auth/permissions")
            if response.status_code == 200:
                data = response.json()
                group_count = len(data)
                print(f"✅ Permissions retrieved successfully - {group_count} groups")
                return True
            else:
                print(f"❌ Permissions retrieval failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Roles/permissions test failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all authentication integration tests."""
        print("🚀 Starting Authentication Integration Tests...")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Roles & Permissions", self.test_roles_permissions),
            ("Admin Login", self.test_login),
            ("Auth Status", self.test_auth_status),
            ("Tenants", self.test_tenants),
            ("Token Refresh", self.test_token_refresh),
            ("User Registration", self.test_registration),
            ("Logout", self.test_logout),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🧪 Running {test_name}...")
            try:
                result = await test_func()
                if result:
                    passed += 1
                else:
                    print(f"❌ {test_name} failed")
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {e}")
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All authentication integration tests passed!")
            return True
        else:
            print("⚠️  Some tests failed. Check the output above.")
            return False
    
    async def cleanup(self):
        """Clean up resources."""
        await self.client.aclose()


async def main():
    """Main test function."""
    tester = AuthIntegrationTest()
    
    try:
        success = await tester.run_all_tests()
        if success:
            print("\n✅ Authentication integration is working correctly!")
            sys.exit(0)
        else:
            print("\n❌ Authentication integration has issues!")
            sys.exit(1)
    finally:
        await tester.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
