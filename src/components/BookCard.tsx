import React from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Chip
} from '@mui/material'
import { ShoppingCart, CardGiftcard, Download } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { Book } from '@/types'
import { useCart } from '@/context/CartContext'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'
import { booksApi } from '@/services/api/books'
import GiftModal from './GiftModal'

interface BookCardProps {
  book: Book
  owned?: boolean
}

const BookCard: React.FC<BookCardProps> = ({ book, owned = false }) => {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { addToCart } = useCart()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [giftModalOpen, setGiftModalOpen] = React.useState(false)
  const [isOwned, setIsOwned] = React.useState(owned)

  React.useEffect(() => {
    const checkOwnership = async () => {
      if (profile) {
        const owns = await booksApi.checkOwnership(book.id, profile.id)
        setIsOwned(owns)
      }
    }
    checkOwnership()
  }, [book.id, profile])

  const handleAddToCart = () => {
    addToCart(book)
    showNotification(t('bookAddedToCart'), 'success')
  }

  const handleDownload = () => {
    window.open(book.file_url, '_blank')
  }

  return (
    <>
      <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <CardMedia
          component="img"
          height="300"
          image={book.cover_url}
          alt={book.title}
          sx={{ cursor: 'pointer' }}
          onClick={() => navigate(`/books/${book.id}`)}
        />
        <CardContent sx={{ flexGrow: 1 }}>
          <Typography gutterBottom variant="h6" component="h2">
            {book.title}
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              display: '-webkit-box',
              WebkitLineClamp: 3,
              WebkitBoxOrient: 'vertical',
            }}
          >
            {book.description}
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Chip
              label={`$${book.price}`}
              color="primary"
              size="small"
              sx={{ fontWeight: 'bold' }}
            />
          </Box>
        </CardContent>
        <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
          {isOwned ? (
            <Button
              fullWidth
              variant="contained"
              startIcon={<Download />}
              onClick={handleDownload}
            >
              {t('download')}
            </Button>
          ) : (
            <>
              <Button
                variant="contained"
                startIcon={<ShoppingCart />}
                onClick={handleAddToCart}
                sx={{ flex: 1, mr: 1 }}
              >
                {t('addToCart')}
              </Button>
              <Button
                variant="outlined"
                startIcon={<CardGiftcard />}
                onClick={() => setGiftModalOpen(true)}
              >
                {t('gift')}
              </Button>
            </>
          )}
        </CardActions>
      </Card>

      <GiftModal
        open={giftModalOpen}
        onClose={() => setGiftModalOpen(false)}
        book={book}
      />
    </>
  )
}

export default BookCard