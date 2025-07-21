import React from 'react'
import { Link as RouterLink } from 'react-router-dom'
import {
  Box,
  Typography,
  Button,
  Grid,
  Container,
  Paper,
  useTheme
} from '@mui/material'
import {
  MenuBook,
  School,
  PersonAdd,
  Login as LoginIcon
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/context/AuthContext'

const HomePage: React.FC = () => {
  const { t } = useTranslation()
  const theme = useTheme()
  const { profile } = useAuth()

  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          minHeight: '80vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center',
          py: 8,
        }}
      >
        <Typography
          component="h1"
          variant="h2"
          gutterBottom
          sx={{
            fontWeight: 700,
            background: `linear-gradient(45deg, ${theme.palette.primary.main} 30%, ${theme.palette.secondary.main} 90%)`,
            backgroundClip: 'text',
            textFillColor: 'transparent',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          React Academy
        </Typography>

        <Typography
          variant="h5"
          color="text.secondary"
          paragraph
          sx={{ maxWidth: 600, mb: 4 }}
        >
          Your journey to knowledge starts here. Explore our collection of digital books
          and courses designed to help you grow.
        </Typography>

        <Grid container spacing={3} justifyContent="center" sx={{ mb: 6 }}>
          <Grid item>
            <Button
              component={RouterLink}
              to="/books"
              variant="contained"
              size="large"
              startIcon={<MenuBook />}
              sx={{ px: 4, py: 1.5 }}
            >
              {t('books')}
            </Button>
          </Grid>
          <Grid item>
            <Button
              component={RouterLink}
              to="/courses"
              variant="outlined"
              size="large"
              startIcon={<School />}
              sx={{ px: 4, py: 1.5 }}
            >
              {t('courses')}
            </Button>
          </Grid>
          {!profile && (
            <>
              <Grid item>
                <Button
                  component={RouterLink}
                  to="/register"
                  variant="contained"
                  color="secondary"
                  size="large"
                  startIcon={<PersonAdd />}
                  sx={{ px: 4, py: 1.5 }}
                >
                  {t('register')}
                </Button>
              </Grid>
              <Grid item>
                <Button
                  component={RouterLink}
                  to="/login"
                  variant="text"
                  size="large"
                  startIcon={<LoginIcon />}
                  sx={{ px: 4, py: 1.5 }}
                >
                  {t('login')}
                </Button>
              </Grid>
            </>
          )}
        </Grid>

        <Grid container spacing={4} sx={{ mt: 4 }}>
          <Grid item xs={12} md={4}>
            <Paper
              elevation={0}
              sx={{
                p: 3,
                height: '100%',
                backgroundColor: theme.palette.background.default,
              }}
            >
              <MenuBook sx={{ fontSize: 48, color: theme.palette.primary.main, mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Digital Library
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Access a curated collection of books on various topics. Purchase once,
                download forever.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper
              elevation={0}
              sx={{
                p: 3,
                height: '100%',
                backgroundColor: theme.palette.background.default,
              }}
            >
              <School sx={{ fontSize: 48, color: theme.palette.secondary.main, mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Expert-Led Courses
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Join structured courses with expert instructors. Track your progress
                and earn certificates.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper
              elevation={0}
              sx={{
                p: 3,
                height: '100%',
                backgroundColor: theme.palette.background.default,
              }}
            >
              <PersonAdd sx={{ fontSize: 48, color: theme.palette.success.main, mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Community Learning
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Connect with fellow learners, share reviews, and gift books to
                friends and colleagues.
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  )
}

export default HomePage