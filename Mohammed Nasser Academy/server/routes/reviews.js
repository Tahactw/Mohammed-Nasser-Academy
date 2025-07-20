import express from 'express';
import { supabaseHelpers } from '../lib/supabaseClient.js';
import { verifySupabaseToken } from './auth.js';

const router = express.Router();

// Get reviews for a course or book
router.get('/', async (req, res) => {
  try {
    const { courseId, bookId } = req.query;
    
    let query = supabase
      .from('reviews')
      .select(`
        *,
        user:users (
          id,
          full_name,
          avatar
        )
      `);
    
    if (courseId) {
      query = query.eq('course_id', courseId);
    } else if (bookId) {
      query = query.eq('book_id', bookId);
    } else {
      return res.status(400).json({ error: 'courseId or bookId required' });
    }
    
    const { data: reviews, error } = await query.order('created_at', { ascending: false });
    
    if (error) throw error;
    res.json(reviews);
  } catch (error) {
    console.error('Reviews fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch reviews' });
  }
});

// Create a review
router.post('/', verifySupabaseToken, async (req, res) => {
  try {
    const { courseId, bookId, rating, comment } = req.body;
    
    if (!courseId && !bookId) {
      return res.status(400).json({ error: 'courseId or bookId required' });
    }
    
    if (!rating || rating < 1 || rating > 5) {
      return res.status(400).json({ error: 'Valid rating (1-5) required' });
    }
    
    // Check if user already reviewed this item
    let existingQuery = supabase
      .from('reviews')
      .select('id')
      .eq('user_id', req.user.id);
    
    if (courseId) {
      existingQuery = existingQuery.eq('course_id', courseId);
    } else {
      existingQuery = existingQuery.eq('book_id', bookId);
    }
    
    const { data: existing } = await existingQuery.single();
    
    if (existing) {
      return res.status(400).json({ error: 'You have already reviewed this item' });
    }
    
    // Create the review
    const review = await supabaseHelpers.createReview({
      user_id: req.user.id,
      course_id: courseId || null,
      book_id: bookId || null,
      rating,
      comment
    });
    
    res.json(review);
  } catch (error) {
    console.error('Review creation error:', error);
    res.status(500).json({ error: 'Failed to create review' });
  }
});

// Update a review
router.put('/:id', verifySupabaseToken, async (req, res) => {
  try {
    const { rating, comment } = req.body;
    
    const { data: review, error } = await supabase
      .from('reviews')
      .update({ rating, comment })
      .eq('id', req.params.id)
      .eq('user_id', req.user.id)
      .select()
      .single();
    
    if (error) throw error;
    
    // Update average rating
    const targetTable = review.course_id ? 'courses' : 'books';
    const targetId = review.course_id || review.book_id;
    await supabaseHelpers.updateAverageRating(targetTable, targetId);
    
    res.json(review);
  } catch (error) {
    console.error('Review update error:', error);
    res.status(500).json({ error: 'Failed to update review' });
  }
});

// Delete a review
router.delete('/:id', verifySupabaseToken, async (req, res) => {
  try {
    const { data: review, error } = await supabase
      .from('reviews')
      .delete()
      .eq('id', req.params.id)
      .eq('user_id', req.user.id)
      .select()
      .single();
    
    if (error) throw error;
    
    // Update average rating
    const targetTable = review.course_id ? 'courses' : 'books';
    const targetId = review.course_id || review.book_id;
    await supabaseHelpers.updateAverageRating(targetTable, targetId);
    
    res.json({ success: true });
  } catch (error) {
    console.error('Review deletion error:', error);
    res.status(500).json({ error: 'Failed to delete review' });
  }
});

export default router;
