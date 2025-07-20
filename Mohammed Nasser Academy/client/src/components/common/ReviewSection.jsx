import { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Rating,
  Card,
  CardContent,
  Avatar,
  Divider,
} from '@mui/material';
import { Send } from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { toast } from 'react-toastify';
import api from '../../lib/api';
import { useNavigate } from 'react-router-dom';

const ReviewSection = ({ itemType, itemId, reviews, canReview }) => {
  const { user, profile } = useAuth();
  const navigate = useNavigate();
  const [rating, setRating] = useState(5);
  const [content, setContent] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!user) {
      toast.info('Please login to leave a review');
      navigate('/login');
      return;
    }

    if (!canReview) {
      toast.error(`You must purchase this ${itemType} to leave a review`);
      return;
    }

    setSubmitting(true);
    try {
      await api.post('/api/reviews', {
        itemType,
        itemId,
        rating,
        content,
        userId: user.id,
      });

      toast.success('Review submitted successfully');
      setContent('');
      setRating(5);
      // Refresh page to show new review
      window.location.reload();
    } catch (error) {
      toast.error('Failed to submit review');
    } finally {
      setSubmitting(false);
    }
  };

  const handleUserClick = (userId) => {
    // Navigate to public profile (not showing email)
    navigate(`/user/${userId}`);
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Reviews ({reviews.length})
      </Typography>

      {/* Review Form */}
      {user && canReview && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Box component="form" onSubmit={handleSubmit}>
              <Typography variant="h6" gutterBottom>
                Leave a Review
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Typography component="legend" sx={{ mr: 2 }}>
                  Rating:
                </Typography>
                <Rating
                  value={rating}
                  onChange={(e, value) => setRating(value)}
                />
              </Box>
              <TextField
                fullWidth
                multiline
                rows={3}
                placeholder="Share your thoughts..."
                value={content}
                onChange={(e) => setContent(e.target.value)}
                required
                sx={{ mb: 2 }}
              />
              <Button
                type="submit"
                variant="contained"
                startIcon={<Send />}
                disabled={submitting}
              >
                Submit Review
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Reviews List */}
      <Box>
        {reviews.map((review, index) => (
          <Box key={review._id}>
            {index > 0 && <Divider sx={{ my: 2 }} />}
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Avatar
                src={review.user?.avatar}
                sx={{ cursor: 'pointer' }}
                onClick={() => handleUserClick(review.user?._id)}
              >
                {review.user?.fullName?.charAt(0)}
              </Avatar>
              <Box sx={{ flex: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Typography
                    variant="subtitle1"
                    sx={{ cursor: 'pointer', '&:hover': { textDecoration: 'underline' } }}
                    onClick={() => handleUserClick(review.user?._id)}
                  >
                    {review.user?.fullName}
                  </Typography>
                  <Rating value={review.rating} readOnly size="small" />
                </Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {new Date(review.createdAt).toLocaleDateString()}
                </Typography>
                <Typography variant="body1">{review.content}</Typography>
              </Box>
            </Box>
          </Box>
        ))}

        {reviews.length === 0 && (
          <Typography color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
            No reviews yet. Be the first to review!
          </Typography>
        )}
      </Box>
    </Box>
  );
};

export default ReviewSection;
