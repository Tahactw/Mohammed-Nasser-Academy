import React, { useState } from 'react'
import { Box, Container } from '@mui/material'
import Header from './Header'
import Footer from './Footer'
import NotificationsDrawer from './NotificationsDrawer' // <--- Import the drawer

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [notificationsOpen, setNotificationsOpen] = useState(false)

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header onOpenNotifications={() => setNotificationsOpen(true)} />
      <Box component="main" sx={{ flex: 1, py: 4 }}>
        <Container maxWidth="lg">
          {children}
        </Container>
      </Box>
      <Footer />
      <NotificationsDrawer
        open={notificationsOpen}
        onClose={() => setNotificationsOpen(false)}
      />
    </Box>
  )
}

export default Layout