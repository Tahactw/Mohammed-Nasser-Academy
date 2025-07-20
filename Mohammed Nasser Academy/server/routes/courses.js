import express from 'express';
import { getSupabaseAdmin } from '../config/supabase.js';
import { verifySupabaseToken } from './auth.js';

const router = express.Router();

// Get all courses
router.get('/', async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    const { data: courses, error } = await supabase
      .from('courses')
      .select('*')
      .order('order_index', { ascending: true });

    if (error) throw error;
    res.json(courses || []);
  } catch (error) {
    console.error('Error fetching courses:', error);
    res.status(500).json({ error: 'Failed to fetch courses' });
  }
});

// Get single course
router.get('/:id', async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    const { data: course, error } = await supabase
      .from('courses')
      .select('*')
      .eq('id', req.params.id)
      .single();

    if (error || !course) {
      return res.status(404).json({ error: 'Course not found' });
    }

    res.json(course);
  } catch (error) {
    console.error('Error fetching course:', error);
    res.status(500).json({ error: 'Failed to fetch course' });
  }
});

// Enroll in course
router.post('/:id/enroll', verifySupabaseToken, async (req, res) => {
  try {
    const supabase = getSupabaseAdmin();
    const courseId = req.params.id;
    const userId = req.user.id;

    // Check if already enrolled
    const { data: existing } = await supabase
      .from('user_course_progress')
      .select('*')
      .eq('user_id', userId)
      .eq('course_id', courseId)
      .single();

    if (existing) {
      return res.json({ message: 'Already enrolled', progress: existing });
    }

    // Create enrollment
    const { data: progress, error } = await supabase
      .from('user_course_progress')
      .insert({
        user_id: userId,
        course_id: courseId,
        status: 'in_progress',
        progress: 0,
        started_at: new Date().toISOString(),
      })
      .select()
      .single();

    if (error) throw error;

    // Update enrollment count
    await supabase.rpc('increment_course_enrollment', { course_id: courseId });

    res.json({ message: 'Enrolled successfully', progress });
  } catch (error) {
    console.error('Error enrolling in course:', error);
    res.status(500).json({ error: 'Failed to enroll in course' });
  }
});

export default router;