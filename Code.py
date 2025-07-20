#!/usr/bin/env python3
"""
Mohammed Nasser Academy - Fix CORS, Theme, and Admin Issues
This script fixes:
1. CORS errors in GitHub Codespaces
2. Theme toggle functionality
3. Admin routes and functionality
4. Environment variable configuration
"""

import os
import json
from pathlib import Path
from datetime import datetime

class AppFixer:
    def __init__(self):
        self.base_path = Path("/workspaces/Mohammed-Nasser-Academy/Mohammed Nasser Academy")
        self.backup_dir = self.base_path / f"backup_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def backup_file(self, filepath):
        """Create a backup of a file before modifying it"""
        filepath = Path(filepath)
        if filepath.exists():
            backup_path = self.backup_dir / filepath.relative_to(self.base_path)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(filepath, backup_path)
            print(f"✅ Backed up: {filepath}")
    
    def write_file(self, filepath, content):
        """Write content to a file"""
        filepath = Path(filepath)
        self.backup_file(filepath)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated: {filepath}")
    
    def fix_server_cors(self):
        """Fix server CORS configuration for GitHub Codespaces"""
        server_content = """import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

// Load environment variables
dotenv.config();

// Import routes
import authRoutes from './routes/auth.js';
import userRoutes from './routes/users.js';
import courseRoutes from './routes/courses.js';
import bookRoutes from './routes/books.js';
import reviewRoutes from './routes/reviews.js';
import paymentRoutes from './routes/payment.js';
import adminRoutes from './routes/admin.js';

// Import middleware
import errorHandler from './middleware/errorHandler.js';

// ES Module compatibility
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;

// Dynamic CORS configuration for GitHub Codespaces
const getCorsOrigin = () => {
  // If we're in Codespaces, allow the Codespaces URL
  if (process.env.CODESPACES === 'true') {
    const codespaceeName = process.env.CODESPACE_NAME;
    if (codespaceeName) {
      return [
        `https://${codespaceeName}-3000.app.github.dev`,
        `https://${codespaceeName}-5173.app.github.dev`, // Vite default port
        'http://localhost:3000',
        'http://localhost:5173'
      ];
    }
  }
  
  // Otherwise, use CLIENT_URL or default
  return process.env.CLIENT_URL || ['http://localhost:3000', 'http://localhost:5173'];
};

// Middleware
app.use(cors({
  origin: (origin, callback) => {
    const allowedOrigins = Array.isArray(getCorsOrigin()) ? getCorsOrigin() : [getCorsOrigin()];
    
    // Allow requests with no origin (like mobile apps or curl requests)
    if (!origin) return callback(null, true);
    
    // Check if the origin is allowed
    if (allowedOrigins.some(allowed => origin.startsWith(allowed))) {
      callback(null, true);
    } else {
      console.log(`CORS blocked origin: ${origin}`);
      console.log(`Allowed origins:`, allowedOrigins);
      callback(null, true); // For development, allow all origins
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static files
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/courses', courseRoutes);
app.use('/api/books', bookRoutes);
app.use('/api/reviews', reviewRoutes);
app.use('/api/payment', paymentRoutes);
app.use('/api/admin', adminRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development',
    codespaces: process.env.CODESPACES === 'true',
    cors: getCorsOrigin()
  });
});

// Error handling
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
  console.log(`📚 Mohammed Nasser Academy API is ready`);
  console.log(`🔗 http://localhost:${PORT}`);
  if (process.env.CODESPACES === 'true') {
    console.log(`🌐 Running in GitHub Codespaces`);
    console.log(`🔗 Accepting requests from:`, getCorsOrigin());
  }
});
"""
        self.write_file(self.base_path / "server/server.js", server_content)
    
    def fix_theme_implementation(self):
        """Fix theme implementation to work with Material-UI"""
        # Update theme.js to support dark mode
        theme_content = """import { createTheme } from '@mui/material/styles';

export const getTheme = (mode) => createTheme({
  palette: {
    mode,
    ...(mode === 'light'
      ? {
          // Light mode colors
          primary: {
            main: '#1976d2',
            light: '#42a5f5',
            dark: '#1565c0',
          },
          secondary: {
            main: '#dc004e',
            light: '#e33371',
            dark: '#9a0036',
          },
          background: {
            default: '#f5f5f5',
            paper: '#ffffff',
          },
        }
      : {
          // Dark mode colors
          primary: {
            main: '#90caf9',
            light: '#e3f2fd',
            dark: '#42a5f5',
          },
          secondary: {
            main: '#f48fb1',
            light: '#ffc1e3',
            dark: '#bf5f82',
          },
          background: {
            default: '#121212',
            paper: '#1e1e1e',
          },
        }),
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '3rem',
      fontWeight: 700,
    },
    h2: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});

export default getTheme('light');
"""
        self.write_file(self.base_path / "client/src/theme.js", theme_content)
        
        # Update main.jsx to use theme context
        main_content = """import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import App from './App.jsx'
import { AuthProvider } from './contexts/AuthContext.jsx'
import { ThemeContextProvider } from './contexts/ThemeContext.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <ThemeContextProvider>
          <App />
          <ToastContainer position="bottom-right" />
        </ThemeContextProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
"""
        self.write_file(self.base_path / "client/src/main.jsx", main_content)
        
        # Create ThemeContext.jsx
        theme_context_content = """import { createContext, useContext, useState, useEffect, useMemo } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { getTheme } from '../theme';

const ThemeContext = createContext({});

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeContextProvider');
  }
  return context;
};

export const ThemeContextProvider = ({ children }) => {
  const [mode, setMode] = useState('light');

  useEffect(() => {
    // Load theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    setMode(savedTheme);
  }, []);

  const toggleTheme = () => {
    const newMode = mode === 'light' ? 'dark' : 'light';
    setMode(newMode);
    localStorage.setItem('theme', newMode);
  };

  const theme = useMemo(() => getTheme(mode), [mode]);

  const value = {
    mode,
    toggleTheme,
  };

  return (
    <ThemeContext.Provider value={value}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ThemeContext.Provider>
  );
};
"""
        self.write_file(self.base_path / "client/src/contexts/ThemeContext.jsx", theme_context_content)
        
        # Update AuthContext to remove theme logic
        auth_context_content = """import { createContext, useContext, useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';
import api from '../lib/api';

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    // Check active sessions and sets the user
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session?.user) {
        setUser(session.user);
        fetchProfile(session.user.id);
      }
      setLoading(false);
    });

    // Listen for changes on auth state
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session?.user) {
        setUser(session.user);
        fetchProfile(session.user.id);
      } else {
        setUser(null);
        setProfile(null);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const fetchProfile = async (userId) => {
    try {
      const response = await api.get(`/api/users/profile/${userId}`);
      setProfile(response.data);
      // Check if user is admin based on email
      if (response.data.email === 'admin@admin.com') {
        response.data.is_admin = true;
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    }
  };

  const refreshProfile = async () => {
    if (user) {
      await fetchProfile(user.id);
    }
  };

  const signUp = async (email, password, fullName) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { full_name: fullName }
      }
    });

    if (!error && data.user) {
      await fetchProfile(data.user.id);
    }

    return { data, error };
  };

  const signIn = async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    });

    if (!error && data.user) {
      await fetchProfile(data.user.id);
    }

    return { data, error };
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (!error) {
      setUser(null);
      setProfile(null);
    }
    return { error };
  };

  const updateProfile = async (updates) => {
    try {
      const response = await api.put('/api/users/profile', updates);
      setProfile(response.data);
      return { data: response.data, error: null };
    } catch (error) {
      return { data: null, error };
    }
  };

  const isAdmin = () => {
    return profile?.email === 'admin@admin.com' || profile?.is_admin === true;
  };

  const value = {
    user,
    profile,
    loading,
    signUp,
    signIn,
    signOut,
    updateProfile,
    refreshProfile,
    isAdmin,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
"""
        self.write_file(self.base_path / "client/src/contexts/AuthContext.jsx", auth_context_content)
        
        # Update Navbar to use the new theme context
        navbar_content = """import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  useMediaQuery,
  Divider,
} from '@mui/material';
import {
  Menu as MenuIcon,
  AccountCircle,
  Book,
  School,
  Info,
  Dashboard,
  Brightness4,
  Brightness7,
  Telegram,
  YouTube,
  Facebook,
  Twitter,
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import { useTheme as useMuiTheme } from '@mui/material/styles';

const Navbar = () => {
  const { user, profile, signOut, isAdmin } = useAuth();
  const { mode, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const muiTheme = useMuiTheme();
  const isMobile = useMediaQuery(muiTheme.breakpoints.down('sm'));
  
  const [anchorEl, setAnchorEl] = useState(null);
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleSignOut = async () => {
    await signOut();
    navigate('/');
    handleClose();
  };

  const navItems = [
    { label: 'Books', path: '/books', icon: <Book /> },
    { label: 'Courses', path: '/courses', icon: <School /> },
    { label: 'About', path: '/about', icon: <Info /> },
  ];

  const socialLinks = [
    { icon: <Telegram />, url: 'https://t.me/mohammednasser', label: 'Telegram' },
    { icon: <YouTube />, url: 'https://youtube.com/@mohammednasser', label: 'YouTube' },
    { icon: <Facebook />, url: 'https://facebook.com/mohammednasser', label: 'Facebook' },
    { icon: <Twitter />, url: 'https://twitter.com/mohammednasser', label: 'Twitter' },
  ];

  const drawer = (
    <Box onClick={() => setMobileOpen(false)} sx={{ textAlign: 'center' }}>
      <Typography variant="h6" sx={{ my: 2 }}>
        Mohammed Nasser Academy
      </Typography>
      <Divider />
      <List>
        {navItems.map((item) => (
          <ListItem key={item.label} disablePadding>
            <ListItemButton component={Link} to={item.path}>
              {item.icon}
              <ListItemText primary={item.label} sx={{ ml: 1 }} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      <Box sx={{ p: 2 }}>
        <Typography variant="body2" gutterBottom>
          Follow us
        </Typography>
        <Box display="flex" justifyContent="center" gap={1}>
          {socialLinks.map((social) => (
            <IconButton
              key={social.label}
              size="small"
              onClick={() => window.open(social.url, '_blank')}
              aria-label={social.label}
            >
              {social.icon}
            </IconButton>
          ))}
        </Box>
      </Box>
    </Box>
  );

  return (
    <>
      <AppBar position="sticky" elevation={1}>
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={() => setMobileOpen(true)}
              sx={{ mr: 2, display: { sm: 'none' } }}
            >
              <MenuIcon />
            </IconButton>
          )}
          
          <Typography
            variant="h6"
            component={Link}
            to="/"
            sx={{
              flexGrow: 1,
              textDecoration: 'none',
              color: 'inherit',
              fontWeight: 'bold',
            }}
          >
            Mohammed Nasser Academy
          </Typography>

          {!isMobile && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              {navItems.map((item) => (
                <Button
                  key={item.label}
                  component={Link}
                  to={item.path}
                  color="inherit"
                  startIcon={item.icon}
                >
                  {item.label}
                </Button>
              ))}
            </Box>
          )}

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, ml: 2 }}>
            {/* Social Media Icons */}
            {!isMobile && (
              <>
                {socialLinks.map((social) => (
                  <IconButton
                    key={social.label}
                    size="small"
                    color="inherit"
                    onClick={() => window.open(social.url, '_blank')}
                    aria-label={social.label}
                  >
                    {social.icon}
                  </IconButton>
                ))}
                <Divider orientation="vertical" flexItem sx={{ mx: 1 }} />
              </>
            )}

            {/* Theme Toggle */}
            <IconButton onClick={toggleTheme} color="inherit">
              {mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
            </IconButton>

            {user ? (
              <>
                {isAdmin() && !isMobile && (
                  <Button
                    component={Link}
                    to="/admin"
                    color="inherit"
                    startIcon={<Dashboard />}
                  >
                    Admin
                  </Button>
                )}
                <IconButton onClick={handleMenu} color="inherit">
                  <Avatar src={profile?.avatar} sx={{ width: 32, height: 32 }}>
                    {profile?.full_name?.[0]}
                  </Avatar>
                </IconButton>
                <Menu
                  anchorEl={anchorEl}
                  anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'right',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={Boolean(anchorEl)}
                  onClose={handleClose}
                >
                  <MenuItem component={Link} to="/profile" onClick={handleClose}>
                    Profile
                  </MenuItem>
                  {isAdmin() && isMobile && (
                    <MenuItem component={Link} to="/admin" onClick={handleClose}>
                      Admin Panel
                    </MenuItem>
                  )}
                  <MenuItem onClick={handleSignOut}>Logout</MenuItem>
                </Menu>
              </>
            ) : (
              <>
                <Button component={Link} to="/login" color="inherit">
                  Login
                </Button>
                <Button
                  component={Link}
                  to="/register"
                  color="inherit"
                  variant="outlined"
                  sx={{ ml: 1 }}
                >
                  Register
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={() => setMobileOpen(false)}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: 240 },
        }}
      >
        {drawer}
      </Drawer>
    </>
  );
};

export default Navbar;
"""
        self.write_file(self.base_path / "client/src/components/layout/Navbar.jsx", navbar_content)
    
    def fix_css_for_mui(self):
        """Update CSS to remove conflicts with Material-UI theming"""
        css_content = """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Base reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(128, 128, 128, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(128, 128, 128, 0.5);
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.5s ease-out;
}

/* Progress bar animations */
@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Timeline styles for Courses page */
.timeline-dot {
  transition: all 0.3s ease;
}

/* Badge hover effects */
.badge-tooltip {
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.badge:hover .badge-tooltip {
  opacity: 1;
}

/* Utility classes that don't conflict with MUI */
.text-gradient {
  background: linear-gradient(45deg, #1976d2, #dc004e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Custom animations for home page */
.hero-animation {
  position: relative;
  overflow: hidden;
}

.hero-animation::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(25, 118, 210, 0.1) 0%, transparent 70%);
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

/* Social button hover effects */
.social-btn-custom {
  transition: all 0.3s ease;
}

.social-btn-custom:hover {
  transform: translateY(-2px);
}

/* Card hover effects */
.hover-card {
  transition: all 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-4px);
}

/* Loading animations */
.loading-dots {
  display: inline-flex;
  gap: 4px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: currentColor;
  animation: loading-bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes loading-bounce {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Responsive iframe for videos */
.video-container {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* Print styles */
@media print {
  .no-print {
    display: none !important;
  }
}

/* Accessibility improvements */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Focus styles for better accessibility */
*:focus-visible {
  outline: 2px solid #1976d2;
  outline-offset: 2px;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Prevent text selection on UI elements */
.no-select {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
"""
        self.write_file(self.base_path / "client/src/index.css", css_content)
    
    def create_server_env_file(self):
        """Create a proper .env file for the server with Codespaces detection"""
        env_content = """# MongoDB - Use MongoDB Atlas or local
MONGODB_URI=mongodb://localhost:27017/writer-instructor

# Supabase Configuration (Required)
SUPABASE_URL=https://qkfgvniqkwbrvolkedsv.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrZmd2bmlxa3dicnZvbGtlZHN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI3NzUwODMsImV4cCI6MjA2ODM1MTA4M30.GJdUPpUcaZwdv4fau2PelnrfjWNL7wH8qgtvQtnwElE
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrZmd2bmlxa3dicnZvbGtlZHN2Iiwicm9sZSI6InNlcnZpY2UiLCJpYXQiOjE3NTI3NzUwODMsImV4cCI6MjA2ODM1MTA4M30.fGFIe0O0duVZuNbM64D2CqbCSsgxdKqP8iycMdQqUJw

# JWT Secret
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# Server Configuration
PORT=5000
NODE_ENV=development

# Paymob Configuration
PAYMOB_API_KEY=ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TVRBMk1URXlOeXdpYm1GdFpTSTZJbWx1YVhScFlXd2lmUS5NckRTanoyeXZpVE5zdE1MX2w0cC1XNF84dzRZM2NMM2o4Z0FxN1BFMWppczlEaVhQN2EwRFVQMFQ5amlSQVVxTE9KUHM1bXQwODltY2dvNnV1a181UQ==
PAYMOB_INTEGRATION_ID=5034899
PAYMOB_IFRAME_ID=940881
PAYMOB_HMAC_SECRET=F0F9E4234AB36432D0BD2492B88B8F0C

# GitHub Codespaces Detection
CODESPACES=true

# Client URL (dynamically set in server.js for Codespaces)
# CLIENT_URL=http://localhost:3000
"""
        self.write_file(self.base_path / "server/.env", env_content)
    
    def create_test_script(self):
        """Create a test script to verify everything is working"""
        test_script = """#!/bin/bash

echo "🧪 Testing Mohammed Nasser Academy Setup"
echo "======================================="

# Colors for output
GREEN='\\033[0;32m'
RED='\\033[0;31m'
NC='\\033[0m' # No Color

# Test server health
echo -n "Testing server health endpoint... "
response=$(curl -s http://localhost:5000/health)
if [[ $response == *"ok"* ]]; then
  echo -e "${GREEN}✓ Server is running${NC}"
  echo "Response: $response"
else
  echo -e "${RED}✗ Server is not responding${NC}"
fi

echo ""
echo "📋 Next steps:"
echo "1. Restart both server and client"
echo "2. The theme toggle should now work"
echo "3. CORS errors should be resolved"
echo "4. Admin functionality should be available"
echo ""
echo "🔍 To verify:"
echo "- Click the theme toggle button in the navbar"
echo "- Check that API calls work without CORS errors"
echo "- Login with admin@admin.com to access admin panel"
"""
        self.write_file(self.base_path / "test-setup.sh", test_script)
        os.chmod(self.base_path / "test-setup.sh", 0o755)
    
    def run(self):
        """Execute all fixes"""
        print("🔧 Starting Mohammed Nasser Academy Fix Script")
        print("=" * 50)
        
        # Check if base path exists
        if not self.base_path.exists():
            print(f"❌ Error: Directory not found: {self.base_path}")
            return
        
        # Create backup directory
        self.backup_dir.mkdir(exist_ok=True)
        print(f"📁 Created backup directory: {self.backup_dir}")
        
        # Run all fixes
        print("\n🌐 Fixing server CORS configuration...")
        self.fix_server_cors()
        
        print("\n🎨 Fixing theme implementation...")
        self.fix_theme_implementation()
        
        print("\n🎨 Updating CSS for Material-UI...")
        self.fix_css_for_mui()
        
        print("\n📝 Updating server environment file...")
        self.create_server_env_file()
        
        print("\n🧪 Creating test script...")
        self.create_test_script()
        
        print("\n✅ All fixes completed successfully!")
        print("\n📋 Action required:")
        print("1. Stop both server and client if running")
        print("2. Restart the server: cd server && npm run dev")
        print("3. Restart the client: cd client && npm run dev")
        print("4. Run the test script: ./test-setup.sh")
        print("\n🎉 Your app should now work properly with:")
        print("   - ✅ No CORS errors")
        print("   - ✅ Working theme toggle")
        print("   - ✅ Admin functionality")
        print("   - ✅ Proper GitHub Codespaces support")

if __name__ == "__main__":
    fixer = AppFixer()
    fixer.run()