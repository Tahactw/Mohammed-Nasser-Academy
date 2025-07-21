import { supabase } from '../supabase'
import { AdminLog } from '@/types'

export const adminApi = {
  // Log admin action
  async logAction(adminId: string, action: string, entityType: string, entityId: string, details?: any) {
    const { data, error } = await supabase
      .from('admin_logs')
      .insert({
        admin_id: adminId,
        action,
        entity_type: entityType,
        entity_id: entityId,
        details
      })
      .select()
      .single()

    if (error) throw error
    return data as AdminLog
  },

  // Get admin logs
  async getLogs(limit = 100) {
    const { data, error } = await supabase
      .from('admin_logs')
      .select(`
        *,
        admin:users(id, username)
      `)
      .order('created_at', { ascending: false })
      .limit(limit)

    if (error) throw error
    return data as AdminLog[]
  },

  // Get dashboard stats
  async getDashboardStats() {
    const [
      { count: usersCount },
      { count: booksCount },
      { count: coursesCount },
      { count: transactionsCount }
    ] = await Promise.all([
      supabase.from('users').select('*', { count: 'exact', head: true }),
      supabase.from('books').select('*', { count: 'exact', head: true }),
      supabase.from('courses').select('*', { count: 'exact', head: true }),
      supabase.from('transactions').select('*', { count: 'exact', head: true })
    ])

    return {
      users: usersCount || 0,
      books: booksCount || 0,
      courses: coursesCount || 0,
      transactions: transactionsCount || 0
    }
  },

  // Badges management
  async getAllBadges() {
    const { data, error } = await supabase
      .from('badges')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data
  },

  async createBadge(badge: any) {
    const { data, error } = await supabase
      .from('badges')
      .insert(badge)
      .select()
      .single()

    if (error) throw error
    return data
  },

  async assignBadge(userId: string, badgeId: string, adminId: string) {
    const { data, error } = await supabase
      .from('user_badges')
      .insert({
        user_id: userId,
        badge_id: badgeId,
        assigned_by: adminId
      })
      .select()
      .single()

    if (error) throw error
    return data
  },

  async revokeBadge(userId: string, badgeId: string) {
    const { error } = await supabase
      .from('user_badges')
      .delete()
      .eq('user_id', userId)
      .eq('badge_id', badgeId)

    if (error) throw error
  },

  // Certificates management
  async issueCertificate(userId: string, courseId: string, certificateUrl: string, adminId: string) {
    const { data, error } = await supabase
      .from('certificates')
      .insert({
        user_id: userId,
        course_id: courseId,
        certificate_url: certificateUrl,
        issued_by: adminId
      })
      .select()
      .single()

    if (error) throw error
    return data
  },

  // Site settings
  async getSiteSettings() {
    const { data, error } = await supabase
      .from('site_settings')
      .select('*')
      .single()

    if (error && error.code !== 'PGRST116') throw error
    return data || {}
  },

  async updateSiteSettings(settings: any) {
    const { data, error } = await supabase
      .from('site_settings')
      .upsert(settings)
      .select()
      .single()

    if (error) throw error
    return data
  }
}