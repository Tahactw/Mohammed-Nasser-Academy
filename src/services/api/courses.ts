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

  // Get course by ID
  async getById(id: string) {
    const { data, error } = await supabase
      .from('courses')
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data as Course
  },

  // Create course
  async create(course: Omit<Course, 'id' | 'created_at' | 'updated_at'>) {
    const { data, error } = await supabase
      .from('courses')
      .insert(course)
      .select()
      .single()

    if (error) throw error
    return data as Course
  },

  // Update course
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

  // Delete course
  async delete(id: string) {
    const { error } = await supabase
      .from('courses')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Get course enrollments
  async getCourseEnrollments(courseId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .select(`
        *,
        user:users(id, username, avatar_url, email)
      `)
      .eq('course_id', courseId)
      .order('enrolled_at', { ascending: false })

    if (error) throw error
    return data as CourseEnrollment[]
  },

  // Get user enrollments
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

  // Check enrollment
  async checkEnrollment(courseId: string, userId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .select('id')
      .eq('course_id', courseId)
      .eq('user_id', userId)
      .single()

    if (error && error.code !== 'PGRST116') throw error
    return !!data
  },

  // Enroll user
  async enrollUser(courseId: string, userId: string) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .insert({
        course_id: courseId,
        user_id: userId,
        status: 'enrolled',
        progress: 0,
        enrolled_at: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data as CourseEnrollment
  },

  // Update enrollment
  async updateEnrollment(enrollmentId: string, updates: Partial<CourseEnrollment>) {
    const { data, error } = await supabase
      .from('course_enrollments')
      .update(updates)
      .eq('id', enrollmentId)
      .select()
      .single()

    if (error) throw error
    return data as CourseEnrollment
  },

  // Remove enrollment
  async removeEnrollment(courseId: string, userId: string) {
    const { error } = await supabase
      .from('course_enrollments')
      .delete()
      .eq('course_id', courseId)
      .eq('user_id', userId)

    if (error) throw error
  },

  // Update progress
  async updateProgress(enrollmentId: string, progress: number) {
    const updates: any = { progress }
    
    if (progress >= 100) {
      updates.status = 'completed'
      updates.completed_at = new Date().toISOString()
    }

    const { data, error } = await supabase
      .from('course_enrollments')
      .update(updates)
      .eq('id', enrollmentId)
      .select()
      .single()

    if (error) throw error
    return data as CourseEnrollment
  }
}