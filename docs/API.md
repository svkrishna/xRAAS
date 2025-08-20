# XReason API Documentation

## Overview

XReason is a Reasoning as a Service (RaaS) platform that combines LLM intuition (System 1) with symbolic/rule-based checks (System 2) to provide explainable, validated answers.

## Base URL

- Development: `http://localhost:8000`
- Production: `https://api.xreason.com` (when deployed)

## Authentication

Currently, the API does not require authentication for the MVP. In production, this will be implemented using JWT tokens.

## Endpoints

### 1. Health Check

#### GET /health/

Basic health check endpoint.

**Response:**
```json
{
  "success": true,
  "message": "XReason API is healthy",
  "data": {
    "status": "healthy",
    "timestamp": 1640995200.0,
    "version": "1.0.0",
    "app_name": "XReason API"
  }
}
```

#### GET /health/detailed

Detailed health check with component status.

**Response:**
```json
{
  "success": true,
  "message": "All components are healthy",
  "data": {
    "status": "healthy",
    "timestamp": 1640995200.0,
    "version": "1.0.0",
    "components": {
      "llm_service": {
        "status": "healthy",
        "model": "gpt-4o"
      },
      "symbolic_service": {
        "status": "healthy",
        "rule_sets": ["healthcare", "finance", "general"]
      },
      "knowledge_service": {
        "status": "healthy",
        "facts_count": 15
      }
    }
  }
}
```

### 2. Reasoning

#### POST /api/v1/reason/

Main reasoning endpoint that orchestrates the complete reasoning pipeline.

**Request Body:**
```json
{
  "question": "Is this access request compliant with HIPAA 164.312(a)(1)?",
  "context": "A nurse is requesting access to patient records through the electronic health system.",
  "domain": "healthcare",
  "confidence_threshold": 0.7,
  "max_steps": 10
}
```

**Parameters:**
- `question` (required): The question to reason about
- `context` (optional): Additional context or background information
- `domain` (optional): Domain context ("healthcare", "finance", "general")
- `confidence_threshold` (optional): Minimum confidence threshold (0-1, default: 0.7)
- `max_steps` (optional): Maximum reasoning steps (default: 10)

**Response:**
```json
{
  "answer": "Based on the analysis, this access request appears to be compliant with HIPAA 164.312(a)(1)...",
  "reasoning_trace": [
    {
      "stage": "LLM Hypothesis",
      "output": "The LLM generated initial analysis...",
      "confidence": 0.8,
      "metadata": {
        "model": "gpt-4o",
        "tokens_used": 150,
        "domain": "healthcare"
      }
    },
    {
      "stage": "Rule Check",
      "output": "Applied 3 HIPAA rules, passed 2/3...",
      "confidence": 0.7,
      "metadata": {
        "domain": "healthcare",
        "rule_set": "HIPAA Compliance Rules",
        "results": [...]
      }
    },
    {
      "stage": "Knowledge Graph",
      "output": "Verified hypothesis against 5 relevant facts...",
      "confidence": 0.9,
      "metadata": {
        "domain": "healthcare",
        "facts_checked": 5,
        "verification_results": [...]
      }
    },
    {
      "stage": "Validation",
      "output": "Final validation confirms the answer is consistent...",
      "confidence": 0.85,
      "metadata": {
        "model": "gpt-4o",
        "validation_result": "..."
      }
    }
  ],
  "confidence": 0.75,
  "domain": "healthcare",
  "metadata": {
    "processing_time": 1.2,
    "session_id": "uuid-here",
    "steps_completed": 4
  }
}
```

### 3. Rules

#### GET /api/v1/reason/rules

Get available rule sets.

**Query Parameters:**
- `domain` (optional): Filter by domain ("healthcare", "finance", "general")

**Response:**
```json
{
  "success": true,
  "message": "Rule sets retrieved successfully",
  "data": {
    "rule_sets": {
      "healthcare": {
        "name": "HIPAA Compliance Rules",
        "description": "Rules for HIPAA compliance checking",
        "rules": [...]
      },
      "finance": {
        "name": "Financial Calculation Rules",
        "description": "Rules for financial calculations and validations",
        "rules": [...]
      }
    },
    "available_domains": ["healthcare", "finance", "general"]
  }
}
```

### 4. Knowledge

#### GET /api/v1/reason/knowledge

Get knowledge base summary.

**Query Parameters:**
- `domain` (optional): Filter by domain

**Response:**
```json
{
  "success": true,
  "message": "Knowledge summary retrieved successfully",
  "data": {
    "total_facts": 15,
    "domains": ["healthcare", "finance", "general"],
    "graph_nodes": 20,
    "graph_edges": 25
  }
}
```

### 5. Capabilities

#### GET /api/v1/reason/capabilities

Get reasoning capabilities summary.

**Query Parameters:**
- `domain` (optional): Filter by domain

**Response:**
```json
{
  "success": true,
  "message": "Capabilities retrieved successfully",
  "data": {
    "llm_model": "gpt-4o",
    "available_rule_sets": ["healthcare", "finance", "general"],
    "knowledge_summary": {
      "total_facts": 15,
      "domains": ["healthcare", "finance", "general"]
    },
    "max_reasoning_steps": 10,
    "confidence_threshold": 0.7
  }
}
```

### 6. Validation

#### POST /api/v1/reason/validate

Validate a reasoning request without executing it.

**Request Body:** Same as the main reasoning endpoint

**Response:**
```json
{
  "success": true,
  "message": "Request validation completed",
  "data": {
    "valid": true,
    "issues": [],
    "warnings": ["Question is quite short"]
  }
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message",
  "detail": "Additional error details"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

Currently, there are no rate limits implemented for the MVP. In production, rate limiting will be added based on API keys.

## Examples

### Healthcare Example

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/reason/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Is this access request compliant with HIPAA 164.312(a)(1)?",
    "context": "A nurse is requesting access to patient records through the electronic health system.",
    "domain": "healthcare"
  }'
```

### Finance Example

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/reason/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "If debt=100, equity=50, what is Debt-to-Equity ratio?",
    "context": "Financial analysis for company XYZ",
    "domain": "finance"
  }'
```

## SDKs and Libraries

### Python

```python
import requests

def reason(question, context=None, domain=None):
    response = requests.post(
        "http://localhost:8000/api/v1/reason/",
        json={
            "question": question,
            "context": context,
            "domain": domain
        }
    )
    return response.json()

# Example usage
result = reason(
    question="Is this HIPAA compliant?",
    context="Access request for patient records",
    domain="healthcare"
)
print(result["answer"])
```

### JavaScript/TypeScript

```typescript
interface ReasoningRequest {
  question: string;
  context?: string;
  domain?: string;
}

async function reason(request: ReasoningRequest) {
  const response = await fetch("http://localhost:8000/api/v1/reason/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });
  return response.json();
}

// Example usage
const result = await reason({
  question: "Is this HIPAA compliant?",
  context: "Access request for patient records",
  domain: "healthcare",
});
console.log(result.answer);
```

## Support

For support and questions:
- GitHub Issues: [https://github.com/xreason/xreason/issues](https://github.com/xreason/xreason/issues)
- Documentation: [https://docs.xreason.com](https://docs.xreason.com)
- Email: support@xreason.com
