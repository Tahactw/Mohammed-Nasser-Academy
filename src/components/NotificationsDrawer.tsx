import React from 'react'
import {
  Drawer,
  Box,
  Typography,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Divider,
  Badge,
  Alert
} from '@mui/material'
import { MarkEmailRead, Delete, Notifications } from '@mui/icons-material'
import { useNotification } from '@/context/NotificationContext'

interface NotificationsDrawerProps {
  open: boolean
  onClose: () => void
}

const NotificationsDrawer: React.FC<NotificationsDrawerProps> = ({ open, onClose }) => {
  const { notifications, markAsRead, deleteNotification, unreadCount } = useNotification()

  return (
    <Drawer anchor="right" open={open} onClose={onClose}>
      <Box sx={{ width: 350, p: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Notifications sx={{ mr: 1 }} color="primary" />
          <Typography variant="h6" sx={{ flexGrow: 1 }}>Notifications</Typography>
          <Badge badgeContent={unreadCount} color="secondary" />
        </Box>
        <Divider sx={{ mb: 2 }} />

        <List>
          {notifications.length === 0 && (
            <Alert severity="info">No notifications yet.</Alert>
          )}
          {notifications.map(n => (
            <React.Fragment key={n.id}>
              <ListItem
                sx={{ bgcolor: n.read_at ? undefined : 'action.selected' }}
                secondaryAction={
                  <>
                    {!n.read_at && (
                      <IconButton onClick={() => markAsRead(n.id)} edge="end" title="Mark as read">
                        <MarkEmailRead color="primary" />
                      </IconButton>
                    )}
                    <IconButton onClick={() => deleteNotification(n.id)} edge="end" title="Delete">
                      <Delete color="error" />
                    </IconButton>
                  </>
                }
              >
                <ListItemText
                  primary={n.title}
                  secondary={
                    <>
                      {n.content}
                      <br />
                      {new Date(n.created_at).toLocaleString()}
                    </>
                  }
                />
              </ListItem>
              <Divider />
            </React.Fragment>
          ))}
        </List>
      </Box>
    </Drawer>
  )
}

export default NotificationsDrawer