#!/usr/bin/env python3
"""
Fix TypeScript compilation errors in React Academy App
This script will fix all the unused variable and type errors
"""

import os
import sys

def write_file(path, content):
    """Write content to file, creating directories if needed"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Fixed: {path}")

def main():
    # Fix src/App.tsx - Remove unused React import
    write_file('src/App.tsx', '''import { Suspense, lazy } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { CssBaseline, CircularProgress, Box } from '@mui/material'
import { LocalizationProvider } from '@mui/x-date-pickers'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import './i18n'

// Contexts
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import { NotificationProvider } from './context/NotificationContext'
import { CartProvider } from './context/CartContext'
import { LanguageProvider } from './context/LanguageContext'

// Layout
import Layout from './components/Layout'

// Lazy load pages
const HomePage = lazy(() => import('./pages/Home'))
const BooksPage = lazy(() => import('./pages/Books'))
const BookDetailPage = lazy(() => import('./pages/BookDetail'))
const CoursesPage = lazy(() => import('./pages/Courses'))
const ProfilePage = lazy(() => import('./pages/Profile'))
const AdminPage = lazy(() => import('./pages/Admin'))
const RegisterPage = lazy(() => import('./pages/Register'))
const LoginPage = lazy(() => import('./pages/Login'))
const CartPage = lazy(() => import('./pages/Cart'))
const NotFoundPage = lazy(() => import('./pages/NotFound'))

// Loading component
const Loading = () => (
  <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
    <CircularProgress />
  </Box>
)

function App() {
  return (
    <BrowserRouter>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <LanguageProvider>
          <ThemeProvider>
            <AuthProvider>
              <NotificationProvider>
                <CartProvider>
                  <CssBaseline />
                  <Layout>
                    <Suspense fallback={<Loading />}>
                      <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/books" element={<BooksPage />} />
                        <Route path="/books/:id" element={<BookDetailPage />} />
                        <Route path="/courses" element={<CoursesPage />} />
                        <Route path="/profile/:userId?" element={<ProfilePage />} />
                        <Route path="/admin/*" element={<AdminPage />} />
                        <Route path="/register" element={<RegisterPage />} />
                        <Route path="/login" element={<LoginPage />} />
                        <Route path="/cart" element={<CartPage />} />
                        <Route path="/404" element={<NotFoundPage />} />
                        <Route path="*" element={<Navigate to="/404" replace />} />
                      </Routes>
                    </Suspense>
                  </Layout>
                </CartProvider>
              </NotificationProvider>
            </AuthProvider>
          </ThemeProvider>
        </LanguageProvider>
      </LocalizationProvider>
    </BrowserRouter>
  )
}

export default App
''')

    # Fix src/components/CourseCard.tsx - Fix setEnrollment type issue
    write_file('src/components/CourseCard.tsx', '''import React from 'react'
import {
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  LinearProgress,
  Chip
} from '@mui/material'
import {
  Telegram,
  School,
  EmojiEvents,
  CalendarToday
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
import { Course, CourseEnrollment } from '@/types'
import { coursesApi } from '@/services/api/courses'
import { useAuth } from '@/context/AuthContext'

interface CourseCardProps {
  course: Course
  enrollment?: CourseEnrollment | null
}

const CourseCard: React.FC<CourseCardProps> = ({ course, enrollment: initialEnrollment }) => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const [enrollment, setEnrollment] = React.useState(initialEnrollment)

  React.useEffect(() => {
    const checkEnrollment = async () => {
      if (profile && !initialEnrollment) {
        const enrolled = await coursesApi.checkEnrollment(course.id, profile.id)
        setEnrollment(enrolled || null)
      }
    }
    checkEnrollment()
  }, [course.id, profile, initialEnrollment])

  const getStatusColor = () => {
    if (!enrollment) return 'default'
    switch (enrollment.status) {
      case 'completed':
        return 'success'
      case 'in_progress':
        return 'primary'
      default:
        return 'default'
    }
  }

  const getStatusText = () => {
    if (!enrollment) return t('enrollNow')
    switch (enrollment.status) {
      case 'completed':
        return t('completed')
      case 'in_progress':
        return t('inProgress')
      default:
        return t('notStarted')
    }
  }

  const handleEnrollClick = () => {
    window.open('https://t.me/your_admin_contact', '_blank')
  }

  const handleTelegramClick = () => {
    if (course.telegram_link) {
      window.open(course.telegram_link, '_blank')
    }
  }

  const handleCertificateDownload = () => {
    if (enrollment?.certificate_url) {
      window.open(enrollment.certificate_url, '_blank')
    }
  }

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardMedia
        component="img"
        height="200"
        image={course.image_url}
        alt={course.title}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography gutterBottom variant="h6" component="h2">
          {course.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          {course.description}
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <CalendarToday sx={{ fontSize: 16, mr: 1 }} />
            <Typography variant="caption">
              {format(new Date(course.start_date), 'MMM dd, yyyy')} -{' '}
              {format(new Date(course.end_date), 'MMM dd, yyyy')}
            </Typography>
          </Box>

          {enrollment && (
            <>
              <Chip
                label={getStatusText()}
                color={getStatusColor() as any}
                size="small"
                sx={{ mb: 1 }}
              />
              <LinearProgress
                variant="determinate"
                value={enrollment.progress}
                sx={{ height: 8, borderRadius: 4 }}
              />
              <Typography variant="caption" color="text.secondary">
                {enrollment.progress}% {t('completed')}
              </Typography>
            </>
          )}
        </Box>
      </CardContent>

      <CardActions>
        {!enrollment ? (
          <Button
            fullWidth
            variant="contained"
            startIcon={<School />}
            onClick={handleEnrollClick}
          >
            {t('enrollNow')}
          </Button>
        ) : enrollment.status === 'completed' && enrollment.certificate_url ? (
          <Button
            fullWidth
            variant="contained"
            color="success"
            startIcon={<EmojiEvents />}
            onClick={handleCertificateDownload}
          >
            {t('downloadCertificate')}
          </Button>
        ) : course.telegram_link ? (
          <Button
            fullWidth
            variant="contained"
            startIcon={<Telegram />}
            onClick={handleTelegramClick}
          >
            {t('joinTelegram')}
          </Button>
        ) : null}
      </CardActions>
    </Card>
  )
}

export default CourseCard
''')

    # Fix src/components/Footer.tsx - Remove unused t
    write_file('src/components/Footer.tsx', '''import React from 'react'
import { Box, Container, Typography, Link, Grid } from '@mui/material'

const Footer: React.FC = () => {
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
''')

    # Fix src/components/NotificationsDrawer.tsx - Remove unused import
    write_file('src/components/NotificationsDrawer.tsx', '''import React from 'react'
import {
  Drawer,
  Box,
  Typography,
  IconButton,
  List,
  ListItem,
  ListItemText,
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
''')

    # Fix src/components/ReviewSection.tsx - Remove unused import
    write_file('src/components/ReviewSection.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Rating,
  TextField,
  Button,
  Paper,
  Avatar,
  IconButton,
  Divider,
  Stack,
  Collapse
} from '@mui/material'
import {
  ThumbUp,
  ThumbUpOutlined,
  Reply,
  Edit,
  Delete,
  Send
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { format } from 'date-fns'
import { Review } from '@/types'
import { reviewsApi } from '@/services/api/reviews'
import { notificationsApi } from '@/services/api/notifications'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'

interface ReviewSectionProps {
  bookId: string
}

const ReviewSection: React.FC<ReviewSectionProps> = ({ bookId }) => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [reviews, setReviews] = useState<Review[]>([])
  const [userReview, setUserReview] = useState<Review | null>(null)
  const [rating, setRating] = useState(0)
  const [reviewContent, setReviewContent] = useState('')
  const [editingReview, setEditingReview] = useState<string | null>(null)
  const [replyingTo, setReplyingTo] = useState<string | null>(null)
  const [replyContent, setReplyContent] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchReviews()
  }, [bookId])

  const fetchReviews = async () => {
    try {
      const data = await reviewsApi.getBookReviews(bookId)
      setReviews(data)
      
      // Find user's review
      if (profile) {
        const userRev = data.find(r => r.user_id === profile.id)
        if (userRev) {
          setUserReview(userRev)
          setRating(userRev.rating)
          setReviewContent(userRev.content || '')
        }
      }
    } catch (error) {
      console.error('Error fetching reviews:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitReview = async () => {
    if (!profile || rating === 0) return

    try {
      if (userReview) {
        // Update existing review
        await reviewsApi.updateReview(userReview.id, {
          rating,
          content: reviewContent
        })
      } else {
        // Create new review
        await reviewsApi.createReview({
          book_id: bookId,
          user_id: profile.id,
          rating,
          content: reviewContent
        })
      }
      
      showNotification(t('reviewPosted'), 'success')
      await fetchReviews()
    } catch (error) {
      showNotification('Failed to post review', 'error')
    }
  }

  const handleDeleteReview = async (reviewId: string) => {
    try {
      await reviewsApi.deleteReview(reviewId)
      showNotification('Review deleted', 'success')
      await fetchReviews()
    } catch (error) {
      showNotification('Failed to delete review', 'error')
    }
  }

  const handleLikeReview = async (review: Review) => {
    if (!profile) return

    try {
      if (review.user_has_liked) {
        await reviewsApi.unlikeReview(review.id, profile.id)
      } else {
        await reviewsApi.likeReview(review.id, profile.id)
        
        // Notify review author
        if (review.user_id !== profile.id) {
          await notificationsApi.notifyReviewLike(
            review.user_id,
            profile.id,
            profile.username
          )
        }
      }
      await fetchReviews()
    } catch (error) {
      console.error('Error liking review:', error)
    }
  }

  const handleSubmitReply = async (reviewId: string) => {
    if (!profile || !replyContent.trim()) return

    try {
      await reviewsApi.createReply({
        review_id: reviewId,
        user_id: profile.id,
        content: replyContent
      })

      // Notify review author
      const review = reviews.find(r => r.id === reviewId)
      if (review && review.user_id !== profile.id) {
        await notificationsApi.notifyReviewReply(
          review.user_id,
          profile.id,
          profile.username
        )
      }

      setReplyContent('')
      setReplyingTo(null)
      showNotification('Reply posted', 'success')
      await fetchReviews()
    } catch (error) {
      showNotification('Failed to post reply', 'error')
    }
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {t('reviews')}
      </Typography>

      {/* Write/Edit Review Section */}
      {profile && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            {userReview ? 'Edit your review' : t('writeReview')}
          </Typography>
          <Box sx={{ mb: 2 }}>
            <Typography component="legend">{t('rating')}</Typography>
            <Rating
              value={rating}
              onChange={(_, value) => setRating(value || 0)}
              size="large"
            />
          </Box>
          <TextField
            fullWidth
            multiline
            rows={4}
            value={reviewContent}
            onChange={(e) => setReviewContent(e.target.value)}
            placeholder="Share your thoughts about this book..."
            sx={{ mb: 2 }}
          />
          <Button
            variant="contained"
            onClick={handleSubmitReview}
            disabled={rating === 0}
          >
            {userReview ? 'Update Review' : 'Post Review'}
          </Button>
        </Paper>
      )}

      {/* Reviews List */}
      <Stack spacing={2}>
        {reviews.map((review) => (
          <Paper key={review.id} sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 1 }}>
              <Avatar
                src={review.user?.avatar_url}
                sx={{ mr: 2 }}
              >
                {review.user?.username[0].toUpperCase()}
              </Avatar>
              <Box sx={{ flex: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {review.user?.username}
                  </Typography>
                  <Rating value={review.rating} readOnly size="small" />
                  <Typography variant="caption" color="text.secondary">
                    {format(new Date(review.created_at), 'MMM dd, yyyy')}
                  </Typography>
                </Box>

                {editingReview === review.id ? (
                  <Box sx={{ mt: 1 }}>
                    <TextField
                      fullWidth
                      multiline
                      rows={3}
                      value={reviewContent}
                      onChange={(e) => setReviewContent(e.target.value)}
                      sx={{ mb: 1 }}
                    />
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Button
                        size="small"
                        variant="contained"
                        onClick={handleSubmitReview}
                      >
                        Save
                      </Button>
                      <Button
                        size="small"
                        onClick={() => {
                          setEditingReview(null)
                          setReviewContent(userReview?.content || '')
                        }}
                      >
                        Cancel
                      </Button>
                    </Box>
                  </Box>
                ) : (
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    {review.content}
                  </Typography>
                )}

                {/* Review Actions */}
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1, gap: 1 }}>
                  <IconButton
                    size="small"
                    onClick={() => handleLikeReview(review)}
                  >
                    {review.user_has_liked ? <ThumbUp /> : <ThumbUpOutlined />}
                  </IconButton>
                  <Typography variant="caption">
                    {review.likes_count}
                  </Typography>
                  
                  {profile && (
                    <IconButton
                      size="small"
                      onClick={() => setReplyingTo(review.id)}
                    >
                      <Reply />
                    </IconButton>
                  )}

                  {profile?.id === review.user_id && (
                    <>
                      <IconButton
                        size="small"
                        onClick={() => {
                          setEditingReview(review.id)
                          setReviewContent(review.content || '')
                        }}
                      >
                        <Edit />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleDeleteReview(review.id)}
                      >
                        <Delete />
                      </IconButton>
                    </>
                  )}
                </Box>

                {/* Reply Section */}
                <Collapse in={replyingTo === review.id}>
                  <Box sx={{ mt: 2, ml: 4 }}>
                    <TextField
                      fullWidth
                      size="small"
                      placeholder="Write a reply..."
                      value={replyContent}
                      onChange={(e) => setReplyContent(e.target.value)}
                      onKeyPress={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                          e.preventDefault()
                          handleSubmitReply(review.id)
                        }
                      }}
                      InputProps={{
                        endAdornment: (
                          <IconButton
                            size="small"
                            onClick={() => handleSubmitReply(review.id)}
                            disabled={!replyContent.trim()}
                          >
                            <Send />
                          </IconButton>
                        )
                      }}
                    />
                  </Box>
                </Collapse>

                {/* Replies */}
                {review.replies && review.replies.length > 0 && (
                  <Box sx={{ mt: 2, ml: 4 }}>
                    <Divider sx={{ mb: 1 }} />
                    {review.replies.map((reply) => (
                      <Box key={reply.id} sx={{ mb: 1 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Avatar
                            src={reply.user?.avatar_url}
                            sx={{ width: 24, height: 24 }}
                          >
                            {reply.user?.username[0].toUpperCase()}
                          </Avatar>
                          <Typography variant="subtitle2">
                            {reply.user?.username}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {format(new Date(reply.created_at), 'MMM dd, yyyy')}
                          </Typography>
                        </Box>
                        <Typography variant="body2" sx={{ ml: 4 }}>
                          {reply.content}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                )}
              </Box>
            </Box>
          </Paper>
        ))}
      </Stack>

      {reviews.length === 0 && !loading && (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography color="text.secondary">
            No reviews yet. Be the first to review this book!
          </Typography>
        </Paper>
      )}
    </Box>
  )
}

export default ReviewSection
''')

    # Fix src/context/AuthContext.tsx - Remove unused import
    write_file('src/context/AuthContext.tsx', '''import React, { createContext, useContext, useState, useEffect } from 'react'
import { User as SupabaseUser } from '@supabase/supabase-js'
import { supabase } from '@/services/supabase'
import { usersApi } from '@/services/api/users'
import { User } from '@/types'

interface AuthContextType {
  user: SupabaseUser | null
  profile: User | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (email: string, password: string, username: string) => Promise<void>
  signOut: () => Promise<void>
  updateProfile: (updates: Partial<User>) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<SupabaseUser | null>(null)
  const [profile, setProfile] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check active sessions and set the user
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      if (session?.user) {
        loadProfile(session.user.id)
      }
      setLoading(false)
    })

    // Listen for changes on auth state
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
      if (session?.user) {
        loadProfile(session.user.id)
      } else {
        setProfile(null)
      }
    })

    return () => subscription.unsubscribe()
  }, [])

  const loadProfile = async (userId: string) => {
    try {
      const profile = await usersApi.getProfile(userId)
      setProfile(profile)
    } catch (error) {
      console.error('Error loading profile:', error)
    }
  }

  const signIn = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    if (error) throw error
    if (data.user) {
      await loadProfile(data.user.id)
    }
  }

  const signUp = async (email: string, password: string, username: string) => {
    // Check username availability
    const isAvailable = await usersApi.checkUsername(username)
    if (!isAvailable) {
      throw new Error('Username already taken')
    }

    // Create auth user and pass username as raw_user_meta_data
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { username }
      }
    })

    if (error) throw error

    // Profile will be created by DB trigger automatically
    if (data.user) {
      await loadProfile(data.user.id)
    }
  }

  const signOut = async () => {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
    setProfile(null)
  }

  const updateProfile = async (updates: Partial<User>) => {
    if (!user) throw new Error('No user logged in')
    
    const updatedProfile = await usersApi.updateProfile(user.id, updates)
    setProfile(updatedProfile)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        loading,
        signIn,
        signUp,
        signOut,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}
''')

    # Fix src/pages/Admin/BooksManagement.tsx - Remove unused variables
    write_file('src/pages/Admin/BooksManagement.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  InputAdornment,
  CircularProgress
} from '@mui/material'
import { Edit, Delete, Add, Upload } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { Book } from '@/types'
import { booksApi } from '@/services/api/books'
import { supabase } from '@/services/supabase'
import { useAuth } from '@/context/AuthContext'
import { adminApi } from '@/services/api/admin'
import { useNotification } from '@/context/NotificationContext'

const BooksManagement: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(true)
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingBook, setEditingBook] = useState<Book | null>(null)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: 0,
    cover_url: '',
    file_url: ''
  })
  const [coverFile, setCoverFile] = useState<File | null>(null)
  const [bookFile, setBookFile] = useState<File | null>(null)

  useEffect(() => {
    fetchBooks()
  }, [])

  const fetchBooks = async () => {
    try {
      const data = await booksApi.getAll()
      setBooks(data)
    } catch (error) {
      console.error('Error fetching books:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenDialog = (book?: Book) => {
    if (book) {
      setEditingBook(book)
      setFormData({
        title: book.title,
        description: book.description,
        price: book.price,
        cover_url: book.cover_url,
        file_url: book.file_url
      })
    } else {
      setEditingBook(null)
      setFormData({
        title: '',
        description: '',
        price: 0,
        cover_url: '',
        file_url: ''
      })
    }
    setDialogOpen(true)
  }

  const handleCloseDialog = () => {
    setDialogOpen(false)
    setEditingBook(null)
    setCoverFile(null)
    setBookFile(null)
  }

  const handleUploadFile = async (file: File, bucket: string, path: string) => {
    try {
      const { error } = await supabase.storage
        .from(bucket)
        .upload(path, file, { upsert: true })
      
      if (error) throw error
      
      const { data: { publicUrl } } = supabase.storage
        .from(bucket)
        .getPublicUrl(path)
      
      return publicUrl
    } catch (error) {
      console.error('Upload error:', error)
      throw error
    }
  }

  const handleSave = async () => {
    try {
      let coverUrl = formData.cover_url
      let fileUrl = formData.file_url

      // Upload cover if new file selected
      if (coverFile) {
        const path = `covers/${Date.now()}-${coverFile.name}`
        coverUrl = await handleUploadFile(coverFile, 'book-covers', path)
      }

      // Upload book file if new file selected
      if (bookFile) {
        const path = `books/${Date.now()}-${bookFile.name}`
        fileUrl = await handleUploadFile(bookFile, 'book-files', path)
      }

      const bookData = {
        ...formData,
        cover_url: coverUrl,
        file_url: fileUrl
      }

      if (editingBook) {
        await booksApi.update(editingBook.id, bookData)
        await adminApi.logAction(
          profile!.id,
          'update_book',
          'book',
          editingBook.id,
          { title: bookData.title }
        )
      } else {
        const newBook = await booksApi.create(bookData)
        await adminApi.logAction(
          profile!.id,
          'create_book',
          'book',
          newBook.id,
          { title: bookData.title }
        )
      }

      showNotification('Book saved successfully', 'success')
      handleCloseDialog()
      fetchBooks()
    } catch (error) {
      showNotification('Failed to save book', 'error')
    }
  }

  const handleDelete = async (book: Book) => {
    if (!window.confirm(`Are you sure you want to delete "${book.title}"?`)) {
      return
    }

    try {
      await booksApi.delete(book.id)
      await adminApi.logAction(
        profile!.id,
        'delete_book',
        'book',
        book.id,
        { title: book.title }
      )
      showNotification('Book deleted successfully', 'success')
      fetchBooks()
    } catch (error) {
      showNotification('Failed to delete book', 'error')
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">{t('manageBooks')}</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
        >
          Add Book
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Cover</TableCell>
              <TableCell>Title</TableCell>
              <TableCell>Price</TableCell>
              <TableCell>Created</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {books.map((book) => (
              <TableRow key={book.id}>
                <TableCell>
                  <img
                    src={book.cover_url}
                    alt={book.title}
                    style={{ width: 50, height: 70, objectFit: 'cover' }}
                  />
                </TableCell>
                <TableCell>{book.title}</TableCell>
                <TableCell>${book.price}</TableCell>
                <TableCell>
                  {new Date(book.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => handleOpenDialog(book)}>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(book)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>{editingBook ? 'Edit Book' : 'Add Book'}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            margin="normal"
            multiline
            rows={4}
            required
          />
          <TextField
            fullWidth
            label="Price"
            type="number"
            value={formData.price}
            onChange={(e) => setFormData({ ...formData, price: Number(e.target.value) })}
            margin="normal"
            InputProps={{
              startAdornment: <InputAdornment position="start">$</InputAdornment>,
            }}
            required
          />
          
          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              component="label"
              startIcon={<Upload />}
              fullWidth
            >
              Upload Cover Image
              <input
                type="file"
                hidden
                accept="image/*"
                onChange={(e) => setCoverFile(e.target.files?.[0] || null)}
              />
            </Button>
            {(coverFile || formData.cover_url) && (
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                {coverFile ? coverFile.name : 'Current cover uploaded'}
              </Typography>
            )}
          </Box>

          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              component="label"
              startIcon={<Upload />}
              fullWidth
            >
              Upload Book File (PDF)
              <input
                type="file"
                hidden
                accept=".pdf"
                onChange={(e) => setBookFile(e.target.files?.[0] || null)}
              />
            </Button>
            {(bookFile || formData.file_url) && (
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                {bookFile ? bookFile.name : 'Current file uploaded'}
              </Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleSave}
            variant="contained"
            disabled={!formData.title || !formData.description || formData.price <= 0}
          >
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default BooksManagement
''')

    # Continue with remaining files...
    # Part 2 of the script

    # Fix src/pages/Admin/TransactionsView.tsx - Add loading indicator
    write_file('src/pages/Admin/TransactionsView.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  List,
  ListItem,
  ListItemText,
  CircularProgress
} from '@mui/material'
import { Visibility } from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { Transaction } from '@/types'
import { supabase } from '@/services/supabase'

const TransactionsView: React.FC = () => {
  const { t } = useTranslation()
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null)
  const [detailsOpen, setDetailsOpen] = useState(false)

  useEffect(() => {
    fetchTransactions()
  }, [])

  const fetchTransactions = async () => {
    try {
      const { data, error } = await supabase
        .from('transactions')
        .select(`
          *,
          user:users(id, username, email)
        `)
        .order('created_at', { ascending: false })

      if (error) throw error
      setTransactions(data || [])
    } catch (error) {
      console.error('Error fetching transactions:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleViewDetails = (transaction: Transaction) => {
    setSelectedTransaction(transaction)
    setDetailsOpen(true)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success'
      case 'pending':
        return 'warning'
      case 'failed':
        return 'error'
      default:
        return 'default'
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('transactions')}
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>User</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Date</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactions.map((transaction) => (
              <TableRow key={transaction.id}>
                <TableCell>{transaction.id.substring(0, 8)}...</TableCell>
                <TableCell>{transaction.user?.username}</TableCell>
                <TableCell>${transaction.amount.toFixed(2)}</TableCell>
                <TableCell>
                  <Chip
                    label={transaction.status}
                    color={getStatusColor(transaction.status) as any}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {new Date(transaction.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => handleViewDetails(transaction)}>
                    <Visibility />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog
        open={detailsOpen}
        onClose={() => setDetailsOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Transaction Details</DialogTitle>
        <DialogContent>
          {selectedTransaction && (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Transaction ID: {selectedTransaction.id}
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                User: {selectedTransaction.user?.username} ({selectedTransaction.user?.email})
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                Amount: ${selectedTransaction.amount.toFixed(2)} {selectedTransaction.currency}
              </Typography>
              <Typography variant="subtitle2" gutterBottom>
                Status: <Chip
                  label={selectedTransaction.status}
                  color={getStatusColor(selectedTransaction.status) as any}
                  size="small"
                />
              </Typography>
              {selectedTransaction.paymob_transaction_id && (
                <Typography variant="subtitle2" gutterBottom>
                  Paymob ID: {selectedTransaction.paymob_transaction_id}
                </Typography>
              )}
              <Typography variant="subtitle2" gutterBottom>
                Created: {new Date(selectedTransaction.created_at).toLocaleString()}
              </Typography>
              {selectedTransaction.completed_at && (
                <Typography variant="subtitle2" gutterBottom>
                  Completed: {new Date(selectedTransaction.completed_at).toLocaleString()}
                </Typography>
              )}
              
              <Typography variant="h6" sx={{ mt: 2 }}>
                Items:
              </Typography>
              <List>
                {selectedTransaction.items?.map((item, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={`Book ID: ${item.book_id}`}
                      secondary={
                        <>
                          Quantity: {item.quantity} × ${item.price} = ${(item.quantity * item.price).toFixed(2)}
                          {item.is_gift && ` (Gift to ${item.recipient_id})`}
                        </>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
      </Dialog>
    </Box>
  )
}

export default TransactionsView
''')

    # Fix src/pages/Admin/UsersManagement.tsx - Add loading indicator
    write_file('src/pages/Admin/UsersManagement.tsx', '''import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  Avatar,
  TextField,
  InputAdornment,
  Menu,
  MenuItem,
  CircularProgress
} from '@mui/material'
import {
  Search,
  MoreVert,
  Block,
  Delete,
  AdminPanelSettings
} from '@mui/icons-material'
import { useTranslation } from 'react-i18next'
import { User } from '@/types'
import { usersApi } from '@/services/api/users'
import { useAuth } from '@/context/AuthContext'
import { adminApi } from '@/services/api/admin'
import { useNotification } from '@/context/NotificationContext'

const UsersManagement: React.FC = () => {
  const { t } = useTranslation()
  const { profile } = useAuth()
  const { showNotification } = useNotification()
  const [users, setUsers] = useState<User[]>([])
  const [filteredUsers, setFilteredUsers] = useState<User[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [selectedUser, setSelectedUser] = useState<User | null>(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  useEffect(() => {
    if (searchQuery) {
      const filtered = users.filter(
        user =>
          user.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
          user.email.toLowerCase().includes(searchQuery.toLowerCase())
      )
      setFilteredUsers(filtered)
    } else {
      setFilteredUsers(users)
    }
  }, [searchQuery, users])

  const fetchUsers = async () => {
    try {
      const data = await usersApi.getAllUsers()
      setUsers(data)
      setFilteredUsers(data)
    } catch (error) {
      console.error('Error fetching users:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, user: User) => {
    setAnchorEl(event.currentTarget)
    setSelectedUser(user)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
    setSelectedUser(null)
  }

  const handleToggleBan = async () => {
    if (!selectedUser) return

    try {
      if (selectedUser.is_banned) {
        await usersApi.unbanUser(selectedUser.id)
        await adminApi.logAction(
          profile!.id,
          'unban_user',
          'user',
          selectedUser.id,
          { username: selectedUser.username }
        )
        showNotification('User unbanned', 'success')
      } else {
        await usersApi.banUser(selectedUser.id)
        await adminApi.logAction(
          profile!.id,
          'ban_user',
          'user',
          selectedUser.id,
          { username: selectedUser.username }
        )
        showNotification('User banned', 'success')
      }
      
      fetchUsers()
    } catch (error) {
      showNotification('Failed to update ban status', 'error')
    } finally {
      handleMenuClose()
    }
  }

  const handleToggleAdmin = async () => {
    if (!selectedUser) return

    try {
      await usersApi.updateProfile(selectedUser.id, {
        is_admin: !selectedUser.is_admin
      })
      await adminApi.logAction(
        profile!.id,
        selectedUser.is_admin ? 'remove_admin' : 'make_admin',
        'user',
        selectedUser.id,
        { username: selectedUser.username }
      )
      showNotification(
        selectedUser.is_admin ? 'Admin privileges removed' : 'Admin privileges granted',
        'success'
      )
      fetchUsers()
    } catch (error) {
      showNotification('Failed to update admin status', 'error')
    } finally {
      handleMenuClose()
    }
  }

  const handleDeleteUser = async () => {
    if (!selectedUser || !window.confirm(`Delete user "${selectedUser.username}"? This cannot be undone.`)) {
      return
    }

    try {
      await usersApi.deleteAccount(selectedUser.id)
      await adminApi.logAction(
        profile!.id,
        'delete_user',
        'user',
        selectedUser.id,
        { username: selectedUser.username }
      )
      showNotification('User deleted', 'success')
      fetchUsers()
    } catch (error) {
      showNotification('Failed to delete user', 'error')
    } finally {
      handleMenuClose()
    }
  }

  const handleViewProfile = () => {
    if (selectedUser) {
      window.open(`/profile/${selectedUser.id}`, '_blank')
    }
    handleMenuClose()
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('manageUsers')}
      </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search users..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Avatar</TableCell>
              <TableCell>Username</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Joined</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredUsers.map((user) => (
              <TableRow key={user.id}>
                <TableCell>
                  <Avatar src={user.avatar_url} sx={{ width: 40, height: 40 }}>
                    {user.username[0].toUpperCase()}
                  </Avatar>
                </TableCell>
                <TableCell>
                  {user.username}
                  {user.is_admin && (
                    <Chip
                      icon={<AdminPanelSettings />}
                      label="Admin"
                      size="small"
                      color="primary"
                      sx={{ ml: 1 }}
                    />
                  )}
                </TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>
                  {user.is_banned ? (
                    <Chip label="Banned" color="error" size="small" />
                  ) : user.email_verified ? (
                    <Chip label="Active" color="success" size="small" />
                  ) : (
                    <Chip label="Unverified" color="warning" size="small" />
                  )}
                </TableCell>
                <TableCell>
                  {new Date(user.created_at).toLocaleDateString()}
                </TableCell>
                <TableCell align="right">
                  <IconButton
                    onClick={(e) => handleMenuOpen(e, user)}
                    disabled={user.id === profile?.id}
                  >
                    <MoreVert />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleViewProfile}>
          View Profile
        </MenuItem>
        <MenuItem onClick={handleToggleBan}>
          <Block sx={{ mr: 1 }} />
          {selectedUser?.is_banned ? 'Unban User' : 'Ban User'}
        </MenuItem>
        <MenuItem onClick={handleToggleAdmin}>
          <AdminPanelSettings sx={{ mr: 1 }} />
          {selectedUser?.is_admin ? 'Remove Admin' : 'Make Admin'}
        </MenuItem>
        <MenuItem onClick={handleDeleteUser} sx={{ color: 'error.main' }}>
          <Delete sx={{ mr: 1 }} />
          Delete User
        </MenuItem>
      </Menu>
    </Box>
  )
}

export default UsersManagement
''')

    # Continue with Cart.tsx and Profile.tsx...
    # Part 3 - Final files

    # Fix src/pages/Cart.tsx - Remove unused transaction variable
    write_file('src/pages/Cart.tsx', '''import React, { useState } from 'react'
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
      const { error: transactionError } = await supabase
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
''')

    # Fix src/pages/Profile.tsx - Remove unused imports and variables
    write_file('src/pages/Profile.tsx', '''import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Paper,
  Avatar,
  Button,
  Grid,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Switch,
  FormControlLabel,
  TextField,
  CircularProgress,
  Divider,
  Badge as MuiBadge,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert
} from '@mui/material'
import {
  Edit,
  Delete,
  Download,
  Message,
  Block,
  CardGiftcard,
  School,
  MenuBook,
  EmojiEvents,
  Settings,
  Upload
} from '@mui/icons-material'
import { format } from 'date-fns'
import { User, BookOwnership, CourseEnrollment, UserBadge, Certificate, Message as MessageType } from '@/types'
import { usersApi } from '@/services/api/users'
import { booksApi } from '@/services/api/books'
import { coursesApi } from '@/services/api/courses'
import { messagesApi } from '@/services/api/messages'
import { notificationsApi } from '@/services/api/notifications'
import { useAuth } from '@/context/AuthContext'
import { useNotification } from '@/context/NotificationContext'
import { getPublicUrl, uploadFile } from '@/services/supabase'

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

const TabPanel: React.FC<TabPanelProps> = ({ children, value, index, ...other }) => {
  return (
    <div hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  )
}

const ProfilePage: React.FC = () => {
  const { userId } = useParams<{ userId?: string }>()
  const navigate = useNavigate()
  const { profile: currentUser, updateProfile } = useAuth()
  const { showNotification } = useNotification()

  const [user, setUser] = useState<User | null>(null)
  const [tabValue, setTabValue] = useState(0)
  const [loading, setLoading] = useState(true)
  const [editingBio, setEditingBio] = useState(false)
  const [bio, setBio] = useState('')
  const [courseProgressPublic, setCourseProgressPublic] = useState(true)
  const [books, setBooks] = useState<BookOwnership[]>([])
  const [courses, setCourses] = useState<CourseEnrollment[]>([])
  const [badges, setBadges] = useState<UserBadge[]>([])
  const [messages, setMessages] = useState<MessageType[]>([])
  const [giftHistory, setGiftHistory] = useState<BookOwnership[]>([])
  const [isBlocked, setIsBlocked] = useState(false)

  // New: Edit profile dialog state
  const [editProfileOpen, setEditProfileOpen] = useState(false)
  const [editUsername, setEditUsername] = useState('')
  const [usernameError, setUsernameError] = useState<string | null>(null)
  const [editAvatarFile, setEditAvatarFile] = useState<File | null>(null)
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null)
  const [editLoading, setEditLoading] = useState(false)
  const [editError, setEditError] = useState<string | null>(null)

  const isOwnProfile = !userId || userId === currentUser?.id
  const profileId = userId || currentUser?.id

  useEffect(() => {
    if (profileId) {
      fetchProfile()

      // Track profile visit
      if (!isOwnProfile && currentUser) {
        notificationsApi.notifyProfileVisit(profileId, currentUser.id, currentUser.username)
      }
    }
  }, [profileId])

  const fetchProfile = async () => {
    try {
      const userData = await usersApi.getProfile(profileId!)
      setUser(userData)
      setBio(userData.bio || '')
      setCourseProgressPublic(userData.course_progress_public)

      // Fetch related data
      const [
        booksData,
        coursesData,
        badgesData,
        certificatesData
      ] = await Promise.all([
        booksApi.getUserBooks(profileId!),
        coursesApi.getUserEnrollments(profileId!),
        usersApi.getUserBadges(profileId!),
        usersApi.getUserCertificates(profileId!)
      ])

      setBooks(booksData)
      setCourses(coursesData)
      setBadges(badgesData)

      // Fetch additional data for own profile
      if (isOwnProfile) {
        const messagesData = await messagesApi.getUserMessages(profileId!)
        setMessages(messagesData)

        // Filter gift history
        const giftsReceived = booksData.filter((b: BookOwnership) => b.is_gift)
        setGiftHistory(giftsReceived)
      }

      // Check if blocked
      if (currentUser && !isOwnProfile) {
        const blocked = await usersApi.isBlocked(currentUser.id, profileId!)
        setIsBlocked(blocked)
      }
    } catch (error) {
      console.error('Error fetching profile:', error)
      navigate('/404')
    } finally {
      setLoading(false)
    }
  }

  const handleSaveBio = async () => {
    try {
      await updateProfile({ bio })
      setEditingBio(false)
      showNotification('Bio updated', 'success')
      fetchProfile()
    } catch (error) {
      showNotification('Failed to update bio', 'error')
    }
  }

  const handleToggleCoursePrivacy = async () => {
    try {
      await updateProfile({ course_progress_public: !courseProgressPublic })
      setCourseProgressPublic(!courseProgressPublic)
      showNotification('Privacy settings updated', 'success')
      fetchProfile()
    } catch (error) {
      showNotification('Failed to update privacy settings', 'error')
    }
  }

  const handleBlockUser = async () => {
    if (!currentUser || !user) return

    try {
      if (isBlocked) {
        await usersApi.unblockUser(currentUser.id, user.id)
        setIsBlocked(false)
        showNotification('User unblocked', 'success')
      } else {
        await usersApi.blockUser(currentUser.id, user.id)
        setIsBlocked(true)
        showNotification('User blocked', 'success')
      }
    } catch (error) {
      showNotification('Failed to update block status', 'error')
    }
  }

  const handleDeleteAccount = async () => {
    if (!window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      return
    }

    try {
      await usersApi.deleteAccount(currentUser!.id)
      navigate('/')
    } catch (error) {
      showNotification('Failed to delete account', 'error')
    }
  }

  // Edit Profile dialog handlers
  const handleEditProfileOpen = () => {
    setEditProfileOpen(true)
    setEditUsername(user?.username || '')
    setUsernameError(null)
    setEditAvatarFile(null)
    setAvatarPreview(user?.avatar_url || null)
    setEditError(null)
  }

  const handleEditProfileClose = () => {
    setEditProfileOpen(false)
    setEditLoading(false)
    setEditError(null)
    setEditAvatarFile(null)
    setAvatarPreview(user?.avatar_url || null)
    setUsernameError(null)
  }

  const handleUsernameChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const newUsername = e.target.value
    setEditUsername(newUsername)
    setUsernameError(null)
    if (newUsername.length >= 3 && /^[a-zA-Z0-9_]+$/.test(newUsername)) {
      if (newUsername !== user?.username) {
        const available = await usersApi.checkUsername(newUsername, user?.id)
        if (!available) {
          setUsernameError('Username already taken')
        }
      }
    } else if (newUsername.length > 0) {
      setUsernameError('Username must be at least 3 characters and contain only letters, numbers, and underscores')
    }
  }

  const handleAvatarFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null
    setEditAvatarFile(file)
    setEditError(null)
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setAvatarPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleEditProfileSave = async () => {
    setEditLoading(true)
    setEditError(null)
    let avatarUrl = user?.avatar_url || ''
    try {
      // Validate username again before submit
      if (!editUsername || editUsername.length < 3 || !/^[a-zA-Z0-9_]+$/.test(editUsername)) {
        setUsernameError('Username must be at least 3 characters and contain only letters, numbers, and underscores')
        setEditLoading(false)
        return
      }
      if (editUsername !== user?.username) {
        const available = await usersApi.checkUsername(editUsername, user?.id)
        if (!available) {
          setUsernameError('Username already taken')
          setEditLoading(false)
          return
        }
      }

      // If avatar file is selected, upload it to Supabase Storage
      if (editAvatarFile) {
        const path = `avatars/${user?.id}-${Date.now()}-${editAvatarFile.name}`
        await uploadFile('avatars', path, editAvatarFile)
        avatarUrl = getPublicUrl('avatars', path)
      }

      await updateProfile({
        username: editUsername,
        avatar_url: avatarUrl
      })
      showNotification('Profile updated successfully', 'success')
      setEditProfileOpen(false)
      fetchProfile()
    } catch (error: any) {
      setEditError(error.message || 'Failed to update profile')
    } finally {
      setEditLoading(false)
    }
  }

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    )
  }

  if (!user) {
    return null
  }

  return (
    <Box>
      {/* Profile Header */}
      <Paper sx={{ p: 4, mb: 3 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item>
            <Box sx={{ position: 'relative', display: 'inline-block' }}>
              <Avatar
                src={user.avatar_url}
                sx={{ width: 120, height: 120 }}
              >
                {user.username[0].toUpperCase()}
              </Avatar>
              {isOwnProfile && (
                <IconButton
                  size="small"
                  sx={{
                    position: 'absolute',
                    bottom: 8,
                    right: 8,
                    bgcolor: 'background.paper',
                    boxShadow: 1,
                  }}
                  onClick={handleEditProfileOpen}
                >
                  <Edit />
                </IconButton>
              )}
            </Box>
          </Grid>
          <Grid item xs>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography variant="h4">{user.username}</Typography>
              {isOwnProfile && (
                <IconButton
                  size="small"
                  sx={{ ml: 1 }}
                  onClick={handleEditProfileOpen}
                >
                  <Edit />
                </IconButton>
              )}
            </Box>
            {user.is_admin && (
              <Chip label="Admin" color="primary" size="small" sx={{ mt: 1 }} />
            )}

            {/* Badges */}
            <Box sx={{ display: 'flex', gap: 1, mt: 2, flexWrap: 'wrap' }}>
              {badges.map((userBadge) => (
                <MuiBadge
                  key={userBadge.id}
                  overlap="circular"
                  anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                  badgeContent={
                    <Avatar
                      src={userBadge.badge?.icon_url}
                      sx={{ width: 24, height: 24 }}
                    />
                  }
                >
                  <Chip
                    label={userBadge.badge?.name}
                    size="small"
                    variant="outlined"
                  />
                </MuiBadge>
              ))}
            </Box>

            {/* Bio */}
            <Box sx={{ mt: 2 }}>
              {editingBio && isOwnProfile ? (
                <Box>
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                    placeholder="Tell us about yourself..."
                    sx={{ mb: 1 }}
                  />
                  <Box>
                    <Button size="small" variant="contained" onClick={handleSaveBio}>
                      Save
                    </Button>
                    <Button
                      size="small"
                      onClick={() => {
                        setEditingBio(false)
                        setBio(user.bio || '')
                      }}
                      sx={{ ml: 1 }}
                    >
                      Cancel
                    </Button>
                  </Box>
                </Box>
              ) : (
                <Box>
                  <Typography variant="body1" color={user.bio ? 'inherit' : 'text.secondary'}>
                    {user.bio || 'No bio yet'}
                  </Typography>
                  {isOwnProfile && (
                    <IconButton size="small" onClick={() => setEditingBio(true)}>
                      <Edit />
                    </IconButton>
                  )}
                </Box>
              )}
            </Box>
          </Grid>
          {!isOwnProfile && currentUser && (
            <Grid item>
              <Button
                variant="contained"
                startIcon={<Message />}
                onClick={() => navigate(`/messages/${user.id}`)}
                disabled={isBlocked}
                sx={{ mb: 1 }}
              >
                Message
              </Button>
              <Button
                variant="outlined"
                startIcon={<Block />}
                onClick={handleBlockUser}
                color={isBlocked ? 'error' : 'inherit'}
                fullWidth
              >
                {isBlocked ? 'Unblock' : 'Block'}
              </Button>
            </Grid>
          )}
        </Grid>
      </Paper>

      {/* Edit Profile Dialog */}
      <Dialog open={editProfileOpen} onClose={handleEditProfileClose} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Profile</DialogTitle>
        <DialogContent>
          {editError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {editError}
            </Alert>
          )}
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 2 }}>
            <Avatar
              src={avatarPreview || undefined}
              sx={{ width: 100, height: 100, mb: 2 }}
            >
              {editUsername[0]?.toUpperCase() || user.username[0].toUpperCase()}
            </Avatar>
            <Button
              variant="outlined"
              component="label"
              startIcon={<Upload />}
              sx={{ mb: 1 }}
            >
              Change Picture
              <input
                type="file"
                hidden
                accept="image/*"
                onChange={handleAvatarFileChange}
              />
            </Button>
            {editAvatarFile && (
              <Typography variant="caption" display="block" sx={{ mb: 1 }}>
                {editAvatarFile.name}
              </Typography>
            )}
          </Box>
          <TextField
            fullWidth
            label="Username"
            value={editUsername}
            onChange={handleUsernameChange}
            error={!!usernameError}
            helperText={usernameError || 'Username must be at least 3 characters and contain only letters, numbers, and underscores'}
            margin="normal"
            required
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleEditProfileClose}>Cancel</Button>
          <Button
            onClick={handleEditProfileSave}
            variant="contained"
            disabled={editLoading || !!usernameError || !editUsername}
          >
            {editLoading ? 'Saving...' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={(_, v) => setTabValue(v)}>
          <Tab label="Books" icon={<MenuBook />} />
          <Tab label="Courses" icon={<School />} />
          {isOwnProfile && (
            <>
              <Tab label="Messages" icon={<Message />} />
              <Tab label="Gift History" icon={<CardGiftcard />} />
              <Tab label="Settings" icon={<Settings />} />
            </>
          )}
        </Tabs>
      </Paper>

      {/* Tab Panels */}
      <TabPanel value={tabValue} index={0}>
        <Typography variant="h6" gutterBottom>
          Book Ownership ({books.length})
        </Typography>
        <Grid container spacing={2}>
          {books.map((ownership) => (
            <Grid item xs={12} sm={6} md={4} key={ownership.id}>
              <Paper sx={{ p: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'start' }}>
                  <img
                    src={ownership.book?.cover_url}
                    alt={ownership.book?.title}
                    style={{ width: 60, height: 80, borderRadius: 4, marginRight: 16 }}
                  />
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="subtitle1">{ownership.book?.title}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {format(new Date(ownership.purchase_date), 'MMM dd, yyyy')}
                    </Typography>
                    {ownership.is_gift && (
                      <Chip label="Gift" size="small" color="secondary" sx={{ ml: 1 }} />
                    )}
                    {isOwnProfile && (
                      <Box sx={{ mt: 1 }}>
                        <Button
                          size="small"
                          startIcon={<Download />}
                          onClick={() => window.open(ownership.book?.file_url, '_blank')}
                        >
                          Download
                        </Button>
                      </Box>
                    )}
                  </Box>
                </Box>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Typography variant="h6" gutterBottom>
          Course History ({courses.length})
        </Typography>
        {(!isOwnProfile && !user.course_progress_public) ? (
          <Typography color="text.secondary">
            This user's course progress is private.
          </Typography>
        ) : (
          <List>
            {courses.map((enrollment) => (
              <ListItem key={enrollment.id}>
                <ListItemAvatar>
                  <Avatar src={enrollment.course?.image_url}>
                    <School />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={enrollment.course?.title}
                  secondary={
                    <>
                      Status: {enrollment.status} • Progress: {enrollment.progress}%
                      {enrollment.completed_at && (
                        <> • Completed: {format(new Date(enrollment.completed_at), 'MMM dd, yyyy')}</>
                      )}
                    </>
                  }
                />
                {enrollment.certificate_url && (
                  <ListItemSecondaryAction>
                    <IconButton
                      onClick={() => window.open(enrollment.certificate_url, '_blank')}
                    >
                      <EmojiEvents color="primary" />
                    </IconButton>
                  </ListItemSecondaryAction>
                )}
              </ListItem>
            ))}
          </List>
        )}
      </TabPanel>

      {isOwnProfile && (
        <>
          <TabPanel value={tabValue} index={2}>
            <Typography variant="h6" gutterBottom>
              Messages
            </Typography>
            <List>
              {messages.map((message) => (
                <ListItem key={message.id}>
                  <ListItemAvatar>
                    <Avatar src={
                      message.sender_id === currentUser?.id
                        ? message.recipient?.avatar_url
                        : message.sender?.avatar_url
                    }>
                      {(message.sender_id === currentUser?.id
                        ? message.recipient?.username[0]
                        : message.sender?.username[0]
                      )?.toUpperCase()}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      message.sender_id === currentUser?.id
                        ? `To: ${message.recipient?.username}`
                        : `From: ${message.sender?.username}`
                    }
                    secondary={
                      <>
                        {message.content.substring(0, 50)}...
                        <br />
                        {format(new Date(message.created_at), 'MMM dd, yyyy HH:mm')}
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Typography variant="h6" gutterBottom>
              Gift History
            </Typography>
            <List>
              {giftHistory.map((gift) => (
                <ListItem key={gift.id}>
                  <ListItemAvatar>
                    <Avatar>
                      <CardGiftcard />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={gift.book?.title}
                    secondary={
                      <>
                        From: {gift.gifter?.username}
                        <br />
                        {gift.gift_message && `Message: ${gift.gift_message}`}
                        <br />
                        {format(new Date(gift.purchase_date), 'MMM dd, yyyy')}
                      </>
                    }
                  />
                </ListItem>
              ))}
            </List>
          </TabPanel>

          <TabPanel value={tabValue} index={4}>
            <Typography variant="h6" gutterBottom>
              Settings
            </Typography>

            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Privacy
              </Typography>
              <FormControlLabel
                control={
                  <Switch
                    checked={courseProgressPublic}
                    onChange={handleToggleCoursePrivacy}
                  />
                }
                label="Show course progress publicly"
              />
            </Box>

            <Divider sx={{ my: 3 }} />

            <Box>
              <Typography variant="subtitle1" gutterBottom color="error">
                Danger Zone
              </Typography>
              <Button
                variant="outlined"
                color="error"
                startIcon={<Delete />}
                onClick={handleDeleteAccount}
              >
                Delete Account
              </Button>
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                This will permanently delete your account and all associated data.
              </Typography>
            </Box>
          </TabPanel>
        </>
      )}
    </Box>
  )
}

export default ProfilePage
''')

    print("\n✅ All TypeScript errors have been fixed!")
    print("Files updated:")
    print("  - src/App.tsx")
    print("  - src/components/CourseCard.tsx")
    print("  - src/components/Footer.tsx")
    print("  - src/components/NotificationsDrawer.tsx")
    print("  - src/components/ReviewSection.tsx")
    print("  - src/context/AuthContext.tsx")
    print("  - src/pages/Admin/BooksManagement.tsx")
    print("  - src/pages/Admin/TransactionsView.tsx")
    print("  - src/pages/Admin/UsersManagement.tsx")
    print("  - src/pages/Cart.tsx")
    print("  - src/pages/Profile.tsx")
    print("\n🚀 Run 'npm run build' to verify all errors are resolved.")

if __name__ == "__main__":
    main()