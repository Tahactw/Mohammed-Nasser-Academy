import { supabase } from '../supabase'
import { Course, CourseEnrollment } from '@/types'

export const coursesApi = {
  // Get all courses
  async getAll() {
    const { data, error } = await supabase
      .from('courses')
      .select('*')
      .order('start_date', { ascending: false })

    if (error) throw error
    return data as Course[]
  },

  // Get single course
  async getById(id: string) {
    const { data, error } = await supabase
      .from('courses')
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data as Course
  },

  // Get user's enrollments
  async getUserEnrollments(userId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .select(`
        *,
        course:courses(*)
      `)
      .eq('user_id', userId)
      .order('enrolled_at', { ascending: false })

    if (error) throw error
    return data as CourseEnrollment[]
  },

  // Get course enrollments
  async getCourseEnrollments(courseId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .select(`
        *,
        user:users(id, username, avatar_url)
      `)
      .eq('course_id', courseId)
      .order('enrolled_at', { ascending: false })

    if (error) throw error
    return data as CourseEnrollment[]
  },

  // Check enrollment
  async checkEnrollment(courseId: string, userId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .select('*')
      .eq('course_id', courseId)
      .eq('user_id', userId)
      .single()

    if (error && error.code !== 'PGRST116') throw error
    return data as CourseEnrollment | null
  },

  // Create course (admin)
  async create(course: Omit<Course, 'id' | 'created_at' | 'updated_at'>) {
    const { data, error } = await supabase
      .from('courses')
      .insert(course)
      .select()
      .single()

    if (error) throw error
    return data as Course
  },

  // Update course (admin)
  async update(id: string, updates: Partial<Course>) {
    const { data, error } = await supabase
      .from('courses')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as Course
  },

  // Delete course (admin)
  async delete(id: string) {
    const { error } = await supabase
      .from('courses')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Enroll user (admin)
  async enrollUser(courseId: string, userId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .insert({
        course_id: courseId,
        user_id: userId,
        status: 'not_started',
        progress: 0,
        enrolled_at: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data as CourseEnrollment
  },

  // Update enrollment (admin)
  async updateEnrollment(id: string, updates: Partial<CourseEnrollment>) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as CourseEnrollment
  },

  // Remove enrollment (admin)
  async removeEnrollment(courseId: string, userId: string) {
    const { error } = await supabase
      .from('course_enrollments')
      .delete()
      .eq('course_id', courseId)
      .eq('user_id', userId)

    if (error) throw error
  }
}