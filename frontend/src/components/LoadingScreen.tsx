/**
 * Loading Screen Component
 * Full-screen loading indicator
 */

import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

export function LoadingScreen() {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        gap: 2
      }}
    >
      <CircularProgress size={48} />
      <Typography variant="h6" color="text.secondary">
        Loading XReason...
      </Typography>
    </Box>
  );
}
