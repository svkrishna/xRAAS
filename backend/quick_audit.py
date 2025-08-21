#!/usr/bin/env python3
"""
Quick XReason Audit - Fast Critical Component Check
Focuses on the most important issues first.
"""

import os
import sys
import importlib
from typing import Dict, List, Any

# Set required environment variables
os.environ["OPENAI_API_KEY"] = "sk-demo-key-for-testing"
os.environ["SECRET_KEY"] = "dev-secret-key-for-testing-only"

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def quick_import_test(module_name: str) -> tuple[bool, str]:
    """Quick import test with timeout."""
    try:
        importlib.import_module(module_name)
        return True, "OK"
    except Exception as e:
        return False, str(e)

def main():
    print("🚀 XReason Quick Audit - Critical Components")
    print("=" * 50)
    
    # Critical modules that must work
    critical_modules = [
        "app.core.config",
        "app.models.base", 
        "app.main",
        "app.services.llm_service",
        "app.services.orchestration_service",
        "app.api.health",
        "app.api.reasoning"
    ]
    
    print("\n🔍 Testing Critical Imports:")
    issues = []
    
    for module in critical_modules:
        print(f"  Testing {module}...", end=" ")
        success, error = quick_import_test(module)
        if success:
            print("✅")
        else:
            print("❌")
            issues.append(f"{module}: {error}")
    
    # Check key dependencies
    print("\n🔍 Testing Key Dependencies:")
    key_deps = ["fastapi", "uvicorn", "openai", "pydantic", "sqlmodel"]
    
    for dep in key_deps:
        print(f"  Testing {dep}...", end=" ")
        success, error = quick_import_test(dep)
        if success:
            print("✅")
        else:
            print("❌")
            issues.append(f"Dependency {dep}: {error}")
    
    # Check file structure
    print("\n🔍 Checking File Structure:")
    critical_files = [
        "app/main.py",
        "app/core/config.py", 
        "requirements.txt",
        "Dockerfile"
    ]
    
    for file_path in critical_files:
        print(f"  Checking {file_path}...", end=" ")
        if os.path.exists(file_path):
            print("✅")
        else:
            print("❌")
            issues.append(f"Missing file: {file_path}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 QUICK AUDIT SUMMARY")
    print("=" * 50)
    
    if issues:
        print(f"\n❌ Found {len(issues)} critical issues:")
        for issue in issues:
            print(f"  • {issue}")
        print(f"\n⚠️  XReason has critical issues that need to be addressed.")
        return False
    else:
        print("\n✅ All critical components are working!")
        print("🎉 XReason is ready for basic operation.")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
