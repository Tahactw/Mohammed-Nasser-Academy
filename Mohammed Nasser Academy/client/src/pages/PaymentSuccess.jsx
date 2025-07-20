import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Container, Typography, Box, CircularProgress } from '@mui/material';
import { CheckCircle } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const PaymentSuccess = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { refreshProfile } = useAuth();

  useEffect(() => {
    const verifyPayment = async () => {
      // Refresh profile to get updated purchases
      await refreshProfile();
      
      // Redirect to appropriate page after 3 seconds
      setTimeout(() => {
        const itemType = searchParams.get('type');
        const itemId = searchParams.get('id');
        
        if (itemType === 'book' && itemId) {
          navigate(`/books/${itemId}`);
        } else {
          navigate('/profile');
        }
      }, 3000);
    };

    verifyPayment();
  }, []);

  return (
    <Container maxWidth="sm" sx={{ py: 8, textAlign: 'center' }}>
      <CheckCircle sx={{ fontSize: 80, color: 'success.main', mb: 3 }} />
      <Typography variant="h4" gutterBottom>
        Payment Successful!
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Thank you for your purchase. You will be redirected shortly...
      </Typography>
      <Box sx={{ mt: 4 }}>
        <CircularProgress />
      </Box>
    </Container>
  );
};

export default PaymentSuccess;
