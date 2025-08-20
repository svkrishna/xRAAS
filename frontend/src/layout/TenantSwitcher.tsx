/**
 * Tenant Switcher Component
 * Dropdown for switching between available tenants
 */

import React, { useState } from 'react';
import {
  Box,
  Button,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Typography,
  Chip,
  Divider,
  TextField,
  InputAdornment,
  Avatar
} from '@mui/material';
import {
  Business,
  Add,
  Search,
  Star,
  StarBorder
} from '@mui/icons-material';
import { useTenant } from '../auth/TenantProvider';

export function TenantSwitcher() {
  const { currentTenant, availableTenants, switchTenant } = useTenant();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [favorites, setFavorites] = useState<string[]>([]);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
    setSearchTerm('');
  };

  const handleTenantSelect = async (tenantId: string) => {
    try {
      await switchTenant(tenantId);
      handleClose();
    } catch (error) {
      console.error('Failed to switch tenant:', error);
    }
  };

  const handleToggleFavorite = (tenantId: string) => {
    setFavorites(prev => 
      prev.includes(tenantId) 
        ? prev.filter(id => id !== tenantId)
        : [...prev, tenantId]
    );
  };

  const filteredTenants = availableTenants.filter(tenant =>
    tenant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    tenant.slug.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const sortedTenants = filteredTenants.sort((a, b) => {
    const aIsFavorite = favorites.includes(a.id);
    const bIsFavorite = favorites.includes(b.id);
    
    if (aIsFavorite && !bIsFavorite) return -1;
    if (!aIsFavorite && bIsFavorite) return 1;
    
    return a.name.localeCompare(b.name);
  });

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'mission_critical': return 'error';
      case 'enterprise': return 'warning';
      case 'professional': return 'info';
      case 'starter': return 'default';
      default: return 'default';
    }
  };

  return (
    <>
      <Button
        onClick={handleClick}
        startIcon={<Business />}
        endIcon={
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              {currentTenant?.name}
            </Typography>
            <Chip
              label={currentTenant?.subscriptionTier}
              size="small"
              color={getTierColor(currentTenant?.subscriptionTier || 'starter')}
              variant="outlined"
              sx={{ height: 20, fontSize: '0.7rem' }}
            />
          </Box>
        }
        sx={{
          color: 'inherit',
          textTransform: 'none',
          '&:hover': {
            backgroundColor: 'rgba(255, 255, 255, 0.1)'
          }
        }}
      />

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        PaperProps={{
          sx: {
            width: 320,
            maxHeight: 400
          }
        }}
        transformOrigin={{ horizontal: 'left', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'left', vertical: 'bottom' }}
      >
        {/* Header */}
        <Box sx={{ p: 2, pb: 1 }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
            Switch Organization
          </Typography>
          
          <TextField
            size="small"
            placeholder="Search organizations..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search fontSize="small" />
                </InputAdornment>
              )
            }}
            sx={{ width: '100%' }}
          />
        </Box>

        <Divider />

        {/* Tenant List */}
        <Box sx={{ maxHeight: 300, overflow: 'auto' }}>
          {sortedTenants.map((tenant) => {
            const isFavorite = favorites.includes(tenant.id);
            const isCurrent = tenant.id === currentTenant?.id;
            
            return (
              <MenuItem
                key={tenant.id}
                onClick={() => handleTenantSelect(tenant.id)}
                selected={isCurrent}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1,
                  py: 1.5,
                  px: 2,
                  '&.Mui-selected': {
                    backgroundColor: 'primary.main',
                    color: 'primary.contrastText',
                    '&:hover': {
                      backgroundColor: 'primary.dark'
                    }
                  }
                }}
              >
                <Avatar
                  sx={{
                    width: 32,
                    height: 32,
                    bgcolor: isCurrent ? 'primary.contrastText' : 'primary.main',
                    color: isCurrent ? 'primary.main' : 'primary.contrastText',
                    fontSize: '0.875rem'
                  }}
                >
                  {tenant.name.charAt(0).toUpperCase()}
                </Avatar>

                <Box sx={{ flexGrow: 1, minWidth: 0 }}>
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: isCurrent ? 600 : 500,
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap'
                    }}
                  >
                    {tenant.name}
                  </Typography>
                  
                  <Typography
                    variant="caption"
                    sx={{
                      color: isCurrent ? 'primary.contrastText' : 'text.secondary',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 0.5
                    }}
                  >
                    {tenant.slug}
                    {isCurrent && (
                      <Chip
                        label="Current"
                        size="small"
                        color="inherit"
                        variant="outlined"
                        sx={{ height: 16, fontSize: '0.6rem' }}
                      />
                    )}
                  </Typography>
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <Chip
                    label={tenant.subscriptionTier}
                    size="small"
                    color={getTierColor(tenant.subscriptionTier)}
                    variant="outlined"
                    sx={{ height: 20, fontSize: '0.7rem' }}
                  />
                  
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleToggleFavorite(tenant.id);
                    }}
                    sx={{
                      color: isFavorite ? 'warning.main' : 'text.secondary',
                      '&:hover': {
                        color: isFavorite ? 'warning.dark' : 'text.primary'
                      }
                    }}
                  >
                    {isFavorite ? <Star fontSize="small" /> : <StarBorder fontSize="small" />}
                  </IconButton>
                </Box>
              </MenuItem>
            );
          })}
        </Box>

        <Divider />

        {/* Add New Organization */}
        <MenuItem
          onClick={() => {
            // TODO: Implement add organization flow
            handleClose();
          }}
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 1,
            py: 1.5,
            px: 2,
            color: 'primary.main'
          }}
        >
          <ListItemIcon sx={{ minWidth: 32 }}>
            <Add color="primary" />
          </ListItemIcon>
          <ListItemText>
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              Add Organization
            </Typography>
          </ListItemText>
        </MenuItem>
      </Menu>
    </>
  );
}
