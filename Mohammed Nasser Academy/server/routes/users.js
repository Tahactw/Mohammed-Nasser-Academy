import express from 'express';
import { getSupabaseAdmin } from '../config/supabase.js';
import { verifySupabaseToken } from './auth.js';

const router = express.Router();

// Helper function to ensure user profile exists
async function ensureUserProfile(userId) {
  const supabase = getSupabaseAdmin();
  
  // Check if user profile exists
  const { data: existingProfile, error: fetchError } = await supabase
    .from('users')
    .select('*')
    .eq('id', userId)
    .single();
  
  if (existingProfile) {
    return existingProfile;
  }
  
  // Get auth user details
  const { data: { user: authUser }, error: authError } = await supabase.auth.admin.getUserById(userId);
  
  if (authError || !authUser) {
    console.error('Auth user not found:', userId, authError);
    return null;
  }
  
  // Create new profile
  const { data: newProfile, error: createError } = await supabase
    .from('users')
    .insert({
      id: authUser.id,
      email: authUser.email,
      full_name: authUser.user_metadata?.full_name || authUser.email.split('@')[0],
      avatar: authUser.user_metadata?.avatar_url,
      created_at: new Date().toISOString(),
    })
    .select()
    .single();
  
  if (createError) {
    console.error('Error creating profile:', createError);
    return null;
  }
  
  return newProfile;
}

// Get user profile by ID (public)
router.get('/profile/:id', async (req, res) => {
  try {
    const { id } = req.params;
    console.log('Fetching profile for user:', id);
    
    const profile = await ensureUserProfile(id);
    if (!profile) {
      console.error(`[PROFILE/:id] User not found or not in Auth: ${id}`);
      return res.status(404).json({ error: 'User not found', details: `User ${id} not found in users table or Supabase Auth.` });
    }
    const supabase = getSupabaseAdmin();
    try {
      const [badges, purchasedBooks, courseProgress] = await Promise.all([
        supabase.from('user_badges')
          .select('*, badge:badge_templates(*)')
          .eq('user_id', id),
        supabase.from('user_purchased_books')
          .select('*, book:books(*)')
          .eq('user_id', id),
        supabase.from('user_course_progress')
          .select('*')
          .eq('user_id', id),
      ]);
      const enrichedProfile = {
        ...profile,
        badges: badges.data || [],
        purchasedBooks: purchasedBooks.data?.map(pb => pb.book).filter(Boolean) || [],
        courseProgress: courseProgress.data || [],
      };
      return res.json(enrichedProfile);
    } catch (err) {
      console.error(`[PROFILE/:id] Error enriching profile for user ${id}:`, err);
      return res.status(500).json({ error: 'Failed to enrich profile', details: err.message });
    }
  } catch (error) {
    console.error('Public profile fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch profile', details: error.message });
  }
});

// Get authenticated user's profile
router.get('/profile', verifySupabaseToken, async (req, res) => {
  try {
    const profile = await ensureUserProfile(req.user.id);
    if (!profile) {
      console.error(`[PROFILE] Authenticated user profile not found: ${req.user.id}`);
      return res.status(404).json({ error: 'Profile not found', details: `User ${req.user.id} not found in users table or Supabase Auth.` });
    }
    const supabase = getSupabaseAdmin();
    try {
      const [badges, purchasedBooks, courseProgress] = await Promise.all([
        supabase.from('user_badges')
          .select('*, badge:badge_templates(*)')
          .eq('user_id', req.user.id),
        supabase.from('user_purchased_books')
          .select('book_id')
          .eq('user_id', req.user.id),
        supabase.from('user_course_progress')
          .select('*')
          .eq('user_id', req.user.id),
      ]);
      res.json({
        ...profile,
        badges: badges.data || [],
        purchasedBooks: purchasedBooks.data?.map(pb => pb.book_id) || [],
        courseProgress: courseProgress.data || [],
      });
    } catch (err) {
      console.error(`[PROFILE] Error enriching authenticated profile:`, err);
      res.status(500).json({ error: 'Failed to enrich profile', details: err.message });
    }
  } catch (error) {
    console.error('Profile fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch profile' });
  }
});

// Create user profile (for existing auth users)
router.post('/profile', verifySupabaseToken, async (req, res) => {
  try {
    const profile = await ensureUserProfile(req.user.id);
    
    if (!profile) {
      return res.status(500).json({ error: 'Failed to create profile' });
    }
    
    res.json(profile);
  } catch (error) {
    console.error('Create profile error:', error);
    res.status(500).json({ error: 'Failed to create profile' });
  }
});

// Update user profile
router.put('/profile', verifySupabaseToken, async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    const { full_name, bio, brief, avatar, theme_preference, social_links } = req.body;
    
    const { data: updatedUser, error } = await supabase
      .from('users')
      .update({
        full_name,
        bio,
        brief,
        avatar,
        theme_preference,
        social_links,
        updated_at: new Date().toISOString(),
      })
      .eq('id', req.user.id)
      .select()
      .single();
    
    if (error) throw error;
    
    res.json(updatedUser);
  } catch (error) {
    console.error('Profile update error:', error);
    res.status(500).json({ error: 'Failed to update profile' });
  }
});

// Get user badges
router.get('/:userId/badges', async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    const { data: badges, error } = await supabase
      .from('user_badges')
      .select('*, badge:badge_templates(*)')
      .eq('user_id', req.params.userId)
      .order('earned_at', { ascending: false });
    
    if (error) throw error;
    res.json(badges || []);
  } catch (error) {
    console.error('Error fetching badges:', error);
    res.status(500).json({ error: 'Failed to fetch badges' });
  }
});

// Get user enrolled courses
router.get('/:userId/courses', async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    try {
      const { data: progress, error } = await supabase
        .from('user_course_progress')
        .select('*, course:courses(*)')
        .eq('user_id', req.params.userId);
      if (error) throw error;
      const courses = progress?.map(p => ({
        ...p.course,
        status: p.status,
        progress: p.progress,
        started_at: p.started_at,
        completed_at: p.completed_at,
      })).filter(c => c.id) || [];
      res.json(courses);
    } catch (err) {
      console.error(`[USER/:userId/courses] Error:`, err);
      res.status(500).json({ error: 'Failed to fetch courses', details: err.message });
    }
  } catch (error) {
    console.error('Error fetching courses:', error);
    res.status(500).json({ error: 'Failed to fetch courses' });
  }
});

// Get user purchased books
router.get('/:userId/books', async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    const { data: purchases, error } = await supabase
      .from('user_purchased_books')
      .select('*, book:books(*)')
      .eq('user_id', req.params.userId);
    
    if (error) throw error;
    
    const books = purchases?.map(p => ({
      ...p.book,
      purchased_at: p.purchased_at,
    })).filter(b => b.id) || [];
    
    res.json(books);
  } catch (error) {
    console.error('Error fetching books:', error);
    res.status(500).json({ error: 'Failed to fetch books' });
  }
});

// Get user reviews
router.get('/:userId/reviews', async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    const { data: reviews, error } = await supabase
      .from('reviews')
      .select('*, course:courses(title), book:books(title)')
      .eq('user_id', req.params.userId)
      .eq('is_visible', true)
      .order('created_at', { ascending: false });
    
    if (error) throw error;
    
    const formattedReviews = reviews?.map(r => ({
      ...r,
      course_title: r.course?.title,
      book_title: r.book?.title,
    })) || [];
    
    res.json(formattedReviews);
  } catch (error) {
    console.error('Error fetching reviews:', error);
    res.status(500).json({ error: 'Failed to fetch reviews' });
  }
});

// Get course progress
router.get('/course-progress', verifySupabaseToken, async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    try {
      const { data: progress, error } = await supabase
        .from('user_course_progress')
        .select('*')
        .eq('user_id', req.user.id);
      if (error) throw error;
      res.json(progress || []);
    } catch (err) {
      console.error(`[COURSE-PROGRESS] Error:`, err);
      res.status(500).json({ error: 'Failed to fetch course progress', details: err.message });
    }
  } catch (error) {
    console.error('Error fetching course progress:', error);
    res.status(500).json({ error: 'Failed to fetch course progress' });
  }
});

export default router;