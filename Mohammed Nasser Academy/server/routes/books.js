import express from 'express';
import { supabaseHelpers } from '../lib/supabaseClient.js';
import { verifySupabaseToken } from './auth.js';

const router = express.Router();

// Get all books
router.get('/', async (req, res) => {
  try {
    const books = await supabaseHelpers.getAllBooks();
    res.json(books);
  } catch (error) {
    console.error('Books fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch books' });
  }
});

// Get single book
router.get('/:id', async (req, res) => {
  try {
    const book = await supabaseHelpers.getBookById(req.params.id);
    
    if (!book) {
      return res.status(404).json({ error: 'Book not found' });
    }
    
    res.json(book);
  } catch (error) {
    console.error('Book fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch book' });
  }
});

// Check if user purchased book
router.get('/:id/check-purchase', verifySupabaseToken, async (req, res) => {
  try {
    const purchased = await supabaseHelpers.checkBookPurchase(req.user.id, req.params.id);
    res.json({ purchased });
  } catch (error) {
    console.error('Purchase check error:', error);
    res.status(500).json({ error: 'Failed to check purchase status' });
  }
});

// Purchase book (after payment confirmed)
router.post('/:id/purchase', verifySupabaseToken, async (req, res) => {
  try {
    const purchase = await supabaseHelpers.purchaseBook(req.user.id, req.params.id);
    
    // Award badge
    await supabaseHelpers.awardBadge(req.user.id, {
      name: 'Book Collector',
      icon: '📚',
      badge_type: 'book_purchase'
    });
    
    res.json({ success: true, purchase });
  } catch (error) {
    console.error('Book purchase error:', error);
    res.status(500).json({ error: 'Failed to complete purchase' });
  }
});

export default router;
