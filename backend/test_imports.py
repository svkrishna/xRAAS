#!/usr/bin/env python3
"""
Test script to verify all imports work correctly.
"""

import os
import sys

# Set required environment variables
os.environ["OPENAI_API_KEY"] = "sk-demo-key-for-testing"
os.environ["SECRET_KEY"] = "dev-secret-key-for-testing-only"

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all module imports."""
    try:
        print("Testing marketplace imports...")
        from app.marketplace import PartnerRegistry, CertificationManager, MarketplaceAPI
        print("✅ All marketplace modules imported successfully")
        
        print("Testing billing imports...")
        from app.billing import UsageMeter, BillingService, QuotaManager
        print("✅ All billing modules imported successfully")
        
        print("Testing auth imports...")
        from app.api.auth import router as auth_router
        print("✅ Auth router imported successfully")
        
        print("Testing security imports...")
        from app.security.audit_logger import audit_logger
        print("✅ Security modules imported successfully")
        
        print("Testing commercial imports...")
        from app.api.commercial import router as commercial_router
        print("✅ Commercial modules imported successfully")
        
        print("\n🎉 All imports successful! The backend integration is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
