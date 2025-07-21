import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Button,
  Divider,
  TextField,
  Avatar
} from '@mui/material'
import {
  Delete,
  Add,
  Remove,
  ShoppingCartCheckout,
  ArrowBack
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { useCart } from '@/context/CartContext'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'
import { paymobService } from '@/services/paymob'
import { supabase } from '@/services/supabase'

const CartPage: React.FC = () => {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { items, itemCount, total, removeFromCart, updateQuantity, clearCart } = useCart()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [loading, setLoading] = useState(false)

  const handleCheckout = async () => {
    if (!profile) {
      showNotification('Please login to checkout', 'warning')
      navigate('/login')
      return
    }

    if (!profile.email_verified) {
      showNotification('Please verify your email before making purchases', 'warning')
      return
    }

    setLoading(true)
    try {
      // Create transaction items
      const transactionItems = items.flatMap(item => {
        const baseItem = {
          book_id: item.book.id,
          quantity: 1,
          price: item.book.price,
          is_gift: false
        }

        // Add items for purchases
        const purchaseItems = Array(item.quantity - (item.recipients?.length || 0))
          .fill(null)
          .map(() => ({ ...baseItem }))

        // Add items for gifts
        const giftItems = (item.recipients || []).map(recipient => ({
          ...baseItem,
          is_gift: true,
          recipient_id: recipient.userId,
          gift_message: recipient.message
        }))

        return [...purchaseItems, ...giftItems]
      })

      // Create transaction record
      const { data: transaction, error: transactionError } = await supabase
        .from('transactions')
        .insert({
          user_id: profile.id,
          amount: total,
          currency: 'USD',
          status: 'pending',
          items: transactionItems
        })
        .select()
        .single()

      if (transactionError) throw transactionError

      // Initialize Paymob checkout
      const checkoutUrl = await paymobService.initiateCheckout(
        total,
        transactionItems,
        profile.email,
        profile.id
      )

      // Clear cart and redirect to payment
      clearCart()
      window.location.href = checkoutUrl
    } catch (error) {
      console.error('Checkout error:', error)
      showNotification('Failed to initialize checkout', 'error')
    } finally {
      setLoading(false)
    }
  }

  if (items.length === 0) {
    return (
      <Box textAlign="center" py={8}>
        <Typography variant="h5" gutterBottom>
          {t('emptyCart')}
        </Typography>
        <Button
          variant="contained"
          startIcon={<ArrowBack />}
          onClick={() => navigate('/books')}
          sx={{ mt: 2 }}
        >
          Continue Shopping
        </Button>
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('cart')} ({itemCount} items)
      </Typography>

      <Paper sx={{ p: 3 }}>
        <List>
          {items.map((item, index) => (
            <React.Fragment key={item.book.id}>
              {index > 0 && <Divider />}
              <ListItem sx={{ py: 2 }}>
                <ListItemAvatar>
                  <Avatar
                    src={item.book.cover_url}
                    variant="rounded"
                    sx={{ width: 60, height: 80 }}
                  />
                </ListItemAvatar>
                <ListItemText
                  primary={item.book.title}
                  secondary={
                    <>
                      ${item.book.price} each
                      {item.recipients && item.recipients.length > 0 && (
                        <Typography variant="caption" display="block">
                          {item.recipients.length} as gifts
                        </Typography>
                      )}
                    </>
                  }
                  sx={{ ml: 2 }}
                />
                <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
                  <IconButton
                    size="small"
                    onClick={() => updateQuantity(item.book.id, item.quantity - 1)}
                    disabled={item.quantity <= 1}
                  >
                    <Remove />
                  </IconButton>
                  <TextField
                    size="small"
                    value={item.quantity}
                    onChange={(e) => {
                      const value = parseInt(e.target.value) || 0
                      if (value > 0) {
                        updateQuantity(item.book.id, value)
                      }
                    }}
                    inputProps={{ min: 1, style: { textAlign: 'center' } }}
                    sx={{ width: 60, mx: 1 }}
                  />
                  <IconButton
                    size="small"
                    onClick={() => updateQuantity(item.book.id, item.quantity + 1)}
                  >
                    <Add />
                  </IconButton>
                </Box>
                <Typography variant="h6">
                  ${(item.book.price * item.quantity).toFixed(2)}
                </Typography>
                <ListItemSecondaryAction>
                  <IconButton
                    edge="end"
                    onClick={() => removeFromCart(item.book.id)}
                    color="error"
                  >
                    <Delete />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            </React.Fragment>
          ))}
        </List>

        <Divider sx={{ my: 3 }} />

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">
            {t('total')}: ${total.toFixed(2)}
          </Typography>
          <Button
            variant="contained"
            size="large"
            startIcon={<ShoppingCartCheckout />}
            onClick={handleCheckout}
            disabled={loading}
          >
            {loading ? 'Processing...' : t('proceedToPayment')}
          </Button>
        </Box>
      </Paper>
    </Box>
  )
}

export default CartPage