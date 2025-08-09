import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Grid,
  Typography,
  Button,
  Paper,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  CircularProgress,
  Divider,
  IconButton
} from '@mui/material'
import {
  ShoppingCart,
  CardGiftcard,
  Download,
  ArrowBack,
  Block
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
import { Book, BookOwnership } from '@/types'
import { booksApi } from '@/services/api/books'
import { usersApi } from '@/services/api/users'
import { useAuth } from '@/context/AuthContext'
import { useCart } from '@/context/CartContext'
import { useNotification } from '@/context/NotificationContext'
import GiftModal from '@/components/GiftModal'
import ReviewSection from '@/components/ReviewSection'

const BookDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { addToCart } = useCart()
  const { showNotification } = useNotification()
  
  const [book, setBook] = useState<Book | null>(null)
  const [owners, setOwners] = useState<BookOwnership[]>([])
  const [isOwned, setIsOwned] = useState(false)
  const [loading, setLoading] = useState(true)
  const [giftModalOpen, setGiftModalOpen] = useState(false)
  const [blockedUsers, setBlockedUsers] = useState<string[]>([])

  useEffect(() => {
    if (id) {
      fetchBookDetails()
    }
  }, [id])

  useEffect(() => {
    if (profile) {
      fetchBlockedUsers()
    }
  }, [profile])

  const fetchBookDetails = async () => {
    try {
      const [bookData, ownersData] = await Promise.all([
        booksApi.getById(id!),
        booksApi.getOwners(id!)
      ])
      
      setBook(bookData)
      setOwners(ownersData)
      
      if (profile) {
        const owns = await booksApi.checkOwnership(id!, profile.id)
        setIsOwned(owns)
      }
    } catch (error) {
      console.error('Error fetching book details:', error)
      navigate('/404')
    } finally {
      setLoading(false)
    }
  }

  const fetchBlockedUsers = async () => {
    if (!profile) return
    try {
      const blocked = await usersApi.getBlockedUsers(profile.id)
      setBlockedUsers(blocked.map(b => b.blocked_id))
    } catch (error) {
      console.error('Error fetching blocked users:', error)
    }
  }

  const handleAddToCart = () => {
    if (book) {
      addToCart(book)
      showNotification(t('bookAddedToCart'), 'success')
    }
  }

  const handleDownload = () => {
    if (book) {
      window.open(book.file_url, '_blank')
    }
  }

  const handleBlockUser = async (userId: string) => {
    if (!profile) return
    
    try {
      const isBlocked = blockedUsers.includes(userId)
      if (isBlocked) {
        await usersApi.unblockUser(profile.id, userId)
        setBlockedUsers(prev => prev.filter(id => id !== userId))
        showNotification('User unblocked', 'success')
      } else {
        await usersApi.blockUser(profile.id, userId)
        setBlockedUsers(prev => [...prev, userId])
        showNotification('User blocked', 'success')
      }
    } catch (error) {
      showNotification('Failed to update block status', 'error')
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  if (!book) {
    return null
  }

  return (
    <Box>
      <Button
        startIcon={<ArrowBack />}
        onClick={() => navigate('/books')}
        sx={{ mb: 2 }}
      >
        Back to Books
      </Button>

      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <img
              src={book.cover_url}
              alt={book.title}
              style={{ width: '100%', height: 'auto', borderRadius: 8 }}
            />
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Typography variant="h4" gutterBottom>
            {book.title}
          </Typography>

          <Box sx={{ mb: 3 }}>
            <Chip
              label={`$${book.price}`}
              color="primary"
              size="medium"
              sx={{ fontWeight: 'bold', fontSize: '1.2rem' }}
            />
          </Box>

          <Typography variant="body1" paragraph>
            {book.description}
          </Typography>

          <Box sx={{ display: 'flex', gap: 2, mb: 4 }}>
            {isOwned ? (
              <Button
                variant="contained"
                size="large"
                startIcon={<Download />}
                onClick={handleDownload}
                fullWidth
              >
                {t('download')}
              </Button>
            ) : (
              <>
                <Button
                  variant="contained"
                  size="large"
                  startIcon={<ShoppingCart />}
                  onClick={handleAddToCart}
                  sx={{ flex: 1 }}
                >
                  {t('addToCart')}
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<CardGiftcard />}
                  onClick={() => setGiftModalOpen(true)}
                >
                  {t('gift')}
                </Button>
              </>
            )}
          </Box>

          {/* Who owns this book */}
          <Paper sx={{ p: 3, mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              {t('whoOwnsThis')}
            </Typography>
            <List>
              {owners.map((ownership) => (
                <ListItem
                  key={ownership.id}
                  secondaryAction={
                    profile && profile.id !== ownership.user_id && (
                      <IconButton
                        edge="end"
                        onClick={() => handleBlockUser(ownership.user_id)}
                        color={blockedUsers.includes(ownership.user_id) ? 'error' : 'default'}
                      >
                        <Block />
                      </IconButton>
                    )
                  }
                >
                  <ListItemAvatar>
                    <Avatar
                      src={ownership.user?.avatar_url}
                      onClick={() => navigate(`/profile/${ownership.user_id}`)}
                      sx={{ cursor: 'pointer' }}
                    >
                      {ownership.user?.username[0].toUpperCase()}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={ownership.user?.username}
                    secondary={
                      <>
                        {format(new Date(ownership.purchase_date), 'MMM dd, yyyy')}
                        {ownership.is_gift && ' • Received as gift'}
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
            {owners.length === 0 && (
              <Typography color="text.secondary">
                No one owns this book yet.
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>

      <Divider sx={{ my: 4 }} />

      {/* Reviews Section */}
      <ReviewSection bookId={book.id} />

      {/* Gift Modal */}
      <GiftModal
        open={giftModalOpen}
        onClose={() => setGiftModalOpen(false)}
        book={book}
      />
    </Box>
  )
}

export default BookDetailPage