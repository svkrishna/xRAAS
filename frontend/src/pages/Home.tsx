import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Chip,
  Paper,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import {
  Psychology,
  Rule,
  Storage,
  Speed,
  CheckCircle,
  Science,
} from '@mui/icons-material';

const Home: React.FC = () => {
  const features = [
    {
      icon: <Psychology color="primary" sx={{ fontSize: 40 }} />,
      title: 'LLM Hypothesis Generation',
      description: 'Fast, intuitive reasoning using OpenAI GPT-4o for initial hypothesis generation',
    },
    {
      icon: <Rule color="primary" sx={{ fontSize: 40 }} />,
      title: 'Symbolic Rule Verification',
      description: 'Rule-based validation using Z3 solver and custom domain-specific rules',
    },
    {
      icon: <Storage color="primary" sx={{ fontSize: 40 }} />,
      title: 'Knowledge Graph Validation',
      description: 'Fact verification against structured knowledge base using NetworkX',
    },
    {
      icon: <Speed color="primary" sx={{ fontSize: 40 }} />,
      title: 'Fast Response Times',
      description: 'Optimized pipeline for sub-2 second response times',
    },
    {
      icon: <CheckCircle color="primary" sx={{ fontSize: 40 }} />,
      title: 'Explainable Traces',
      description: 'Complete reasoning trace showing each step of the decision process',
    },
    {
      icon: <Science color="primary" sx={{ fontSize: 40 }} />,
      title: 'Domain Expertise',
      description: 'Specialized rule sets for Healthcare (HIPAA) and Finance domains',
    },
  ];

  const useCases = [
    {
      domain: 'Healthcare',
      title: 'HIPAA Compliance Engine',
      description: 'Verify access requests against HIPAA 164.312(a)(1) requirements',
      example: 'Is this access request compliant with HIPAA 164.312(a)(1)?',
      color: 'success',
    },
    {
      domain: 'Finance',
      title: 'Financial Calculation Validation',
      description: 'Validate financial ratios and mathematical calculations',
      example: 'If debt=100, equity=50, what is Debt-to-Equity ratio?',
      color: 'info',
    },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Paper
        elevation={0}
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: 8,
          mb: 6,
          borderRadius: 2,
        }}
      >
        <Box textAlign="center">
          <Typography variant="h2" component="h1" gutterBottom fontWeight="bold">
            XReason
          </Typography>
          <Typography variant="h5" component="h2" gutterBottom>
            Reasoning as a Service (RaaS)
          </Typography>
          <Typography variant="body1" sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}>
            A modular reasoning pipeline combining LLM intuition (System 1) with 
            symbolic/rule-based checks (System 2) for explainable, validated answers.
          </Typography>
          <Button
            component={RouterLink}
            to="/demo"
            variant="contained"
            size="large"
            sx={{
              backgroundColor: 'white',
              color: 'primary.main',
              '&:hover': {
                backgroundColor: 'grey.100',
              },
            }}
          >
            Try the Demo
          </Button>
        </Box>
      </Paper>

      {/* Features Section */}
      <Typography variant="h4" component="h2" gutterBottom sx={{ mb: 4 }}>
        Key Features
      </Typography>
      <Grid container spacing={3} sx={{ mb: 6 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card elevation={2} sx={{ height: '100%' }}>
              <CardContent sx={{ textAlign: 'center', py: 3 }}>
                <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                <Typography variant="h6" component="h3" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Use Cases Section */}
      <Typography variant="h4" component="h2" gutterBottom sx={{ mb: 4 }}>
        Use Cases
      </Typography>
      <Grid container spacing={3} sx={{ mb: 6 }}>
        {useCases.map((useCase, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card elevation={2}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Chip
                    label={useCase.domain}
                    color={useCase.color as any}
                    sx={{ mr: 2 }}
                  />
                  <Typography variant="h6" component="h3">
                    {useCase.title}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {useCase.description}
                </Typography>
                <Paper
                  variant="outlined"
                  sx={{
                    p: 2,
                    backgroundColor: 'grey.50',
                    fontFamily: 'monospace',
                    fontSize: '0.875rem',
                  }}
                >
                  {useCase.example}
                </Paper>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* CTA Section */}
      <Paper
        elevation={2}
        sx={{
          p: 4,
          textAlign: 'center',
          background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
          color: 'white',
        }}
      >
        <Typography variant="h5" component="h3" gutterBottom>
          Ready to get started?
        </Typography>
        <Typography variant="body1" sx={{ mb: 3 }}>
          Explore the API documentation or try the interactive demo to see XReason in action.
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button
            component={RouterLink}
            to="/demo"
            variant="contained"
            size="large"
            sx={{
              backgroundColor: 'white',
              color: 'primary.main',
              '&:hover': {
                backgroundColor: 'grey.100',
              },
            }}
          >
            Try Demo
          </Button>
          <Button
            component={RouterLink}
            to="/docs"
            variant="outlined"
            size="large"
            sx={{
              borderColor: 'white',
              color: 'white',
              '&:hover': {
                borderColor: 'grey.100',
                backgroundColor: 'rgba(255,255,255,0.1)',
              },
            }}
          >
            View API Docs
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default Home;
