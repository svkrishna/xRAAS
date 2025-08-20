import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Chip,
  Grid,
  Paper,
  Tooltip,
  IconButton,
  Alert,
  CircularProgress,
  Divider,
} from '@mui/material';
import {
  ZoomIn,
  ZoomOut,
  Refresh,
  Download,
  Settings,
  Info,
  Timeline,
  Analytics,
} from '@mui/icons-material';
import Plot from 'react-plotly.js';
import { apiClient } from '../services/api';

interface GraphNode {
  id: string;
  label: string;
  type: string;
  x: number;
  y: number;
  confidence: number;
  color: string;
  size: number;
  content: any;
  metadata: any;
}

interface GraphEdge {
  id: string;
  source: string;
  target: string;
  label: string;
  type: string;
  weight: number;
  color: string;
  width: number;
  metadata: any;
}

interface GraphVisualizationData {
  nodes: GraphNode[];
  edges: GraphEdge[];
  layout: any;
  metadata: any;
}

interface GraphStatistics {
  total_nodes: number;
  total_edges: number;
  node_types: Record<string, number>;
  edge_types: Record<string, number>;
  average_confidence: number;
  execution_time_ms: number;
  critical_path: string[];
  bottlenecks: string[];
}

interface ReasoningGraphVisualizerProps {
  graphId: string;
  onNodeClick?: (nodeId: string, nodeData: GraphNode) => void;
  onEdgeClick?: (edgeId: string, edgeData: GraphEdge) => void;
  height?: number;
  showControls?: boolean;
  showStatistics?: boolean;
}

const ReasoningGraphVisualizer: React.FC<ReasoningGraphVisualizerProps> = ({
  graphId,
  onNodeClick,
  onEdgeClick,
  height = 600,
  showControls = true,
  showStatistics = true,
}) => {
  const [graphData, setGraphData] = useState<GraphVisualizationData | null>(null);
  const [statistics, setStatistics] = useState<GraphStatistics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [layoutType, setLayoutType] = useState('hierarchical');
  const [zoom, setZoom] = useState(1);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<string | null>(null);

  const layoutOptions = [
    { value: 'hierarchical', label: 'Hierarchical' },
    { value: 'circular', label: 'Circular' },
    { value: 'force_directed', label: 'Force Directed' },
    { value: 'kamada_kawai', label: 'Kamada-Kawai' },
  ];

  const loadGraphData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const [graphResponse, statsResponse] = await Promise.all([
        apiClient.get(`/api/v1/graphs/${graphId}/visualization?layout_type=${layoutType}`),
        apiClient.get(`/api/v1/graphs/${graphId}/statistics`),
      ]);

      setGraphData(graphResponse.data);
      setStatistics(statsResponse.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load graph data');
    } finally {
      setLoading(false);
    }
  }, [graphId, layoutType]);

  useEffect(() => {
    loadGraphData();
  }, [loadGraphData]);

  const handleNodeClick = useCallback((event: any) => {
    const point = event.points[0];
    const nodeId = point.data.nodeIds[point.pointIndex];
    const nodeData = graphData?.nodes.find(n => n.id === nodeId);
    
    if (nodeData) {
      setSelectedNode(nodeId);
      setSelectedEdge(null);
      onNodeClick?.(nodeId, nodeData);
    }
  }, [graphData, onNodeClick]);

  const handleZoomIn = () => setZoom(prev => Math.min(prev * 1.2, 3));
  const handleZoomOut = () => setZoom(prev => Math.max(prev / 1.2, 0.3));
  const handleReset = () => {
    setZoom(1);
    setSelectedNode(null);
    setSelectedEdge(null);
  };

  const exportGraph = async (format: string) => {
    try {
      const response = await apiClient.get(`/api/v1/graphs/${graphId}/export/${format}`, {
        responseType: 'blob',
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `reasoning-graph-${graphId}.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Failed to export graph:', err);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height={height}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ height }}>
        {error}
      </Alert>
    );
  }

  if (!graphData) {
    return (
      <Alert severity="warning" sx={{ height }}>
        No graph data available
      </Alert>
    );
  }

  // Prepare Plotly data
  const plotlyData: any[] = [];

  // Add nodes
  plotlyData.push({
    x: graphData.nodes.map(n => n.x),
    y: graphData.nodes.map(n => n.y),
    mode: 'markers+text',
    type: 'scatter',
    text: graphData.nodes.map(n => n.label),
    textposition: 'top center',
    textfont: { size: 10 },
    marker: {
      size: graphData.nodes.map(n => n.size * zoom),
      color: graphData.nodes.map(n => n.color),
      line: { width: 2, color: 'black' },
      opacity: 0.8,
    },
    hovertemplate: 
      '<b>%{text}</b><br>' +
      'Type: %{customdata[0]}<br>' +
      'Confidence: %{customdata[1]:.2f}<br>' +
      '<extra></extra>',
    customdata: graphData.nodes.map(n => [n.type, n.confidence]),
    nodeIds: graphData.nodes.map(n => n.id),
    name: 'Nodes',
  });

  // Add edges
  graphData.edges.forEach(edge => {
    const sourceNode = graphData.nodes.find(n => n.id === edge.source);
    const targetNode = graphData.nodes.find(n => n.id === edge.target);
    
    if (sourceNode && targetNode) {
      plotlyData.push({
        x: [sourceNode.x, targetNode.x],
        y: [sourceNode.y, targetNode.y],
        mode: 'lines',
        type: 'scatter',
        line: {
          width: edge.width * zoom,
          color: edge.color,
        },
        showlegend: false,
        hoverinfo: 'skip',
        name: edge.label,
      });
    }
  });

  const layout = {
    title: {
      text: 'Reasoning Graph Visualization',
      font: { size: 16 },
    },
    showlegend: false,
    hovermode: 'closest',
    margin: { b: 20, l: 5, r: 5, t: 40 },
    xaxis: {
      showgrid: false,
      zeroline: false,
      showticklabels: false,
      range: [-10, 10],
    },
    yaxis: {
      showgrid: false,
      zeroline: false,
      showticklabels: false,
      range: [-10, 10],
    },
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    width: undefined,
    height: height - 100,
  };

  const config = {
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
  };

  return (
    <Box>
      {showControls && (
        <Card sx={{ mb: 2 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={3}>
                <FormControl fullWidth size="small">
                  <InputLabel>Layout</InputLabel>
                  <Select
                    value={layoutType}
                    label="Layout"
                    onChange={(e) => setLayoutType(e.target.value)}
                  >
                    {layoutOptions.map(option => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Box display="flex" gap={1}>
                  <Tooltip title="Zoom In">
                    <IconButton onClick={handleZoomIn} size="small">
                      <ZoomIn />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Zoom Out">
                    <IconButton onClick={handleZoomOut} size="small">
                      <ZoomOut />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Reset View">
                    <IconButton onClick={handleReset} size="small">
                      <Refresh />
                    </IconButton>
                  </Tooltip>
                  <Divider orientation="vertical" flexItem />
                  <Tooltip title="Export as PNG">
                    <IconButton onClick={() => exportGraph('png')} size="small">
                      <Download />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Export as SVG">
                    <IconButton onClick={() => exportGraph('svg')} size="small">
                      <Download />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={3}>
                <Typography variant="body2" color="text.secondary">
                  Zoom: {zoom.toFixed(1)}x
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      <Grid container spacing={2}>
        <Grid item xs={showStatistics ? 8 : 12}>
          <Paper elevation={2} sx={{ p: 2 }}>
            <Plot
              data={plotlyData}
              layout={layout}
              config={config}
              onClick={handleNodeClick}
              style={{ width: '100%', height: '100%' }}
            />
          </Paper>
        </Grid>

        {showStatistics && statistics && (
          <Grid item xs={4}>
            <Box>
              <Card sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <Analytics sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Graph Statistics
                  </Typography>
                  
                  <Grid container spacing={1}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Nodes
                      </Typography>
                      <Typography variant="h6">
                        {statistics.total_nodes}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Edges
                      </Typography>
                      <Typography variant="h6">
                        {statistics.total_edges}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Avg Confidence
                      </Typography>
                      <Typography variant="h6">
                        {(statistics.average_confidence * 100).toFixed(1)}%
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Execution Time
                      </Typography>
                      <Typography variant="h6">
                        {statistics.execution_time_ms.toFixed(0)}ms
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              <Card sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <Timeline sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Node Types
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    {Object.entries(statistics.node_types).map(([type, count]) => (
                      <Chip
                        key={type}
                        label={`${type}: ${count}`}
                        size="small"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                </CardContent>
              </Card>

              {statistics.bottlenecks.length > 0 && (
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom color="warning.main">
                      <Info sx={{ mr: 1, verticalAlign: 'middle' }} />
                      Bottlenecks
                    </Typography>
                    <Box display="flex" flexWrap="wrap" gap={1}>
                      {statistics.bottlenecks.map(bottleneck => (
                        <Chip
                          key={bottleneck}
                          label={bottleneck}
                          size="small"
                          color="warning"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </CardContent>
                </Card>
              )}
            </Box>
          </Grid>
        )}
      </Grid>

      {selectedNode && (
        <Card sx={{ mt: 2 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Selected Node: {selectedNode}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {graphData.nodes.find(n => n.id === selectedNode)?.content?.question || 
               graphData.nodes.find(n => n.id === selectedNode)?.content?.hypothesis || 
               'No additional information available'}
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default ReasoningGraphVisualizer;
