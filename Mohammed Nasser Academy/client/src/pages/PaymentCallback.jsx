import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Container, CircularProgress, Box } from '@mui/material';
import axios from 'axios';

const PaymentCallback = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const processCallback = async () => {
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/api/payment/callback`,
          {
            // Send all query parameters to backend
            ...Object.fromEntries(searchParams),
          }
        );

        if (response.data.success) {
          navigate(`/payment/success?type=${response.data.itemType}&id=${response.data.itemId}`);
        } else {
          navigate('/payment/failed');
        }
      } catch (error) {
        console.error('Payment callback error:', error);
        navigate('/payment/failed');
      }
    };

    processCallback();
  }, []);

  return (
    <Container maxWidth="sm" sx={{ py: 8 }}>
      <Box sx={{ display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Box>
    </Container>
  );
};

export default PaymentCallback;
