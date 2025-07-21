import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { Snackbar, Alert, AlertColor } from '@mui/material'
import { notificationsApi } from '@/services/api/notifications'
import { Notification } from '@/types'
import { useAuth } from './AuthContext'


interface NotificationContextType {
  notifications: Notification[]
  unreadCount: number
  showNotification: (message: string, type?: AlertColor) => void
  markAsRead: (id: string) => Promise<void>
  markAllAsRead: () => Promise<void>
  deleteNotification: (id: string) => Promise<void>
  refreshNotifications: () => Promise<void>
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined)

export const useNotification = () => {
  const context = useContext(NotificationContext)
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider')
  }
  return context
}

export const NotificationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth()
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [snackbar, setSnackbar] = useState<{
    open: boolean
    message: string
    type: AlertColor
  }>({
    open: false,
    message: '',
    type: 'info'
  })

  const fetchNotifications = useCallback(async () => {
    if (!user) return

    try {
      const [notifs, count] = await Promise.all([
        notificationsApi.getUserNotifications(user.id),
        notificationsApi.getUnreadCount(user.id)
      ])
      setNotifications(notifs)
      setUnreadCount(count)
    } catch (error) {
      console.error('Error fetching notifications:', error)
    }
  }, [user])

  useEffect(() => {
    fetchNotifications()
    
    // Set up realtime subscription
    if (user) {
      const subscription = supabase
        .channel('notifications')
        .on(
          'postgres_changes',
          {
            event: 'INSERT',
            schema: 'public',
            table: 'notifications',
            filter: `user_id=eq.${user.id}`
          },
          (payload) => {
            setNotifications(prev => [payload.new as Notification, ...prev])
            setUnreadCount(prev => prev + 1)
            showNotification(payload.new.content, 'info')
          }
        )
        .subscribe()

      return () => {
        subscription.unsubscribe()
      }
    }
  }, [user, fetchNotifications])

  const showNotification = (message: string, type: AlertColor = 'info') => {
    setSnackbar({ open: true, message, type })
  }

  const markAsRead = async (id: string) => {
    await notificationsApi.markAsRead(id)
    setNotifications(prev =>
      prev.map(n => (n.id === id ? { ...n, read_at: new Date().toISOString() } : n))
    )
    setUnreadCount(prev => Math.max(0, prev - 1))
  }

  const markAllAsRead = async () => {
    if (!user) return
    await notificationsApi.markAllAsRead(user.id)
    setNotifications(prev =>
      prev.map(n => ({ ...n, read_at: n.read_at || new Date().toISOString() }))
    )
    setUnreadCount(0)
  }

  const deleteNotification = async (id: string) => {
    await notificationsApi.delete(id)
    setNotifications(prev => prev.filter(n => n.id !== id))
  }

  const refreshNotifications = async () => {
    await fetchNotifications()
  }

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        unreadCount,
        showNotification,
        markAsRead,
        markAllAsRead,
        deleteNotification,
        refreshNotifications
      }}
    >
      {children}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
      >
        <Alert
          onClose={() => setSnackbar(prev => ({ ...prev, open: false }))}
          severity={snackbar.type}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </NotificationContext.Provider>
  )
}