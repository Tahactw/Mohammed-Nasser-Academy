import React, { useState, useEffect } from 'react'
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
import { Review, ReviewReply } from '@/types'
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