import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  Box,
  CircularProgress,
  Typography,
} from '@mui/material';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';

const PaymentModal = ({ open, onClose, amount, itemType, itemId, onSuccess }) => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [paymentUrl, setPaymentUrl] = useState('');

  useEffect(() => {
    if (open && user) {
      initiatePayment();
    }
  }, [open]);

  const initiatePayment = async () => {
    setLoading(true);
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/api/payment/initiate`,
        {
          amount: amount * 100, // Convert to cents
          itemType,
          itemId,
          userId: user.id,
          userEmail: user.email,
        }
      );

      setPaymentUrl(response.data.paymentUrl);
    } catch (error) {
      console.error('Payment initiation error:', error);
      onClose();
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Complete Payment</DialogTitle>
      <DialogContent>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : paymentUrl ? (
          <Box sx={{ height: 600 }}>
            <iframe
              src={paymentUrl}
              width="100%"
              height="100%"
              frameBorder="0"
              title="Payment"
            />
          </Box>
        ) : (
          <Typography>Error initiating payment. Please try again.</Typography>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default PaymentModal;
