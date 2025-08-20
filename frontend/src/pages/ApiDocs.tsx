import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Tabs,
  Tab,
  Paper,
  Grid,
  Chip,
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Code,
  Api,
  Psychology,
  Rule,
  Storage,
} from '@mui/icons-material';
import JSONPretty from 'react-json-pretty';
import 'react-json-pretty/themes/monikai.css';
import { reasoningService } from '../services/reasoningService';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`api-tabpanel-${index}`}
      aria-labelledby={`api-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const ApiDocs: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [healthData, setHealthData] = useState<any>(null);
  const [rulesData, setRulesData] = useState<any>(null);
  const [knowledgeData, setKnowledgeData] = useState<any>(null);
  const [capabilitiesData, setCapabilitiesData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadApiData();
  }, []);

  const loadApiData = async () => {
    setLoading(true);
    setError(null);

    try {
      const [health, rules, knowledge, capabilities] = await Promise.all([
        reasoningService.getDetailedHealth(),
        reasoningService.getRules(),
        reasoningService.getKnowledgeSummary(),
        reasoningService.getCapabilities(),
      ]);

      setHealthData(health);
      setRulesData(rules);
      setKnowledgeData(knowledge);
      setCapabilitiesData(capabilities);
    } catch (err: any) {
      setError(err.message || 'Failed to load API data');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const endpoints = [
    {
      method: 'POST',
      path: '/api/v1/reason/',
      description: 'Main reasoning endpoint',
      example: {
        question: 'Is this access request compliant with HIPAA 164.312(a)(1)?',
        context: 'A nurse is requesting access to patient records.',
        domain: 'healthcare',
      },
    },
    {
      method: 'GET',
      path: '/health/',
      description: 'Basic health check',
    },
    {
      method: 'GET',
      path: '/health/detailed',
      description: 'Detailed health check with component status',
    },
    {
      method: 'GET',
      path: '/api/v1/reason/rules',
      description: 'Get available rule sets',
      params: 'domain (optional)',
    },
    {
      method: 'GET',
      path: '/api/v1/reason/knowledge',
      description: 'Get knowledge base summary',
      params: 'domain (optional)',
    },
    {
      method: 'GET',
      path: '/api/v1/reason/capabilities',
      description: 'Get reasoning capabilities',
      params: 'domain (optional)',
    },
    {
      method: 'POST',
      path: '/api/v1/reason/validate',
      description: 'Validate a reasoning request',
    },
  ];

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        API Documentation
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Complete API reference and live system status for XReason.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* API Endpoints */}
        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                API Endpoints
              </Typography>
              {endpoints.map((endpoint, index) => (
                <Paper key={index} variant="outlined" sx={{ p: 2, mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Chip
                      label={endpoint.method}
                      color={endpoint.method === 'POST' ? 'primary' : 'default'}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Typography variant="body2" fontFamily="monospace">
                      {endpoint.path}
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {endpoint.description}
                  </Typography>
                  {endpoint.params && (
                    <Typography variant="caption" color="text.secondary">
                      Parameters: {endpoint.params}
                    </Typography>
                  )}
                  {endpoint.example && (
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="caption" fontWeight="bold">
                        Example Request:
                      </Typography>
                      <JSONPretty
                        data={endpoint.example}
                        style={{ backgroundColor: 'transparent' }}
                      />
                    </Box>
                  )}
                </Paper>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* System Status */}
        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Status
              </Typography>
              
              <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
                <Tabs value={tabValue} onChange={handleTabChange}>
                  <Tab label="Health" icon={<Api />} />
                  <Tab label="Rules" icon={<Rule />} />
                  <Tab label="Knowledge" icon={<Storage />} />
                  <Tab label="Capabilities" icon={<Psychology />} />
                </Tabs>
              </Box>

              <TabPanel value={tabValue} index={0}>
                {healthData && (
                  <JSONPretty
                    data={healthData}
                    style={{ backgroundColor: 'transparent' }}
                  />
                )}
              </TabPanel>

              <TabPanel value={tabValue} index={1}>
                {rulesData && (
                  <JSONPretty
                    data={rulesData}
                    style={{ backgroundColor: 'transparent' }}
                  />
                )}
              </TabPanel>

              <TabPanel value={tabValue} index={2}>
                {knowledgeData && (
                  <JSONPretty
                    data={knowledgeData}
                    style={{ backgroundColor: 'transparent' }}
                  />
                )}
              </TabPanel>

              <TabPanel value={tabValue} index={3}>
                {capabilitiesData && (
                  <JSONPretty
                    data={capabilitiesData}
                    style={{ backgroundColor: 'transparent' }}
                  />
                )}
              </TabPanel>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Request/Response Examples */}
      <Card elevation={2} sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Request/Response Examples
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" gutterBottom>
                Example Request
              </Typography>
              <Paper variant="outlined" sx={{ p: 2, backgroundColor: 'grey.50' }}>
                <Typography variant="body2" fontFamily="monospace" sx={{ whiteSpace: 'pre-wrap' }}>
{`POST /api/v1/reason/
Content-Type: application/json

{
  "question": "Is this access request compliant with HIPAA 164.312(a)(1)?",
  "context": "A nurse is requesting access to patient records through the electronic health system.",
  "domain": "healthcare",
  "confidence_threshold": 0.7
}`}
                </Typography>
              </Paper>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" gutterBottom>
                Example Response
              </Typography>
              <Paper variant="outlined" sx={{ p: 2, backgroundColor: 'grey.50' }}>
                <Typography variant="body2" fontFamily="monospace" sx={{ whiteSpace: 'pre-wrap' }}>
{`{
  "answer": "Based on the analysis, this access request appears to be compliant with HIPAA 164.312(a)(1)...",
  "reasoning_trace": [
    {
      "stage": "LLM Hypothesis",
      "output": "The LLM generated initial analysis...",
      "confidence": 0.8
    },
    {
      "stage": "Rule Check",
      "output": "Applied 3 HIPAA rules, passed 2/3...",
      "confidence": 0.7
    }
  ],
  "confidence": 0.75,
  "domain": "healthcare",
  "metadata": {
    "processing_time": 1.2,
    "session_id": "uuid-here"
  }
}`}
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Interactive API Testing */}
      <Card elevation={2} sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Interactive API Testing
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Test the API directly from your browser or use the demo interface.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              href="/demo"
              target="_blank"
            >
              Open Demo Interface
            </Button>
            <Button
              variant="outlined"
              href="/docs"
              target="_blank"
            >
              OpenAPI Documentation
            </Button>
            <Button
              variant="outlined"
              onClick={loadApiData}
            >
              Refresh Data
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ApiDocs;
