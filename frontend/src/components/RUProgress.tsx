/**
 * RU Progress Component
 * Reasoning Units usage meter with forecast and upgrade prompts
 */

import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Button,
  Chip,
  Alert
} from '@mui/material';
import {
  TrendingUp,
  Warning,
  Speed
} from '@mui/icons-material';

interface RUProgressProps {
  used: number;
  quota: number;
  forecastEndOfMonth?: number;
  onUpgrade?: () => void;
}

export function RUProgress({ used, quota, forecastEndOfMonth, onUpgrade }: RUProgressProps) {
  const percentage = (used / quota) * 100;
  const isOverQuota = used > quota;
  const isNearQuota = percentage >= 80;
  const isForecastedOver = forecastEndOfMonth && forecastEndOfMonth > quota;

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat().format(num);
  };

  const getProgressColor = () => {
    if (isOverQuota) return 'error';
    if (isNearQuota) return 'warning';
    return 'primary';
  };

  const getStatusMessage = () => {
    if (isOverQuota) {
      return 'You have exceeded your monthly quota. Consider upgrading your plan.';
    }
    if (isNearQuota) {
      return 'You are approaching your monthly quota limit.';
    }
    if (isForecastedOver) {
      return `Based on current usage, you're projected to exceed your quota by ${formatNumber(forecastEndOfMonth - quota)} RUs.`;
    }
    return 'Your usage is within normal limits.';
  };

  const getStatusIcon = () => {
    if (isOverQuota) return <Warning color="error" />;
    if (isNearQuota || isForecastedOver) return <TrendingUp color="warning" />;
    return <Speed color="success" />;
  };

  const getStatusColor = () => {
    if (isOverQuota) return 'error';
    if (isNearQuota || isForecastedOver) return 'warning';
    return 'success';
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Reasoning Units Usage
          </Typography>
          <Chip
            label={`${formatNumber(used)} / ${formatNumber(quota)}`}
            color={getProgressColor()}
            variant="outlined"
            size="small"
          />
        </Box>

        <Box sx={{ mb: 2 }}>
          <LinearProgress
            variant="determinate"
            value={Math.min(percentage, 100)}
            color={getProgressColor()}
            sx={{ height: 8, borderRadius: 4 }}
          />
          <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
            {percentage.toFixed(1)}% of monthly quota used
          </Typography>
        </Box>

        {forecastEndOfMonth && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Projected end of month: {formatNumber(forecastEndOfMonth)} RUs
            </Typography>
          </Box>
        )}

        {(isOverQuota || isNearQuota || isForecastedOver) && (
          <Alert
            severity={getStatusColor()}
            icon={getStatusIcon()}
            sx={{ mb: 2 }}
          >
            {getStatusMessage()}
          </Alert>
        )}

        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="contained"
            size="small"
            onClick={onUpgrade}
            sx={{ flex: 1 }}
          >
            Upgrade Plan
          </Button>
          <Button
            variant="outlined"
            size="small"
            sx={{ flex: 1 }}
          >
            View Usage Details
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}
