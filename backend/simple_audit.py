#!/usr/bin/env python3
"""
Simple XReason Audit - Basic Structure Check
Checks only file structure and core imports without loading services.
"""

import os
import sys

def check_file_exists(file_path):
    """Check if a file exists."""
    if os.path.exists(file_path):
        print(f"✅ {file_path}")
        return True
    else:
        print(f"❌ {file_path} - MISSING")
        return False

def main():
    print("🔍 XReason Simple Audit - File Structure Check")
    print("=" * 50)
    
    issues = 0
    
    # Check critical files
    critical_files = [
        "app/main.py",
        "app/__init__.py", 
        "app/core/config.py",
        "app/models/__init__.py",
        "app/models/base.py",
        "app/models/auth.py",
        "app/services/__init__.py",
        "app/api/__init__.py",
        "app/api/health.py",
        "app/api/reasoning.py",
        "app/schemas/__init__.py",
        "app/schemas/auth.py",
        "app/schemas/agent.py",
        "app/schemas/reasoning.py",
        "app/schemas/financial.py",
        "app/pilots/__init__.py",
        "app/security/__init__.py",
        "app/reliability/__init__.py",
        "app/billing/__init__.py",
        "app/marketplace/__init__.py",
        "requirements.txt",
        "Dockerfile"
    ]
    
    print("\n📁 Checking File Structure:")
    for file_path in critical_files:
        if not check_file_exists(file_path):
            issues += 1
    
    # Check directory structure
    print("\n📁 Checking Directory Structure:")
    critical_dirs = [
        "app",
        "app/core",
        "app/models", 
        "app/services",
        "app/api",
        "app/schemas",
        "app/pilots",
        "app/security",
        "app/reliability",
        "app/billing",
        "app/marketplace",
        "app/rulesets"
    ]
    
    for dir_path in critical_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - MISSING")
            issues += 1
    
    # Check basic imports (without services)
    print("\n🔍 Checking Basic Imports:")
    try:
        import fastapi
        print("✅ fastapi")
    except ImportError:
        print("❌ fastapi - MISSING")
        issues += 1
    
    try:
        import uvicorn
        print("✅ uvicorn")
    except ImportError:
        print("❌ uvicorn - MISSING")
        issues += 1
    
    try:
        import pydantic
        print("✅ pydantic")
    except ImportError:
        print("❌ pydantic - MISSING")
        issues += 1
    
    try:
        import sqlmodel
        print("✅ sqlmodel")
    except ImportError:
        print("❌ sqlmodel - MISSING")
        issues += 1
    
    # Check core config
    print("\n🔍 Checking Core Configuration:")
    try:
        # Set environment variables for testing
        os.environ["OPENAI_API_KEY"] = "sk-demo-key-for-testing"
        os.environ["SECRET_KEY"] = "dev-secret-key-for-testing-only"
        
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from app.core.config import settings
        print("✅ app.core.config imported successfully")
    except Exception as e:
        print(f"❌ app.core.config import failed: {e}")
        issues += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SIMPLE AUDIT SUMMARY")
    print("=" * 50)
    
    if issues == 0:
        print("\n🎉 All basic components are present!")
        print("✅ XReason has the correct file structure.")
        print("✅ Core dependencies are available.")
        print("✅ Configuration can be loaded.")
        print("\n📝 Note: This audit doesn't test service functionality.")
        print("   Run comprehensive tests for full validation.")
        return True
    else:
        print(f"\n⚠️  Found {issues} structural issues:")
        print("   • Missing files or directories")
        print("   • Import problems")
        print("   • Configuration issues")
        print(f"\n🔧 Please fix these issues before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
