# Graph Persistence Documentation

## Overview

The Graph Persistence feature provides comprehensive save/load functionality for XReason's Knowledge Graphs, supporting both JSON and Neo4j storage formats. This enables persistent storage, sharing, and analysis of complex knowledge graphs across different domains.

## Features

### ✅ Core Functionality
- **JSON Persistence**: Save/load graphs to/from JSON files with metadata
- **Neo4j Integration**: Optional Neo4j database storage for enterprise use
- **Graph Operations**: Full graph querying and analysis after persistence
- **Multiple Export Formats**: JSON, CSV (nodes/edges), and custom formats
- **REST API**: Complete RESTful API for graph persistence operations
- **Statistics & Analytics**: Comprehensive graph analysis and metrics

### ✅ Advanced Capabilities
- **Metadata Preservation**: Timestamps, versioning, and descriptive information
- **Graph Validation**: Integrity checks during save/load operations
- **Bulk Operations**: List, delete, and manage multiple graphs
- **File Management**: Automatic directory creation and cleanup
- **Error Handling**: Robust error handling and recovery

## Architecture

### Components

1. **GraphPersistenceManager**: Core JSON persistence operations
2. **Neo4jPersistenceManager**: Neo4j database integration
3. **GraphPersistenceService**: High-level service orchestrating both storage types
4. **REST API**: FastAPI endpoints for web-based operations

### Data Flow

```
Knowledge Graph → Persistence Service → JSON/Neo4j Storage
                ↓
            Graph Operations (Query, Path Finding, Analysis)
                ↓
            Export Formats (JSON, CSV, Custom)
```

## Usage Examples

### Basic JSON Persistence

```python
from app.services.graph_persistence import create_persistence_service
from app.services.modern_reasoning_service import KnowledgeGraph, GraphNode, GraphEdge

# Create persistence service
persistence_service = create_persistence_service("./data/graphs")

# Create a graph
graph = KnowledgeGraph()
# ... add nodes and edges ...

# Save graph
results = persistence_service.save_graph(graph, "my_graph.json")
print(f"Saved to: {results}")

# Load graph
loaded_graph = persistence_service.load_graph(source="json", filepath="my_graph.json")
print(f"Loaded graph with {len(loaded_graph.nodes)} nodes")
```

### Neo4j Persistence

```python
# Initialize with Neo4j
persistence_service = create_persistence_service(
    json_storage_dir="./data/graphs",
    neo4j_uri="bolt://localhost:7687",
    neo4j_username="neo4j",
    neo4j_password="password"
)

# Save to both JSON and Neo4j
results = persistence_service.save_graph(
    graph, 
    filename="enterprise_graph.json",
    save_to_neo4j=True,
    neo4j_graph_name="enterprise_knowledge_graph"
)

# Load from Neo4j
neo4j_graph = persistence_service.load_graph(
    source="neo4j",
    neo4j_graph_name="enterprise_knowledge_graph"
)
```

### REST API Usage

```bash
# Save a graph
curl -X POST "http://localhost:8000/api/v1/graphs/save" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "compliance_graph.json",
    "save_to_neo4j": false,
    "graph_data": {
      "nodes": [...],
      "edges": [...]
    }
  }'

# List available graphs
curl -X GET "http://localhost:8000/api/v1/graphs/list"

# Load a graph
curl -X POST "http://localhost:8000/api/v1/graphs/load" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "json",
    "filepath": "compliance_graph.json"
  }'

# Get graph statistics
curl -X GET "http://localhost:8000/api/v1/graphs/stats"
```

## API Endpoints

### Graph Persistence API (`/api/v1/graphs`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/save` | Save graph to JSON/Neo4j |
| POST | `/load` | Load graph from storage |
| GET | `/list` | List available graphs |
| DELETE | `/{source}/{identifier}` | Delete graph |
| POST | `/upload` | Upload graph file |
| GET | `/stats` | Get graph statistics |

### Request/Response Models

#### GraphSaveRequest
```python
{
    "filename": "string",           # Optional custom filename
    "save_to_neo4j": false,         # Whether to save to Neo4j
    "neo4j_graph_name": "string",   # Neo4j graph name
    "description": "string"         # Optional description
}
```

#### GraphLoadRequest
```python
{
    "source": "json",               # "json" or "neo4j"
    "filepath": "string",           # File path (for JSON)
    "neo4j_graph_name": "string"    # Graph name (for Neo4j)
}
```

#### GraphInfo
```python
{
    "filename": "string",
    "filepath": "string",
    "created_at": "string",
    "node_count": 0,
    "edge_count": 0,
    "size_bytes": 0,
    "description": "string"
}
```

## Graph Analysis Features

### Statistics
- **Node Count**: Total number of nodes
- **Edge Count**: Total number of relationships
- **Node Types**: Distribution by node type (regulation, concept, requirement, etc.)
- **Relationship Types**: Distribution by relationship type
- **Graph Density**: Measure of graph connectivity
- **Average Node Degree**: Average connections per node

### Operations
- **Query**: Find relationships for specific nodes
- **Path Finding**: Discover paths between nodes
- **Related Concepts**: Find connected concepts
- **Graph Traversal**: Navigate graph structure

## File Formats

### JSON Format
```json
{
    "metadata": {
        "created_at": "2024-01-01T00:00:00Z",
        "version": "1.0",
        "node_count": 15,
        "edge_count": 20,
        "description": "Compliance Knowledge Graph"
    },
    "nodes": [
        {
            "id": "node_id",
            "label": "Node Label",
            "node_type": "regulation",
            "properties": {},
            "confidence": 1.0
        }
    ],
    "edges": [
        {
            "id": "edge_id",
            "source": "source_node_id",
            "target": "target_node_id",
            "relationship": "requires",
            "properties": {},
            "confidence": 1.0
        }
    ]
}
```

### CSV Export
- **Nodes CSV**: `id,label,type,confidence`
- **Edges CSV**: `source,target,relationship,confidence`

## Configuration

### Environment Variables
```bash
# Neo4j Configuration (Optional)
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Storage Configuration
GRAPH_STORAGE_DIR=./data/graphs
```

### Dependencies
```python
# Required
neo4j==5.15.0          # Neo4j driver
networkx               # Graph operations
pydantic              # Data validation
fastapi               # REST API

# Optional
plotly                # Graph visualization
matplotlib            # Graph plotting
```

## Testing

### Test Scripts
- `test_graph_persistence.py`: Core persistence functionality
- `demo_graph_persistence.py`: Comprehensive demonstration
- `test_graph_api.py`: REST API testing

### Running Tests
```bash
# Core persistence tests
python test_graph_persistence.py

# Comprehensive demo
python demo_graph_persistence.py

# API tests
python test_graph_api.py
```

## Performance Considerations

### JSON Storage
- **Pros**: Simple, portable, human-readable
- **Cons**: Limited for very large graphs
- **Best For**: Development, testing, small to medium graphs

### Neo4j Storage
- **Pros**: Scalable, ACID transactions, advanced queries
- **Cons**: Requires Neo4j database setup
- **Best For**: Production, large graphs, complex queries

### Optimization Tips
- Use appropriate storage type for graph size
- Implement graph compression for large JSON files
- Consider Neo4j for graphs with >10,000 nodes
- Use batch operations for multiple graphs

## Security Considerations

### Data Protection
- Encrypt sensitive graph data
- Implement access controls for graph storage
- Validate graph data during import
- Audit graph access and modifications

### Neo4j Security
- Use secure Neo4j connections (TLS)
- Implement proper authentication
- Regular security updates
- Network isolation for production

## Troubleshooting

### Common Issues

1. **Node Count Mismatch**
   - Ensure graph is cleared before loading
   - Check for duplicate node IDs
   - Verify JSON format integrity

2. **Neo4j Connection Issues**
   - Verify Neo4j server is running
   - Check connection credentials
   - Ensure Neo4j driver is installed

3. **File Permission Errors**
   - Check directory permissions
   - Ensure write access to storage directory
   - Verify file ownership

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable debug logging for persistence operations
logger = logging.getLogger("app.services.graph_persistence")
logger.setLevel(logging.DEBUG)
```

## Future Enhancements

### Planned Features
- **Graph Versioning**: Version control for graphs
- **Graph Merging**: Combine multiple graphs
- **Graph Comparison**: Diff and merge operations
- **Advanced Analytics**: More sophisticated graph metrics
- **Visualization**: Built-in graph visualization
- **Graph Templates**: Pre-built graph templates
- **Backup/Restore**: Automated backup strategies

### Integration Opportunities
- **GraphQL API**: GraphQL interface for graph operations
- **Real-time Updates**: WebSocket support for live updates
- **Graph Streaming**: Stream processing for large graphs
- **Machine Learning**: ML-powered graph analysis
- **Cloud Storage**: AWS S3, Azure Blob integration

## Conclusion

The Graph Persistence feature provides a robust, scalable solution for managing knowledge graphs in the XReason platform. With support for both JSON and Neo4j storage, comprehensive REST API, and advanced analytics capabilities, it enables users to effectively store, share, and analyze complex knowledge structures across various domains.

The implementation is production-ready with proper error handling, security considerations, and performance optimizations, making it suitable for both development and enterprise environments.
