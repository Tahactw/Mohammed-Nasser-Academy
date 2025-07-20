import { useState } from 'react';
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
