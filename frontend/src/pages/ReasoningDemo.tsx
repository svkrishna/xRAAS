import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  LinearProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Paper,
  Grid,
} from '@mui/material';
import {
  Send,
  ExpandMore,
  Psychology,
  Rule,
  Storage,
  CheckCircle,
} from '@mui/icons-material';
import JSONPretty from 'react-json-pretty';
import 'react-json-pretty/themes/monikai.css';
import { reasoningService } from '../services/reasoningService';

interface ReasoningTrace {
  stage: string;
  output: string;
  confidence?: number;
  metadata?: any;
}

interface ReasoningResponse {
  answer: string;
  reasoning_trace: ReasoningTrace[];
  confidence: number;
  domain?: string;
  metadata?: any;
}

const ReasoningDemo: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [context, setContext] = useState('');
  const [domain, setDomain] = useState('general');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ReasoningResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const exampleQuestions = [
    {
      question: 'Is this access request compliant with HIPAA 164.312(a)(1)?',
      context: 'A nurse is requesting access to patient records through the electronic health system.',
      domain: 'healthcare',
    },
    {
      question: 'If debt=100, equity=50, what is Debt-to-Equity ratio?',
      context: 'Financial analysis for company XYZ',
      domain: 'finance',
    },
    {
      question: 'What is the logical consistency of the statement "All A are B, and some B are C, therefore all A are C"?',
      context: 'Logical reasoning exercise',
      domain: 'general',
    },
  ];

  const handleSubmit = async () => {
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await reasoningService.reason({
        question: question.trim(),
        context: context.trim() || undefined,
        domain: domain === 'general' ? undefined : domain,
      });
      setResponse(result);
    } catch (err: any) {
      setError(err.message || 'An error occurred while processing your request');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example: any) => {
    setQuestion(example.question);
    setContext(example.context);
    setDomain(example.domain);
  };

  const getStageIcon = (stage: string) => {
    switch (stage) {
      case 'LLM Hypothesis':
        return <Psychology color="primary" />;
      case 'Rule Check':
        return <Rule color="primary" />;
      case 'Knowledge Graph':
        return <Storage color="primary" />;
      case 'Validation':
        return <CheckCircle color="primary" />;
      default:
        return <Psychology color="primary" />;
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'success';
    if (confidence >= 0.6) return 'warning';
    return 'error';
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Reasoning Demo
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Test the XReason reasoning pipeline with your own questions or try the examples below.
      </Typography>

      <Grid container spacing={3}>
        {/* Input Section */}
        <Grid item xs={12} md={6}>
          <Card elevation={2}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Ask a Question
              </Typography>
              
              <TextField
                fullWidth
                label="Question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                multiline
                rows={3}
                sx={{ mb: 2 }}
                placeholder="Enter your question here..."
              />
              
              <TextField
                fullWidth
                label="Context (Optional)"
                value={context}
                onChange={(e) => setContext(e.target.value)}
                multiline
                rows={2}
                sx={{ mb: 2 }}
                placeholder="Additional context or background information..."
              />
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Domain</InputLabel>
                <Select
                  value={domain}
                  label="Domain"
                  onChange={(e) => setDomain(e.target.value)}
                >
                  <MenuItem value="general">General</MenuItem>
                  <MenuItem value="healthcare">Healthcare</MenuItem>
                  <MenuItem value="finance">Finance</MenuItem>
                </Select>
              </FormControl>
              
              <Button
                fullWidth
                variant="contained"
                onClick={handleSubmit}
                disabled={loading || !question.trim()}
                startIcon={<Send />}
                size="large"
              >
                {loading ? 'Processing...' : 'Submit Question'}
              </Button>
              
              {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Example Questions */}
          <Card elevation={2} sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Example Questions
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Click on an example to load it into the form:
              </Typography>
              {exampleQuestions.map((example, index) => (
                <Paper
                  key={index}
                  variant="outlined"
                  sx={{
                    p: 2,
                    mb: 2,
                    cursor: 'pointer',
                    '&:hover': {
                      backgroundColor: 'grey.50',
                    },
                  }}
                  onClick={() => handleExampleClick(example)}
                >
                  <Typography variant="body2" fontWeight="bold" gutterBottom>
                    {example.question}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Context: {example.context}
                  </Typography>
                  <Chip
                    label={example.domain}
                    size="small"
                    sx={{ ml: 1 }}
                    color={example.domain === 'healthcare' ? 'success' : example.domain === 'finance' ? 'info' : 'default'}
                  />
                </Paper>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Results Section */}
        <Grid item xs={12} md={6}>
          {loading && (
            <Card elevation={2}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Processing...
                </Typography>
                <LinearProgress sx={{ mb: 2 }} />
                <Typography variant="body2" color="text.secondary">
                  The reasoning pipeline is analyzing your question...
                </Typography>
              </CardContent>
            </Card>
          )}

          {response && (
            <Card elevation={2}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Results
                </Typography>
                
                {/* Final Answer */}
                <Paper
                  variant="outlined"
                  sx={{
                    p: 2,
                    mb: 3,
                    backgroundColor: 'grey.50',
                  }}
                >
                  <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                    Final Answer:
                  </Typography>
                  <Typography variant="body1">{response.answer}</Typography>
                  <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="body2">Confidence:</Typography>
                    <Chip
                      label={`${(response.confidence * 100).toFixed(1)}%`}
                      color={getConfidenceColor(response.confidence) as any}
                      size="small"
                    />
                  </Box>
                </Paper>

                {/* Reasoning Trace */}
                <Typography variant="h6" gutterBottom>
                  Reasoning Trace
                </Typography>
                {response.reasoning_trace.map((trace, index) => (
                  <Accordion key={index} sx={{ mb: 1 }}>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {getStageIcon(trace.stage)}
                        <Typography variant="subtitle2">{trace.stage}</Typography>
                        {trace.confidence && (
                          <Chip
                            label={`${(trace.confidence * 100).toFixed(1)}%`}
                            color={getConfidenceColor(trace.confidence) as any}
                            size="small"
                          />
                        )}
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                        {trace.output}
                      </Typography>
                      {trace.metadata && (
                        <Box sx={{ mt: 2 }}>
                          <Typography variant="caption" fontWeight="bold">
                            Metadata:
                          </Typography>
                          <JSONPretty
                            data={trace.metadata}
                            style={{ backgroundColor: 'transparent' }}
                          />
                        </Box>
                      )}
                    </AccordionDetails>
                  </Accordion>
                ))}

                {/* Response Metadata */}
                {response.metadata && (
                  <Box sx={{ mt: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Response Metadata
                    </Typography>
                    <JSONPretty
                      data={response.metadata}
                      style={{ backgroundColor: 'transparent' }}
                    />
                  </Box>
                )}
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default ReasoningDemo;
