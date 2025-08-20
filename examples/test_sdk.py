#!/usr/bin/env python3
"""
Simple test script to verify XReason SDK installation
"""

import asyncio
import sys

def test_imports():
    """Test that all SDK modules can be imported."""
    try:
        from xreason_sdk import XReasonClient
        from xreason_sdk import (
            ReasoningRequest, ReasoningResponse,
            LegalAnalysisRequest, LegalAnalysisResponse,
            ScientificAnalysisRequest, ScientificAnalysisResponse
        )
        from xreason_sdk import XReasonError, XReasonAPIError
        print("✅ All SDK imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

async def test_client_creation():
    """Test that the client can be created."""
    try:
        from xreason_sdk import XReasonClient
        
        client = XReasonClient("http://localhost:8000")
        print("✅ Client creation successful!")
        return True
    except Exception as e:
        print(f"❌ Client creation error: {e}")
        return False

async def test_health_check():
    """Test health check endpoint (requires running server)."""
    try:
        from xreason_sdk import XReasonClient
        
        async with XReasonClient("http://localhost:8000") as client:
            health = await client.health_check()
            print(f"✅ Health check successful: {health.get('status', 'unknown')}")
            return True
    except Exception as e:
        print(f"⚠️ Health check failed (server may not be running): {e}")
        return False

async def main():
    """Run all tests."""
    print("🧪 Testing XReason SDK Installation")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("❌ SDK installation test failed!")
        sys.exit(1)
    
    # Test client creation
    if not await test_client_creation():
        print("❌ Client creation test failed!")
        sys.exit(1)
    
    # Test health check (optional)
    await test_health_check()
    
    print("\n✅ SDK installation test completed successfully!")
    print("\n🎯 Next steps:")
    print("   1. Start the services: ./scripts/start-xreason.sh")
    print("   2. Run the full demo: python examples/pilot_demo.py")

if __name__ == "__main__":
    asyncio.run(main())
