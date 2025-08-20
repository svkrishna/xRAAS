/**
 * Dashboard Page
 * Main dashboard with analytics, KPIs, and overview metrics
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Button
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  MoreVert,
  Psychology,
  AccountTree,
  Security,
  Payment,
  People,
  History,
  Download,
  Refresh
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { useAuth } from '../auth/AuthProvider';
import { useTenant } from '../auth/TenantProvider';
import { RUProgress } from '../components/RUProgress';
import { UsageChart } from '../components/UsageChart';
import { ComplianceCard } from '../components/ComplianceCard';

interface DashboardMetric {
  label: string;
  value: string | number;
  change: number;
  trend: 'up' | 'down' | 'neutral';
  icon: React.ReactNode;
  color: string;
}

interface ChartData {
  name: string;
  value: number;
}

export function Dashboard() {
  const { user } = useAuth();
  const { currentTenant } = useTenant();
  const [timeRange, setTimeRange] = useState('7d');
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  // Mock data - replace with real API calls
  const [metrics, setMetrics] = useState<DashboardMetric[]>([
    {
      label: 'Reasoning Units',
      value: '12,847',
      change: 23.5,
      trend: 'up',
      icon: <Psychology />,
      color: '#1976d2'
    },
    {
      label: 'API Calls',
      value: '45,234',
      change: -5.2,
      trend: 'down',
      icon: <AccountTree />,
      color: '#9c27b0'
    },
    {
      label: 'Compliance Score',
      value: '94.2%',
      change: 2.1,
      trend: 'up',
      icon: <Security />,
      color: '#2e7d32'
    },
    {
      label: 'Active Users',
      value: '156',
      change: 12.3,
      trend: 'up',
      icon: <People />,
      color: '#ed6c02'
    }
  ]);

  const usageData = [
    { name: 'Mon', reasoning: 1200, api: 4500 },
    { name: 'Tue', reasoning: 1400, api: 5200 },
    { name: 'Wed', reasoning: 1100, api: 4800 },
    { name: 'Thu', reasoning: 1600, api: 6100 },
    { name: 'Fri', reasoning: 1800, api: 6800 },
    { name: 'Sat', reasoning: 900, api: 3200 },
    { name: 'Sun', reasoning: 800, api: 2800 }
  ];

  const complianceData: ChartData[] = [
    { name: 'Compliant', value: 94 },
    { name: 'At Risk', value: 4 },
    { name: 'Non-Compliant', value: 2 }
  ];

  const COLORS = ['#2e7d32', '#ed6c02', '#d32f2f'];

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleExport = () => {
    // TODO: Implement export functionality
    console.log('Exporting dashboard data...');
    handleMenuClose();
  };

  const handleRefresh = () => {
    // TODO: Implement refresh functionality
    console.log('Refreshing dashboard...');
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 0.5 }}>
            Dashboard
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Welcome back, {user?.name}. Here's what's happening with {currentTenant?.name}.
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Button
            startIcon={<Refresh />}
            onClick={handleRefresh}
            variant="outlined"
            size="small"
          >
            Refresh
          </Button>
          
          <IconButton onClick={handleMenuOpen}>
            <MoreVert />
          </IconButton>
          
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={handleExport}>
              <ListItemIcon>
                <Download fontSize="small" />
              </ListItemIcon>
              <ListItemText>Export Data</ListItemText>
            </MenuItem>
            <MenuItem onClick={handleMenuClose}>
              <ListItemIcon>
                <History fontSize="small" />
              </ListItemIcon>
              <ListItemText>View History</ListItemText>
            </MenuItem>
          </Menu>
        </Box>
      </Box>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {metrics.map((metric, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Box
                    sx={{
                      p: 1,
                      borderRadius: 2,
                      backgroundColor: metric.color + '20',
                      color: metric.color
                    }}
                  >
                    {metric.icon}
                  </Box>
                  <Chip
                    label={`${metric.change > 0 ? '+' : ''}${metric.change}%`}
                    size="small"
                    color={metric.trend === 'up' ? 'success' : metric.trend === 'down' ? 'error' : 'default'}
                    icon={metric.trend === 'up' ? <TrendingUp /> : <TrendingDown />}
                    sx={{ fontSize: '0.75rem' }}
                  />
                </Box>
                
                <Typography variant="h4" sx={{ fontWeight: 700, mb: 0.5 }}>
                  {metric.value}
                </Typography>
                
                <Typography variant="body2" color="text.secondary">
                  {metric.label}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Usage Progress */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Usage Analytics
                </Typography>
                <Chip label="Last 7 days" size="small" variant="outlined" />
              </Box>
              
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={usageData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Line 
                    type="monotone" 
                    dataKey="reasoning" 
                    stroke="#1976d2" 
                    strokeWidth={2}
                    name="Reasoning Units"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="api" 
                    stroke="#9c27b0" 
                    strokeWidth={2}
                    name="API Calls"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Compliance Status
              </Typography>
              
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={complianceData}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {complianceData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              
              <Box sx={{ mt: 2 }}>
                {complianceData.map((item, index) => (
                  <Box key={item.name} sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        borderRadius: '50%',
                        backgroundColor: COLORS[index]
                      }}
                    />
                    <Typography variant="body2">
                      {item.name}: {item.value}%
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* RU Progress and Compliance */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <RUProgress
            used={12847}
            quota={10000}
            forecastEndOfMonth={15000}
            onUpgrade={() => console.log('Upgrade clicked')}
          />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <ComplianceCard />
        </Grid>
      </Grid>
    </Box>
  );
}
