import express from 'express';
// ...existing code...
import { verifySupabaseToken } from './auth.js';

const router = express.Router();

// Create payment intent
router.post('/create-intent', verifySupabaseToken, async (req, res) => {
  try {
    const { itemType, itemId, amount } = req.body;
    
    // Create payment record
    const { data: payment, error } = await supabase
      .from('payments')
      .insert([{
        user_id: req.user.id,
        amount,
        item_type: itemType,
        item_id: itemId,
        status: 'pending'
      }])
      .select()
      .single();
    
    if (error) throw error;
    
    // In production, integrate with Stripe here
    // For now, return mock payment intent
    res.json({
      paymentId: payment.id,
      clientSecret: 'mock_secret_' + payment.id,
      amount
    });
  } catch (error) {
    console.error('Payment creation error:', error);
    res.status(500).json({ error: 'Failed to create payment' });
  }
});

// Confirm payment
router.post('/confirm', verifySupabaseToken, async (req, res) => {
  try {
    const { paymentId } = req.body;
    
    // Update payment status
    const { data: payment, error } = await supabase
      .from('payments')
      .update({ status: 'completed' })
      .eq('id', paymentId)
      .eq('user_id', req.user.id)
      .select()
      .single();
    
    if (error) throw error;
    
    // Process the purchase based on item type
    if (payment.item_type === 'book') {
      await supabase
        .from('user_purchased_books')
        .insert([{
          user_id: req.user.id,
          book_id: payment.item_id
        }]);
    }
    
    res.json({ success: true, payment });
  } catch (error) {
    console.error('Payment confirmation error:', error);
    res.status(500).json({ error: 'Failed to confirm payment' });
  }
});

// Get user's payment history
router.get('/history', verifySupabaseToken, async (req, res) => {
  try {
    const { data: payments, error } = await supabase
      .from('payments')
      .select('*')
      .eq('user_id', req.user.id)
      .order('created_at', { ascending: false });
    
    if (error) throw error;
    res.json(payments);
  } catch (error) {
    console.error('Payment history error:', error);
    res.status(500).json({ error: 'Failed to fetch payment history' });
  }
});

export default router;
