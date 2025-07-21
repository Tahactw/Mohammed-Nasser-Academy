import React, { useState, useEffect } from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Autocomplete,
  Box,
  Typography,
  Alert
} from '@mui/material'
import { useTranslation } from 'react-i18next'
import { Book, User } from '@/types'
import { usersApi } from '@/services/api/users'
import { booksApi } from '@/services/api/books'
import { notificationsApi } from '@/services/api/notifications'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

interface GiftModalProps {
  open: boolean
  onClose: () => void
  book: Book
}

const GiftModal: React.FC<GiftModalProps> = ({ open, onClose, book }) => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [users, setUsers] = useState<User[]>([])
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const allUsers = await usersApi.getAllUsers()
        // Filter out current user and banned users
        const filteredUsers = allUsers.filter(
          u => u.id !== profile?.id && !u.is_banned
        )
        setUsers(filteredUsers)
      } catch (err) {
        console.error('Error fetching users:', err)
      }
    }

    if (open) {
      fetchUsers()
    }
  }, [open, profile])

  const handleSend = async () => {
    if (!selectedUser || !profile) return

    setLoading(true)
    setError(null)

    try {
      // Check if recipient already owns the book
      const alreadyOwns = await booksApi.checkOwnership(book.id, selectedUser.id)
      if (alreadyOwns) {
        setError('This user already owns this book')
        setLoading(false)
        return
      }

      // Check if blocked
      const isBlocked = await usersApi.isBlocked(selectedUser.id, profile.id)
      if (isBlocked) {
        setError('You cannot send gifts to this user')
        setLoading(false)
        return
      }

      // Send gift
      await booksApi.gift(book.id, selectedUser.id, message, profile.id)

      // Send notification
      await notificationsApi.notifyGiftReceived(
        selectedUser.id,
        profile.id,
        book.title
      )

      showNotification(t('giftSent'), 'success')
      onClose()
      setSelectedUser(null)
      setMessage('')
    } catch (err: any) {
      setError(err.message || 'Failed to send gift')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{t('gift')} - {book.title}</DialogTitle>
      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box sx={{ mt: 2 }}>
          <Autocomplete
            options={users}
            getOptionLabel={(option) => option.username}
            value={selectedUser}
            onChange={(_, value) => setSelectedUser(value)}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Select recipient"
                required
                fullWidth
              />
            )}
            renderOption={(props, option) => (
              <Box component="li" {...props}>
                <Typography>{option.username}</Typography>
              </Box>
            )}
          />

          <TextField
            label="Gift message (optional)"
            multiline
            rows={4}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            fullWidth
            sx={{ mt: 2 }}
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>{t('cancel')}</Button>
        <Button
          onClick={handleSend}
          variant="contained"
          disabled={!selectedUser || loading}
        >
          {loading ? 'Sending...' : 'Send Gift'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}

export default GiftModal