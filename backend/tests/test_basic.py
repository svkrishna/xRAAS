"""
Basic tests for the XReason backend.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "XReason API is healthy" in data["message"]


def test_detailed_health_check():
    """Test the detailed health check endpoint."""
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "components" in data["data"]


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "XReason" in data["message"]


def test_info_endpoint():
    """Test the info endpoint."""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["app_name"] == "XReason API"
    assert "features" in data


def test_reasoning_endpoint_structure():
    """Test the reasoning endpoint structure (without actual reasoning)."""
    # This test would require mocking the OpenAI API
    # For now, just test the endpoint exists
    response = client.post("/api/v1/reason/", json={
        "question": "test question"
    })
    # Should return 400 or 500 depending on OpenAI API availability
    assert response.status_code in [400, 500]


def test_rules_endpoint():
    """Test the rules endpoint."""
    response = client.get("/api/v1/reason/rules")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "rule_sets" in data["data"]


def test_knowledge_endpoint():
    """Test the knowledge endpoint."""
    response = client.get("/api/v1/reason/knowledge")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "total_facts" in data["data"]


def test_capabilities_endpoint():
    """Test the capabilities endpoint."""
    response = client.get("/api/v1/reason/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "llm_model" in data["data"]


if __name__ == "__main__":
    pytest.main([__file__])
