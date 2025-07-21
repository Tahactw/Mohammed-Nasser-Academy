import React from 'react'
import { Box, Container, Typography, Link, Grid } from '@mui/material'
import { useTranslation } from 'react-i18next'

const Footer: React.FC = () => {
  const { t } = useTranslation()
  const currentYear = new Date().getFullYear()

  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) =>
          theme.palette.mode === 'light'
            ? theme.palette.grey[200]
            : theme.palette.grey[800],
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              React Academy
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Your journey to knowledge starts here.
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Links
            </Typography>
            <Link href="#" color="inherit" display="block">
              About Us
            </Link>
            <Link href="#" color="inherit" display="block">
              Contact
            </Link>
            <Link href="#" color="inherit" display="block">
              Terms of Service
            </Link>
            <Link href="#" color="inherit" display="block">
              Privacy Policy
            </Link>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Follow Us
            </Typography>
            <Link href="#" color="inherit" display="block">
              Facebook
            </Link>
            <Link href="#" color="inherit" display="block">
              Twitter
            </Link>
            <Link href="#" color="inherit" display="block">
              LinkedIn
            </Link>
            <Link href="#" color="inherit" display="block">
              Instagram
            </Link>
          </Grid>
        </Grid>
        <Box mt={3}>
          <Typography variant="body2" color="text.secondary" align="center">
            © {currentYear} React Academy. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </Box>
  )
}

export default Footer