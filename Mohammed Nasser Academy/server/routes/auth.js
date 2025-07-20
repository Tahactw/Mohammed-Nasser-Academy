import express from 'express';
import jwt from 'jsonwebtoken';
import { getSupabaseAdmin } from '../config/supabase.js';

const router = express.Router();

// Verify Supabase token middleware
export const verifySupabaseToken = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const supabase = getSupabaseAdmin();
    const { data: { user }, error } = await supabase.auth.getUser(token);
    
    if (error || !user) {
      return res.status(401).json({ error: 'Invalid token' });
    }

    req.user = user;
    next();
  } catch (error) {
    console.error('Token verification error:', error);
    res.status(401).json({ error: 'Token verification failed' });
  }
};

// Generate JWT for internal use
router.post('/token', verifySupabaseToken, (req, res) => {
  const token = jwt.sign(
    { userId: req.user.id, email: req.user.email },
    process.env.JWT_SECRET || 'default-dev-secret',
    { expiresIn: '7d' }
  );

  res.json({ token });
});

// Health check for auth service
router.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    supabase: process.env.SUPABASE_URL ? 'configured' : 'not configured',
    timestamp: new Date().toISOString()
  });
});

export default router;
