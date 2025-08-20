import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
} from '@mui/material';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import PsychologyIcon from '@mui/icons-material/Psychology';

const Header: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { label: 'Home', path: '/' },
    { label: 'Demo', path: '/demo' },
    { label: 'Graphs', path: '/graphs' },
    { label: 'API Docs', path: '/docs' },
  ];

  return (
    <AppBar position="static" elevation={2}>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <PsychologyIcon sx={{ mr: 2 }} />
          <Typography
            variant="h6"
            component={RouterLink}
            to="/"
            sx={{
              flexGrow: 1,
              textDecoration: 'none',
              color: 'inherit',
              fontWeight: 700,
            }}
          >
            XReason
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 2 }}>
            {navItems.map((item) => (
              <Button
                key={item.path}
                component={RouterLink}
                to={item.path}
                color="inherit"
                sx={{
                  textTransform: 'none',
                  fontWeight: location.pathname === item.path ? 600 : 400,
                  borderBottom: location.pathname === item.path ? '2px solid white' : 'none',
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header;
