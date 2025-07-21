import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Box, Typography, Button } from '@mui/material'
import { Home } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'

const NotFoundPage: React.FC = () => {
  const navigate = useNavigate()
  const { t } = useTranslation()

  return (
    <Box
      sx={{
        minHeight: '60vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
      }}
    >
      <Typography variant="h1" component="h1" gutterBottom>
        404
      </Typography>
      <Typography variant="h4" gutterBottom>
        {t('pageNotFound')}
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        The page you are looking for doesn't exist or has been moved.
      </Typography>
      <Button
        variant="contained"
        size="large"
        startIcon={<Home />}
        onClick={() => navigate('/')}
      >
        {t('backToHome')}
      </Button>
    </Box>
  )
}

export default NotFoundPage