/**
 * Compliance Card Component
 * Shows compliance status and framework coverage
 */

import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Button,
  LinearProgress
} from '@mui/material';
import {
  CheckCircle,
  Warning,
  Error,
  Security,
  Assignment
} from '@mui/icons-material';

interface ComplianceFramework {
  name: string;
  status: 'compliant' | 'at_risk' | 'non_compliant' | 'not_assessed';
  score: number;
  lastAssessment: string;
  controls: {
    total: number;
    compliant: number;
    atRisk: number;
    nonCompliant: number;
  };
}

export function ComplianceCard() {
  // Mock compliance data
  const frameworks: ComplianceFramework[] = [
    {
      name: 'HIPAA',
      status: 'compliant',
      score: 94,
      lastAssessment: '2024-01-15',
      controls: { total: 45, compliant: 42, atRisk: 2, nonCompliant: 1 }
    },
    {
      name: 'GDPR',
      status: 'at_risk',
      score: 87,
      lastAssessment: '2024-01-10',
      controls: { total: 38, compliant: 33, atRisk: 4, nonCompliant: 1 }
    },
    {
      name: 'SOX',
      status: 'compliant',
      score: 96,
      lastAssessment: '2024-01-12',
      controls: { total: 52, compliant: 50, atRisk: 1, nonCompliant: 1 }
    },
    {
      name: 'PCI DSS',
      status: 'non_compliant',
      score: 72,
      lastAssessment: '2024-01-08',
      controls: { total: 78, compliant: 56, atRisk: 12, nonCompliant: 10 }
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'compliant': return 'success';
      case 'at_risk': return 'warning';
      case 'non_compliant': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'compliant': return <CheckCircle color="success" />;
      case 'at_risk': return <Warning color="warning" />;
      case 'non_compliant': return <Error color="error" />;
      default: return <Assignment color="action" />;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'compliant': return 'Compliant';
      case 'at_risk': return 'At Risk';
      case 'non_compliant': return 'Non-Compliant';
      default: return 'Not Assessed';
    }
  };

  const overallScore = frameworks.reduce((acc, framework) => acc + framework.score, 0) / frameworks.length;

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Compliance Overview
          </Typography>
          <Chip
            label={`${overallScore.toFixed(0)}%`}
            color={overallScore >= 90 ? 'success' : overallScore >= 80 ? 'warning' : 'error'}
            variant="outlined"
          />
        </Box>

        <Box sx={{ mb: 3 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            Overall Compliance Score
          </Typography>
          <LinearProgress
            variant="determinate"
            value={overallScore}
            color={overallScore >= 90 ? 'success' : overallScore >= 80 ? 'warning' : 'error'}
            sx={{ height: 8, borderRadius: 4 }}
          />
        </Box>

        <List sx={{ py: 0 }}>
          {frameworks.map((framework) => (
            <ListItem
              key={framework.name}
              sx={{
                px: 0,
                py: 1,
                borderBottom: '1px solid',
                borderColor: 'divider',
                '&:last-child': { borderBottom: 'none' }
              }}
            >
              <ListItemIcon sx={{ minWidth: 40 }}>
                {getStatusIcon(framework.status)}
              </ListItemIcon>
              
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      {framework.name}
                    </Typography>
                    <Chip
                      label={getStatusText(framework.status)}
                      size="small"
                      color={getStatusColor(framework.status)}
                      variant="outlined"
                    />
                  </Box>
                }
                secondary={
                  <Box>
                    <Typography variant="caption" color="text.secondary">
                      Score: {framework.score}% • Last assessed: {framework.lastAssessment}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                      <Chip
                        label={`${framework.controls.compliant}/${framework.controls.total} controls`}
                        size="small"
                        variant="outlined"
                        sx={{ fontSize: '0.7rem' }}
                      />
                    </Box>
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>

        <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
          <Button
            variant="outlined"
            size="small"
            startIcon={<Security />}
            sx={{ flex: 1 }}
          >
            View Details
          </Button>
          <Button
            variant="contained"
            size="small"
            startIcon={<Assignment />}
            sx={{ flex: 1 }}
          >
            Run Assessment
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}
