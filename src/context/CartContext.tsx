import React, { createContext, useContext, useState, useEffect } from 'react'
import { CartItem, Book } from '@/types'

interface CartContextType {
  items: CartItem[]
  itemCount: number
  total: number
  addToCart: (book: Book, quantity?: number) => void
  removeFromCart: (bookId: string) => void
  updateQuantity: (bookId: string, quantity: number) => void
  addGiftRecipient: (bookId: string, userId: string, message: string) => void
  removeGiftRecipient: (bookId: string, userId: string) => void
  clearCart: () => void
  isInCart: (bookId: string) => boolean
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export const useCart = () => {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}

const CART_STORAGE_KEY = 'academy_cart'

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [items, setItems] = useState<CartItem[]>(() => {
    const saved = localStorage.getItem(CART_STORAGE_KEY)
    return saved ? JSON.parse(saved) : []
  })

  useEffect(() => {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items))
  }, [items])

  const itemCount = items.reduce((sum, item) => sum + item.quantity, 0)
  const total = items.reduce((sum, item) => sum + (item.book.price * item.quantity), 0)

  const addToCart = (book: Book, quantity = 1) => {
    setItems(prev => {
      const existing = prev.find(item => item.book.id === book.id)
      if (existing) {
        return prev.map(item =>
          item.book.id === book.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        )
      }
      return [...prev, { book, quantity, recipients: [] }]
    })
  }

  const removeFromCart = (bookId: string) => {
    setItems(prev => prev.filter(item => item.book.id !== bookId))
  }

  const updateQuantity = (bookId: string, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(bookId)
    } else {
      setItems(prev =>
        prev.map(item =>
          item.book.id === bookId ? { ...item, quantity } : item
        )
      )
    }
  }

  const addGiftRecipient = (bookId: string, userId: string, message: string) => {
    setItems(prev =>
      prev.map(item => {
        if (item.book.id === bookId) {
          const recipients = item.recipients || []
          const existingIndex = recipients.findIndex(r => r.userId === userId)
          
          if (existingIndex >= 0) {
            // Update existing recipient
            recipients[existingIndex] = { userId, message }
          } else {
            // Add new recipient
            recipients.push({ userId, message })
          }
          
          return { ...item, recipients }
        }
        return item
      })
    )
  }

  const removeGiftRecipient = (bookId: string, userId: string) => {
    setItems(prev =>
      prev.map(item => {
        if (item.book.id === bookId) {
          const recipients = (item.recipients || []).filter(r => r.userId !== userId)
          return { ...item, recipients }
        }
        return item
      })
    )
  }

  const clearCart = () => {
    setItems([])
  }

  const isInCart = (bookId: string) => {
    return items.some(item => item.book.id === bookId)
  }

  return (
    <CartContext.Provider
      value={{
        items,
        itemCount,
        total,
        addToCart,
        removeFromCart,
        updateQuantity,
        addGiftRecipient,
        removeGiftRecipient,
        clearCart,
        isInCart
      }}
    >
      {children}
    </CartContext.Provider>
  )
}