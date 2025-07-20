import express from 'express';
import { verifySupabaseToken } from './auth.js';
import { getSupabaseAdmin } from '../config/supabase.js';

const router = express.Router();


// Middleware to check if user is admin
const isAdmin = async (req, res, next) => {
  try {
    const supabase = getSupabaseAdmin();
    const { data: user, error } = await supabase
      .from('users')
      .select('email, is_admin')
      .eq('id', req.user.id)
      .single();
    
    if (error || !user || (user.email !== 'admin@admin.com' && !user.is_admin)) {
      return res.status(403).json({ error: 'Unauthorized' });
    }
    
    next();
  } catch (error) {
    res.status(500).json({ error: 'Admin check failed' });
  }
};

// Apply admin check to all routes
router.use(verifySupabaseToken);
router.use(isAdmin);

// Get admin stats
router.get('/stats', async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    const [users, courses, books, purchases] = await Promise.all([
      supabase.from('users').select('id', { count: 'exact' }),
      supabase.from('courses').select('id', { count: 'exact' }),
      supabase.from('books').select('id', { count: 'exact' }),
      supabase.from('user_purchased_books').select('book_id')
    ]);
    
    const totalRevenue = purchases.data?.length * 10 || 0; // Simple calculation
    
    res.json({
      totalUsers: users.count || 0,
      totalCourses: courses.count || 0,
      totalBooks: books.count || 0,
      totalRevenue
    });
  } catch (error) {
    console.error('Error fetching stats:', error);
    res.status(500).json({ error: 'Failed to fetch stats' });
  }
});

// Get all users
router.get('/users', async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    const { data: users, error } = await supabase
      .from('users')
      .select(`
        *,
        badges:user_badges(count)
      `)
      .order('created_at', { ascending: false });
    
    if (error) throw error;
    res.json(users || []);
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({ error: 'Failed to fetch users' });
  }
});

// Delete user
router.delete('/users/:userId', async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    const { error } = await supabase.auth.admin.deleteUser(req.params.userId);
    if (error) throw error;
    res.json({ success: true });
  } catch (error) {
    console.error('Error deleting user:', error);
    res.status(500).json({ error: 'Failed to delete user' });
  }
});

// Assign badge to user
router.post('/users/:userId/badges', async (req, res) => {
  try {
    const { name, description, icon, color, badge_type } = req.body;
    
    const { data: badge, error } = await supabase
      .from('user_badges')
      .insert({
        user_id: req.params.userId,
        name,
        description,
        icon,
        color,
        badge_type: badge_type || 'custom'
      })
      .select()
      .single();
    
    if (error) throw error;
    res.json(badge);
  } catch (error) {
    console.error('Error assigning badge:', error);
    res.status(500).json({ error: 'Failed to assign badge' });
  }
});

// Get badge templates
router.get('/badge-templates', async (req, res) => {
  try {
    const { data: templates, error } = await supabase
      .from('badge_templates')
      .select('*')
      .order('name');
    
    if (error) throw error;
    res.json(templates || []);
  } catch (error) {
    console.error('Error fetching badge templates:', error);
    res.status(500).json({ error: 'Failed to fetch badge templates' });
  }
});

// Create course
router.post('/courses', async (req, res) => {
  try {
    const { data: course, error } = await supabase
      .from('courses')
      .insert(req.body)
      .select()
      .single();
    
    if (error) throw error;
    res.json(course);
  } catch (error) {
    console.error('Error creating course:', error);
    res.status(500).json({ error: 'Failed to create course' });
  }
});

// Update course
router.put('/courses/:courseId', async (req, res) => {
  try {
    const { data: course, error } = await supabase
      .from('courses')
      .update(req.body)
      .eq('id', req.params.courseId)
      .select()
      .single();
    
    if (error) throw error;
    res.json(course);
  } catch (error) {
    console.error('Error updating course:', error);
    res.status(500).json({ error: 'Failed to update course' });
  }
});

// Delete course
router.delete('/courses/:courseId', async (req, res) => {
  try {
    const { error } = await supabase
      .from('courses')
      .delete()
      .eq('id', req.params.courseId);
    
    if (error) throw error;
    res.json({ success: true });
  } catch (error) {
    console.error('Error deleting course:', error);
    res.status(500).json({ error: 'Failed to delete course' });
  }
});

// Create book
router.post('/books', async (req, res) => {
  try {
    const { data: book, error } = await supabase
      .from('books')
      .insert(req.body)
      .select()
      .single();
    
    if (error) throw error;
    res.json(book);
  } catch (error) {
    console.error('Error creating book:', error);
    res.status(500).json({ error: 'Failed to create book' });
  }
});

// Update book
router.put('/books/:bookId', async (req, res) => {
  try {
    const { data: book, error } = await supabase
      .from('books')
      .update(req.body)
      .eq('id', req.params.bookId)
      .select()
      .single();
    
    if (error) throw error;
    res.json(book);
  } catch (error) {
    console.error('Error updating book:', error);
    res.status(500).json({ error: 'Failed to update book' });
  }
});

// Delete book
router.delete('/books/:bookId', async (req, res) => {
  try {
    const { error } = await supabase
      .from('books')
      .delete()
      .eq('id', req.params.bookId);
    
    if (error) throw error;
    res.json({ success: true });
  } catch (error) {
    console.error('Error deleting book:', error);
    res.status(500).json({ error: 'Failed to delete book' });
  }
});

// Get all reviews
router.get('/reviews', async (req, res) => {
  try {
    const { data: reviews, error } = await supabase
      .from('reviews')
      .select(`
        *,
        user:users(full_name),
        course:courses(title),
        book:books(title)
      `)
      .order('created_at', { ascending: false });
    
    if (error) throw error;
    
    const formattedReviews = reviews?.map(r => ({
      ...r,
      user_name: r.user?.full_name,
      course_title: r.course?.title,
      book_title: r.book?.title
    })) || [];
    
    res.json(formattedReviews);
  } catch (error) {
    console.error('Error fetching reviews:', error);
    res.status(500).json({ error: 'Failed to fetch reviews' });
  }
});

// Update review visibility
router.patch('/reviews/:reviewId', async (req, res) => {
  try {
    const { is_visible } = req.body;
    
    const { data: review, error } = await supabase
      .from('reviews')
      .update({ is_visible })
      .eq('id', req.params.reviewId)
      .select()
      .single();
    
    if (error) throw error;
    res.json(review);
  } catch (error) {
    console.error('Error updating review:', error);
    res.status(500).json({ error: 'Failed to update review' });
  }
});

// Delete review
router.delete('/reviews/:reviewId', async (req, res) => {
  try {
    const { error } = await supabase
      .from('reviews')
      .delete()
      .eq('id', req.params.reviewId);
    
    if (error) throw error;
    res.json({ success: true });
  } catch (error) {
    console.error('Error deleting review:', error);
    res.status(500).json({ error: 'Failed to delete review' });
  }
});

export default router;
