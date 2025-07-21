import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Badge,
  Menu,
  MenuItem,
  Box,
  Avatar,
  Divider,
  useTheme,
  useMediaQuery
} from '@mui/material'
import {
  ShoppingCart,
  Brightness4,
  Brightness7,
  Language,
  AccountCircle,
  Notifications,
  AdminPanelSettings,
  Logout
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/context/AuthContext'
import { useCart } from '@/context/CartContext'
import { useTheme as useAppTheme } from '@/context/ThemeContext'
import { useLanguage } from '@/context/LanguageContext'
import { useNotification } from '@/context/NotificationContext'

const Header: React.FC = () => {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { profile, signOut } = useAuth()
  const { itemCount } = useCart()
  const { theme: appTheme, toggleTheme } = useAppTheme()
  const { language, changeLanguage } = useLanguage()
  const { unreadCount } = useNotification()

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [langAnchorEl, setLangAnchorEl] = useState<null | HTMLElement>(null)

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleProfileMenuClose = () => {
    setAnchorEl(null)
  }

  const handleLanguageMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setLangAnchorEl(event.currentTarget)
  }

  const handleLanguageMenuClose = () => {
    setLangAnchorEl(null)
  }

  const handleSignOut = async () => {
    await signOut()
    navigate('/')
    handleProfileMenuClose()
  }

  const handleLanguageChange = (lang: string) => {
    changeLanguage(lang)
    handleLanguageMenuClose()
  }

  return (
    <AppBar position="sticky">
      <Toolbar>
        <Typography
          variant="h6"
          component={Link}
          to="/"
          sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}
        >
          {t('home')}
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Button color="inherit" component={Link} to="/books">
            {t('books')}
          </Button>
          <Button color="inherit" component={Link} to="/courses">
            {t('courses')}
          </Button>

          <IconButton color="inherit" onClick={toggleTheme}>
            {appTheme === 'dark' ? <Brightness7 /> : <Brightness4 />}
          </IconButton>

          <IconButton color="inherit" onClick={handleLanguageMenuOpen}>
            <Language />
          </IconButton>

          <Menu
            anchorEl={langAnchorEl}
            open={Boolean(langAnchorEl)}
            onClose={handleLanguageMenuClose}
          >
            <MenuItem
              onClick={() => handleLanguageChange('en')}
              selected={language === 'en'}
            >
              English
            </MenuItem>
            <MenuItem
              onClick={() => handleLanguageChange('ar')}
              selected={language === 'ar'}
            >
              العربية
            </MenuItem>
          </Menu>

          <IconButton color="inherit" component={Link} to="/cart">
            <Badge badgeContent={itemCount} color="secondary">
              <ShoppingCart />
            </Badge>
          </IconButton>

          {profile ? (
            <>
              <IconButton color="inherit" component={Link} to="/notifications">
                <Badge badgeContent={unreadCount} color="secondary">
                  <Notifications />
                </Badge>
              </IconButton>

              <IconButton
                edge="end"
                onClick={handleProfileMenuOpen}
                color="inherit"
              >
                {profile.avatar_url ? (
                  <Avatar src={profile.avatar_url} sx={{ width: 32, height: 32 }} />
                ) : (
                  <AccountCircle />
                )}
              </IconButton>

              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleProfileMenuClose}
              >
                <MenuItem
                  onClick={() => {
                    navigate(`/profile/${profile.id}`)
                    handleProfileMenuClose()
                  }}
                >
                  {t('profile')}
                </MenuItem>
                {profile.is_admin && (
                  <MenuItem
                    onClick={() => {
                      navigate('/admin')
                      handleProfileMenuClose()
                    }}
                  >
                    <AdminPanelSettings sx={{ mr: 1 }} />
                    {t('admin')}
                  </MenuItem>
                )}
                <Divider />
                <MenuItem onClick={handleSignOut}>
                  <Logout sx={{ mr: 1 }} />
                  {t('logout')}
                </MenuItem>
              </Menu>
            </>
          ) : (
            <>
              <Button color="inherit" component={Link} to="/login">
                {t('login')}
              </Button>
              {!isMobile && (
                <Button
                  color="inherit"
                  component={Link}
                  to="/register"
                  variant="outlined"
                  sx={{ ml: 1 }}
                >
                  {t('register')}
                </Button>
              )}
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Header