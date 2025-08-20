/**
 * AppShell Component
 * Main application layout with navigation, header, and content area
 */

import React, { useState } from 'react';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  useTheme,
  useMediaQuery,
  Badge,
  Avatar,
  Menu,
  MenuItem,
  Chip
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  Psychology,
  AccountTree,
  Analytics,
  Security,
  LibraryBooks,
  History,
  People,
  Payment,
  Settings,
  Notifications,
  Brightness4,
  Brightness7,
  AccountCircle,
  Business,
  Logout
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../auth/AuthProvider';
import { useTenant } from '../auth/TenantProvider';
import { useTheme as useAppTheme } from '../theme/ThemeProvider';
import { TenantSwitcher } from './TenantSwitcher';
import { NotificationCenter } from './NotificationCenter';

const drawerWidth = 280;

interface AppShellProps {
  children: React.ReactNode;
}

interface NavigationItem {
  label: string;
  path: string;
  icon: React.ReactNode;
  badge?: number;
  permission?: string;
}

export function AppShell({ children }: AppShellProps) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);
  const [userMenuAnchor, setUserMenuAnchor] = useState<null | HTMLElement>(null);
  const [notificationAnchor, setNotificationAnchor] = useState<null | HTMLElement>(null);
  
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const { currentTenant } = useTenant();
  const { toggleTheme, mode } = useAppTheme();

  const navigationItems: NavigationItem[] = [
    {
      label: 'Dashboard',
      path: '/',
      icon: <Dashboard />
    },
    {
      label: 'Reasoning',
      path: '/reasoning',
      icon: <Psychology />
    },
    {
      label: 'Graphs',
      path: '/graphs',
      icon: <AccountTree />
    },
    {
      label: 'Analytics',
      path: '/analytics',
      icon: <Analytics />,
      permission: 'view_analytics'
    },
    {
      label: 'Compliance',
      path: '/compliance',
      icon: <Security />,
      permission: 'view_compliance'
    },
    {
      label: 'Rulesets',
      path: '/rulesets',
      icon: <LibraryBooks />,
      permission: 'view_rulesets'
    },
    {
      label: 'Audit',
      path: '/audit',
      icon: <History />,
      permission: 'view_audit'
    },
    {
      label: 'Partners',
      path: '/partners',
      icon: <People />,
      permission: 'view_partners'
    },
    {
      label: 'Billing',
      path: '/billing',
      icon: <Payment />,
      permission: 'view_billing'
    },
    {
      label: 'Admin',
      path: '/admin',
      icon: <Settings />,
      permission: 'manage_users'
    }
  ];

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleNavigation = (path: string) => {
    navigate(path);
    if (isMobile) {
      setMobileOpen(false);
    }
  };

  const handleUserMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setUserMenuAnchor(event.currentTarget);
  };

  const handleUserMenuClose = () => {
    setUserMenuAnchor(null);
  };

  const handleLogout = async () => {
    await logout();
    handleUserMenuClose();
  };

  const drawer = (
    <Box>
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
        <Typography variant="h6" component="div" sx={{ fontWeight: 'bold' }}>
          XReason
        </Typography>
        <Chip 
          label={currentTenant?.subscriptionTier || 'starter'} 
          size="small" 
          color="primary" 
          variant="outlined"
        />
      </Box>
      
      <Divider />
      
      <List sx={{ pt: 1 }}>
        {navigationItems.map((item) => (
          <ListItem key={item.path} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => handleNavigation(item.path)}
              sx={{
                mx: 1,
                borderRadius: 1,
                '&.Mui-selected': {
                  backgroundColor: theme.palette.primary.main + '20',
                  '&:hover': {
                    backgroundColor: theme.palette.primary.main + '30',
                  }
                }
              }}
            >
              <ListItemIcon sx={{ minWidth: 40 }}>
                {item.badge ? (
                  <Badge badgeContent={item.badge} color="error">
                    {item.icon}
                  </Badge>
                ) : (
                  item.icon
                )}
              </ListItemIcon>
              <ListItemText 
                primary={item.label}
                primaryTypographyProps={{
                  fontSize: '0.875rem',
                  fontWeight: location.pathname === item.path ? 600 : 400
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {/* App Bar */}
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${drawerWidth}px)` },
          ml: { md: `${drawerWidth}px` },
          zIndex: theme.zIndex.drawer + 1
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>

          <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', gap: 2 }}>
            <TenantSwitcher />
            
            <Chip
              label={process.env.NODE_ENV === 'production' ? 'PROD' : 'STAGING'}
              size="small"
              color={process.env.NODE_ENV === 'production' ? 'error' : 'warning'}
              variant="outlined"
            />
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {/* Theme Toggle */}
            <IconButton color="inherit" onClick={toggleTheme}>
              {mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
            </IconButton>

            {/* Notifications */}
            <IconButton 
              color="inherit"
              onClick={(e) => setNotificationAnchor(e.currentTarget)}
            >
              <Badge badgeContent={4} color="error">
                <Notifications />
              </Badge>
            </IconButton>

            {/* User Menu */}
            <IconButton
              color="inherit"
              onClick={handleUserMenuOpen}
              sx={{ ml: 1 }}
            >
              {user?.avatar ? (
                <Avatar src={user.avatar} sx={{ width: 32, height: 32 }} />
              ) : (
                <AccountCircle />
              )}
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Navigation Drawer */}
      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        <Drawer
          variant={isMobile ? 'temporary' : 'permanent'}
          open={isMobile ? mobileOpen : true}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true // Better open performance on mobile.
          }}
          sx={{
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
              borderRight: `1px solid ${theme.palette.divider}`
            }
          }}
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${drawerWidth}px)` },
          mt: 8 // Account for AppBar height
        }}
      >
        {children}
      </Box>

      {/* User Menu */}
      <Menu
        anchorEl={userMenuAnchor}
        open={Boolean(userMenuAnchor)}
        onClose={handleUserMenuClose}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem onClick={() => { navigate('/settings'); handleUserMenuClose(); }}>
          <ListItemIcon>
            <AccountCircle fontSize="small" />
          </ListItemIcon>
          Profile
        </MenuItem>
        <MenuItem onClick={() => { navigate('/admin'); handleUserMenuClose(); }}>
          <ListItemIcon>
            <Business fontSize="small" />
          </ListItemIcon>
          Organization
        </MenuItem>
        <Divider />
        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <Logout fontSize="small" />
          </ListItemIcon>
          Logout
        </MenuItem>
      </Menu>

      {/* Notification Center */}
      <NotificationCenter
        anchorEl={notificationAnchor}
        onClose={() => setNotificationAnchor(null)}
      />
    </Box>
  );
}
