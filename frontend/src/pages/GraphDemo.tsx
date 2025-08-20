import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Chip,
  Divider,
} from '@mui/material';
import { PlayArrow, Refresh, Timeline } from '@mui/icons-material';
import ReasoningGraphVisualizer from '../components/ReasoningGraphVisualizer';
import { apiClient } from '../services/api';

interface GraphDemoProps {}

const GraphDemo: React.FC<GraphDemoProps> = () => {
  const [question, setQuestion] = useState('Is this GDPR compliant?');
  const [context, setContext] = useState('legal');
  const [graphId, setGraphId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [availableGraphs, setAvailableGraphs] = useState<any[]>([]);

  const loadAvailableGraphs = async () => {
    try {
      const response = await apiClient.get('/api/v1/graphs/');
      setAvailableGraphs(response.data);
    } catch (err) {
      console.error('Failed to load graphs:', err);
    }
  };

  useEffect(() => {
    loadAvailableGraphs();
  }, []);

  const generateReasoningGraph = async () => {
    try {
      setLoading(true);
      setError(null);

      // First, create a reasoning request
      const reasoningResponse = await apiClient.post('/api/v1/reason', {
        question,
        context: { domain: context },
      });

      // Get the session ID from the response
      const sessionId = reasoningResponse.data.session_id;

      // Create a graph from the reasoning traces
      const graphResponse = await apiClient.post('/api/v1/graphs/create-from-session', {
        session_id: sessionId,
        layout_type: 'hierarchical',
      });

      setGraphId(graphResponse.data.id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate reasoning graph');
    } finally {
      setLoading(false);
    }
  };

  const handleNodeClick = (nodeId: string, nodeData: any) => {
    console.log('Node clicked:', nodeId, nodeData);
  };

  const handleEdgeClick = (edgeId: string, edgeData: any) => {
    console.log('Edge clicked:', edgeId, edgeData);
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Typography variant="h3" gutterBottom>
        <Timeline sx={{ mr: 2, verticalAlign: 'middle' }} />
        Reasoning Graph Visualization
      </Typography>
      
      <Typography variant="body1" color="text.secondary" paragraph>
        Explore the reasoning process through interactive graph visualizations. 
        See how LLM hypotheses are validated by symbolic rules and knowledge checks.
      </Typography>

      <Grid container spacing={3}>
        {/* Controls Panel */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Generate New Graph
              </Typography>
              
              <Box sx={{ mb: 2 }}>
                <TextField
                  fullWidth
                  label="Question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  multiline
                  rows={3}
                  sx={{ mb: 2 }}
                />
                
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Domain</InputLabel>
                  <Select
                    value={context}
                    label="Domain"
                    onChange={(e) => setContext(e.target.value)}
                  >
                    <MenuItem value="legal">Legal (GDPR)</MenuItem>
                    <MenuItem value="scientific">Scientific</MenuItem>
                    <MenuItem value="healthcare">Healthcare</MenuItem>
                    <MenuItem value="finance">Finance</MenuItem>
                  </Select>
                </FormControl>
                
                <Button
                  fullWidth
                  variant="contained"
                  onClick={generateReasoningGraph}
                  disabled={loading}
                  startIcon={loading ? <Refresh /> : <PlayArrow />}
                >
                  {loading ? 'Generating...' : 'Generate Graph'}
                </Button>
              </Box>

              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}

              <Divider sx={{ my: 2 }} />

              <Typography variant="h6" gutterBottom>
                Available Graphs
              </Typography>
              
              <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
                {availableGraphs.length === 0 ? (
                  <Typography variant="body2" color="text.secondary">
                    No graphs available. Generate one to get started.
                  </Typography>
                ) : (
                  availableGraphs.map((graph) => (
                    <Card
                      key={graph.id}
                      variant="outlined"
                      sx={{ 
                        mb: 1, 
                        cursor: 'pointer',
                        bgcolor: graphId === graph.id ? 'primary.light' : 'transparent'
                      }}
                      onClick={() => setGraphId(graph.id)}
                    >
                      <CardContent sx={{ py: 1 }}>
                        <Typography variant="body2" fontWeight="bold">
                          {graph.metadata?.question || 'Unknown Question'}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(graph.created_at).toLocaleString()}
                        </Typography>
                        <Box sx={{ mt: 1 }}>
                          <Chip
                            label={`${graph.nodes?.length || 0} nodes`}
                            size="small"
                            variant="outlined"
                            sx={{ mr: 1 }}
                          />
                          <Chip
                            label={`${graph.edges?.length || 0} edges`}
                            size="small"
                            variant="outlined"
                          />
                        </Box>
                      </CardContent>
                    </Card>
                  ))
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Graph Visualization */}
        <Grid item xs={12} md={8}>
          {graphId ? (
            <ReasoningGraphVisualizer
              graphId={graphId}
              onNodeClick={handleNodeClick}
              onEdgeClick={handleEdgeClick}
              height={700}
              showControls={true}
              showStatistics={true}
            />
          ) : (
            <Card sx={{ height: 700, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CardContent>
                <Typography variant="h6" color="text.secondary" textAlign="center">
                  Select a graph or generate a new one to start visualizing
                </Typography>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>

      {/* Features Section */}
      <Box sx={{ mt: 6 }}>
        <Typography variant="h4" gutterBottom>
          Features
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🎨 Interactive Visualizations
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Zoom, pan, and interact with reasoning graphs. Click on nodes to see detailed information.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  📊 Advanced Analytics
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  View statistics, identify bottlenecks, and analyze reasoning paths through the graph.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🔄 Multiple Layouts
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Choose from hierarchical, circular, force-directed, and Kamada-Kawai layouts.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default GraphDemo;
