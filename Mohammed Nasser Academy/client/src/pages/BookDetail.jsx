import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Typography,
  Box,
  Button,
  TextField,
  Paper,
  Divider,
  Avatar,
  Rating,
  Card,
  CardContent,
  InputAdornment,
  Alert,
} from '@mui/material';
import {
  ShoppingCart,
  Download,
  AttachMoney,
  Comment,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';
import axios from 'axios';
import PaymentModal from '../components/payment/PaymentModal';
import ReviewSection from '../components/common/ReviewSection';

const BookDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, profile } = useAuth();
  
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [amount, setAmount] = useState(10);
  const [hasPurchased, setHasPurchased] = useState(false);
  const [paymentModalOpen, setPaymentModalOpen] = useState(false);

  useEffect(() => {
    fetchBook();
  }, [id, profile]);

  const fetchBook = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/books/${id}`);
      setBook(response.data);
      
      // Check if user has purchased this book
      if (profile?.purchasedBooks?.includes(id)) {
        setHasPurchased(true);
      }
    } catch (error) {
      console.error('Error fetching book:', error);
      toast.error('Failed to load book details');
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = () => {
    if (!user) {
      toast.info('Please login to purchase books');
      navigate('/login');
      return;
    }

    if (amount < (book.minPrice || 10)) {
      toast.error(`Minimum amount is $${book.minPrice || 10}`);
      return;
    }

    setPaymentModalOpen(true);
  };

  const handlePaymentSuccess = () => {
    setHasPurchased(true);
    toast.success('Payment successful! You can now download the book.');
  };

  const handleDownload = async () => {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/books/${id}/download`,
        {
          headers: {
            Authorization: `Bearer ${await getAuthToken()}`,
          },
          responseType: 'blob',
        }
      );

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${book.title}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Failed to download book');
    }
  };

  if (loading) {
    return <Container sx={{ py: 8 }}>Loading...</Container>;
  }

  if (!book) {
    return <Container sx={{ py: 8 }}>Book not found</Container>;
  }

  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Box sx={{ position: 'sticky', top: 100 }}>
            <img
              src={book.coverImage || '/placeholder-book.jpg'}
              alt={book.title}
              style={{
                width: '100%',
                borderRadius: 8,
                boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
              }}
            />
            
            <Paper sx={{ p: 3, mt: 3 }}>
              {hasPurchased ? (
                <Box>
                  <Alert severity="success" sx={{ mb: 2 }}>
                    You own this book!
                  </Alert>
                  <Button
                    variant="contained"
                    size="large"
                    fullWidth
                    startIcon={<Download />}
                    onClick={handleDownload}
                  >
                    Download Book
                  </Button>
                </Box>
              ) : (
                <Box>
                  <Typography variant="h6" gutterBottom>
                    Pay What You Want
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Minimum: ${book.minPrice || 10}
                  </Typography>
                  <TextField
                    fullWidth
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(Math.max(book.minPrice || 10, Number(e.target.value)))}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <AttachMoney />
                        </InputAdornment>
                      ),
                    }}
                    sx={{ mb: 2 }}
                  />
                  <Button
                    variant="contained"
                    size="large"
                    fullWidth
                    startIcon={<ShoppingCart />}
                    onClick={handlePurchase}
                  >
                    Purchase for ${amount}
                  </Button>
                </Box>
              )}
            </Paper>
          </Box>
        </Grid>

        <Grid item xs={12} md={8}>
          <Typography variant="h3" component="h1" gutterBottom>
            {book.title}
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Rating value={book.averageRating || 0} readOnly precision={0.5} />
            <Typography variant="body2" sx={{ ml: 1 }}>
              ({book.totalReviews || 0} reviews)
            </Typography>
          </Box>

          <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
            About this book
          </Typography>
          <Typography variant="body1" paragraph>
            {book.fullDescription}
          </Typography>

          <Divider sx={{ my: 4 }} />

          {/* Reviews Section */}
          <ReviewSection
            itemType="book"
            itemId={id}
            reviews={book.reviews || []}
            canReview={hasPurchased}
          />
        </Grid>
      </Grid>

      {/* Payment Modal */}
      <PaymentModal
        open={paymentModalOpen}
        onClose={() => setPaymentModalOpen(false)}
        amount={amount}
        itemType="book"
        itemId={id}
        onSuccess={handlePaymentSuccess}
      />
    </Container>
  );
};

export default BookDetail;
