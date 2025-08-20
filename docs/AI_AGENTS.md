# XReason AI Agents

XReason provides advanced AI agent capabilities with intelligent reasoning, knowledge integration, validation, and learning features. The AI agent system is designed to provide sophisticated reasoning capabilities that go beyond simple rule-based systems.

## Overview

The AI agent system consists of specialized agents that work together to provide comprehensive reasoning and analysis capabilities:

- **Reasoning Agent**: Advanced logical reasoning and hypothesis generation
- **Knowledge Agent**: Knowledge integration and discovery
- **Validation Agent**: Fact checking and consistency validation
- **Memory System**: Short-term and long-term memory with pattern recognition
- **Learning System**: Adaptive learning and pattern recognition

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client        │    │   AI Agent      │    │   Backend       │
│   Application   │◄──►│   Service       │◄──►│   Services      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Agent Types    │
                       │                 │
                       │ • Reasoning     │
                       │ • Knowledge     │
                       │ • Validation    │
                       │ • Memory        │
                       │ • Learning      │
                       └─────────────────┘
```

## Agent Types

### 🧠 Reasoning Agent

The reasoning agent provides advanced logical reasoning capabilities:

- **Deductive Reasoning**: Logical conclusions from premises
- **Inductive Reasoning**: Generalizing from specific observations
- **Abductive Reasoning**: Finding the best explanation
- **Analogical Reasoning**: Finding similarities and patterns
- **Causal Reasoning**: Understanding cause-effect relationships

**Capabilities:**
- Hypothesis generation and evaluation
- Multi-strategy reasoning
- Symbolic validation
- Knowledge integration
- Pattern recognition

### 📚 Knowledge Agent

The knowledge agent manages knowledge integration and discovery:

- **Knowledge Discovery**: Finding relevant information
- **Knowledge Validation**: Ensuring consistency and accuracy
- **Knowledge Synthesis**: Combining information coherently
- **Knowledge Graph Updates**: Maintaining knowledge base

**Capabilities:**
- Entity extraction and relationship mapping
- Pattern discovery in data
- Knowledge consistency checking
- Automated knowledge graph updates

### ✅ Validation Agent

The validation agent provides comprehensive validation capabilities:

- **Logical Validation**: Checking logical consistency
- **Factual Validation**: Verifying factual accuracy
- **Consistency Validation**: Ensuring internal consistency
- **Error Detection**: Identifying potential issues

**Capabilities:**
- Multi-level validation (logical, factual, consistency)
- Claim extraction and verification
- Knowledge-based fact checking
- Confidence scoring

## Quick Start

### Using the API

```bash
# Create a session
curl -X POST "http://localhost:8000/api/v1/agents/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "domain": "general",
    "metadata": {"purpose": "analysis"}
  }'

# Process with reasoning agent
curl -X POST "http://localhost:8000/api/v1/agents/reasoning" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your_session_id",
    "input_data": {
      "question": "What is the profit margin if revenue is $1M and costs are $600K?",
      "context": "Financial analysis"
    },
    "priority": "high"
  }'
```

### Using Python

```python
import httpx
import asyncio

async def ai_agent_example():
    async with httpx.AsyncClient() as client:
        # Create session
        session_response = await client.post(
            "http://localhost:8000/api/v1/agents/sessions",
            json={
                "user_id": "user_001",
                "domain": "general"
            }
        )
        session_id = session_response.json()["session_id"]
        
        # Process with reasoning agent
        reasoning_response = await client.post(
            "http://localhost:8000/api/v1/agents/reasoning",
            json={
                "session_id": session_id,
                "input_data": {
                    "question": "Analyze the financial health of this company",
                    "context": "Business analysis"
                }
            }
        )
        
        result = reasoning_response.json()
        print(f"Success: {result['success']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Reasoning: {result['reasoning']}")

asyncio.run(ai_agent_example())
```

## API Reference

### Session Management

#### Create Session
```http
POST /api/v1/agents/sessions
```

**Request:**
```json
{
  "user_id": "string",
  "domain": "string",
  "agent_type": "reasoning_agent",
  "metadata": {}
}
```

**Response:**
```json
{
  "session_id": "uuid"
}
```

#### Get Session Info
```http
GET /api/v1/agents/sessions/{session_id}
```

**Response:**
```json
{
  "session_id": "string",
  "user_id": "string",
  "domain": "string",
  "created_at": "datetime",
  "last_activity": "datetime",
  "status": "string",
  "task_count": 0,
  "agent_status": []
}
```

### Agent Processing

#### General Processing
```http
POST /api/v1/agents/process
```

**Request:**
```json
{
  "session_id": "string",
  "input_data": {},
  "agent_types": ["reasoning_agent"],
  "priority": "medium",
  "metadata": {}
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "string",
  "task_id": "string",
  "result": {},
  "confidence": 0.85,
  "reasoning": "string",
  "processing_time": 1.2,
  "agent_used": "reasoning_001",
  "metadata": {},
  "timestamp": "datetime"
}
```

#### Reasoning Agent
```http
POST /api/v1/agents/reasoning
```

#### Knowledge Agent
```http
POST /api/v1/agents/knowledge-integration
```

#### Validation Agent
```http
POST /api/v1/agents/validation
```

### Memory Operations

#### Memory Operations
```http
POST /api/v1/agents/memory
```

**Request:**
```json
{
  "session_id": "string",
  "memory_type": "long_term",
  "key": "string",
  "value": {},
  "operation": "set"
}
```

**Operations:**
- `get`: Retrieve memory
- `set`: Store memory
- `delete`: Remove memory

### Learning Operations

#### Learning Operations
```http
POST /api/v1/agents/learning
```

**Request:**
```json
{
  "session_id": "string",
  "learning_type": "pattern",
  "input_data": {},
  "feedback": {},
  "adaptation_target": "string"
}
```

**Learning Types:**
- `pattern`: Pattern recognition
- `behavior`: Behavior learning
- `strategy`: Strategy learning

### Knowledge Integration

#### Knowledge Operations
```http
POST /api/v1/agents/knowledge
```

**Request:**
```json
{
  "session_id": "string",
  "knowledge_type": "fact",
  "content": {},
  "source": "string",
  "confidence": 0.95,
  "operation": "add"
}
```

**Operations:**
- `add`: Add knowledge
- `query`: Query knowledge
- `update`: Update knowledge
- `delete`: Delete knowledge

### System Monitoring

#### System Status
```http
GET /api/v1/agents/status
```

**Response:**
```json
{
  "total_agents": 3,
  "active_agents": 3,
  "total_sessions": 10,
  "active_sessions": 5,
  "total_tasks": 150,
  "completed_tasks": 145,
  "failed_tasks": 5,
  "avg_processing_time": 1.2,
  "system_health": "healthy",
  "agent_statuses": [],
  "performance_metrics": []
}
```

#### Agent Status
```http
GET /api/v1/agents/agents
```

#### Health Check
```http
GET /api/v1/agents/health
```

## Advanced Features

### Memory System

The AI agents use a sophisticated memory system:

#### Short-term Memory
- Limited capacity (configurable)
- Fast access
- Automatic cleanup
- Pattern tracking

#### Long-term Memory
- Persistent storage
- Structured knowledge
- Relationship mapping
- Confidence scoring

#### Pattern Recognition
- Frequency tracking
- Temporal patterns
- Success rate monitoring
- Adaptive learning

### Learning Capabilities

#### Pattern Learning
```python
# Learn from successful patterns
learning_request = {
    "session_id": session_id,
    "learning_type": "pattern",
    "input_data": {
        "pattern": "financial_analysis",
        "input": "revenue and costs",
        "output": "profit margin",
        "success": True
    },
    "feedback": {
        "accuracy": 0.9,
        "usefulness": 0.85
    }
}
```

#### Behavior Learning
- Adaptive response patterns
- Success rate optimization
- Strategy refinement
- Performance improvement

### Knowledge Integration

#### Fact Management
```python
# Add factual knowledge
knowledge_request = {
    "session_id": session_id,
    "knowledge_type": "fact",
    "content": {
        "subject": "artificial intelligence",
        "predicate": "is",
        "object": "a branch of computer science",
        "confidence": 0.95,
        "source": "academic"
    },
    "operation": "add"
}
```

#### Rule Management
```python
# Add reasoning rules
rule_request = {
    "session_id": session_id,
    "knowledge_type": "rule",
    "content": {
        "condition": "if revenue > costs",
        "conclusion": "then profit = revenue - costs",
        "confidence": 0.9
    },
    "operation": "add"
}
```

## Use Cases

### Financial Analysis
```python
# Complex financial reasoning
financial_analysis = {
    "session_id": session_id,
    "input_data": {
        "question": "What is the debt-to-equity ratio and what does it indicate?",
        "context": {
            "total_debt": 500000,
            "total_equity": 1000000,
            "industry": "technology"
        }
    },
    "agent_types": ["reasoning_agent", "validation_agent"]
}
```

### Scientific Validation
```python
# Validate scientific claims
scientific_validation = {
    "session_id": session_id,
    "input_data": {
        "statement": "The study shows a 95% confidence interval",
        "context": "statistical analysis",
        "data": {
            "sample_size": 100,
            "p_value": 0.03,
            "effect_size": 0.5
        }
    },
    "agent_types": ["validation_agent", "reasoning_agent"]
}
```

### Knowledge Discovery
```python
# Discover new knowledge patterns
knowledge_discovery = {
    "session_id": session_id,
    "input_data": {
        "topic": "machine learning algorithms",
        "query": "What are the emerging trends in deep learning?",
        "context": "research analysis"
    },
    "agent_types": ["knowledge_agent", "reasoning_agent"]
}
```

## Performance Monitoring

### Metrics

The AI agent system provides comprehensive metrics:

- **Processing Time**: Average response times per agent
- **Success Rate**: Task completion success rates
- **Confidence Scores**: Average confidence levels
- **Memory Usage**: Memory utilization patterns
- **Learning Progress**: Adaptation and improvement rates

### Monitoring Endpoints

```bash
# Get system metrics
curl http://localhost:8000/api/v1/agents/status

# Get agent performance
curl http://localhost:8000/api/v1/agents/agents

# Health check
curl http://localhost:8000/api/v1/agents/health
```

### Grafana Dashboards

View detailed metrics at: http://localhost:3002 (Grafana)

- Agent performance dashboards
- Session monitoring
- Memory utilization
- Learning progress
- System health indicators

## Configuration

### Agent Configuration

```python
# Agent capabilities can be configured
agent_config = {
    "reasoning_agent": {
        "max_hypotheses": 5,
        "confidence_threshold": 0.7,
        "reasoning_strategies": ["deductive", "inductive", "abductive"]
    },
    "knowledge_agent": {
        "max_knowledge_items": 1000,
        "validation_threshold": 0.8,
        "update_frequency": "real_time"
    },
    "validation_agent": {
        "validation_levels": ["logical", "factual", "consistency"],
        "confidence_threshold": 0.75
    }
}
```

### Memory Configuration

```python
# Memory system configuration
memory_config = {
    "short_term": {
        "max_size": 1000,
        "ttl": 3600,  # 1 hour
        "cleanup_interval": 300  # 5 minutes
    },
    "long_term": {
        "max_size": 10000,
        "persistence": True,
        "backup_interval": 86400  # 24 hours
    }
}
```

## Best Practices

### Session Management
- Create sessions for related tasks
- Reuse sessions for continuous learning
- Monitor session activity
- Clean up inactive sessions

### Agent Selection
- Use reasoning agent for complex analysis
- Use knowledge agent for information discovery
- Use validation agent for fact checking
- Combine agents for comprehensive analysis

### Memory Usage
- Store important patterns in long-term memory
- Use short-term memory for temporary data
- Monitor memory usage patterns
- Clean up unused memory

### Learning Optimization
- Provide regular feedback
- Monitor learning progress
- Adjust learning parameters
- Validate learning outcomes

## Troubleshooting

### Common Issues

#### Agent Not Responding
```bash
# Check agent health
curl http://localhost:8000/api/v1/agents/health

# Check system status
curl http://localhost:8000/api/v1/agents/status

# Check logs
docker-compose logs backend
```

#### Low Confidence Scores
- Check input data quality
- Verify knowledge base
- Review validation results
- Adjust confidence thresholds

#### Memory Issues
- Monitor memory usage
- Clean up old sessions
- Adjust memory limits
- Check for memory leaks

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Tuning

- Adjust agent timeouts
- Optimize memory usage
- Configure caching
- Monitor resource usage

## Support

For questions or issues with AI agents:

- Check the API documentation at http://localhost:8000/docs
- Review the demo examples
- Check the logs: `docker-compose logs backend`
- Monitor metrics at http://localhost:3002
- Run the AI agent demo: `./scripts/run-ai-agent-demo.sh`
