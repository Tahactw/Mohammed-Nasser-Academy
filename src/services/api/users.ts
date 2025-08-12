import { supabase } from '../supabase'
import { User, UserBadge, Certificate, BlockedUser } from '@/types'

export const usersApi = {
  // Get user profile
  async getProfile(userId: string) {
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .eq('id', userId)
      .single()

    if (error) throw error
    return data as User
  },

  // Get user by username
  async getByUsername(username: string) {
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .eq('username', username)
      .single()

    if (error) throw error
    return data as User
  },

  // Update profile
  async updateProfile(userId: string, updates: Partial<User>) {
    const { data, error } = await supabase
      .from('users')
      .update(updates)
      .eq('id', userId)
      .select()
      .single()

    if (error) throw error
    return data as User
  },

  // Check username availability
  async checkUsername(username: string, currentUserId?: string) {
    let query = supabase
      .from('users')
      .select('id')
      .eq('username', username)

    if (currentUserId) {
      query = query.neq('id', currentUserId)
    }

    const { data, error } = await query.single()

    if (error && error.code !== 'PGRST116') throw error
    return !data
  },

  // Get user's badges
  async getUserBadges(userId: string) {
    const { data, error } = await supabase
      .from('user_badges')
      .select(`
        *,
        badge:badges(*)
      `)
      .eq('user_id', userId)
      .order('assigned_at', { ascending: false })

    if (error) throw error
    return data as UserBadge[]
  },

  // Get user's certificates
  async getUserCertificates(userId: string) {
    const { data, error } = await supabase
      .from('certificates')
      .select(`
        *,
        course:courses(*)
      `)
      .eq('user_id', userId)
      .order('issued_at', { ascending: false })

    if (error) throw error
    return data as Certificate[]
  },

  // Get blocked users
  async getBlockedUsers(userId: string) {
    const { data, error } = await supabase
      .from('blocked_users')
      .select(`
        *,
        blocked_user:users!blocked_users_blocked_id_fkey(id, username, avatar_url)
      `)
      .eq('blocker_id', userId)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as BlockedUser[]
  },

  // Check if blocked
  async isBlocked(blockerId: string, blockedId: string) {
    const { data, error } = await supabase
      .from('blocked_users')
      .select('id')
      .eq('blocker_id', blockerId)
      .eq('blocked_id', blockedId)
      .single()

    if (error && error.code !== 'PGRST116') throw error
    return !!data
  },

  // Block user
  async blockUser(blockerId: string, blockedId: string) {
    const { data, error } = await supabase
      .from('blocked_users')
      .insert({
        blocker_id: blockerId,
        blocked_id: blockedId
      })
      .select()
      .single()

    if (error) throw error
    return data as BlockedUser
  },

  // Unblock user
  async unblockUser(blockerId: string, blockedId: string) {
    const { error } = await supabase
      .from('blocked_users')
      .delete()
      .eq('blocker_id', blockerId)
      .eq('blocked_id', blockedId)

    if (error) throw error
  },

  // Delete account
  async deleteAccount(userId: string) {
    // This should cascade delete all user data
    const { error } = await supabase
      .from('users')
      .delete()
      .eq('id', userId)

    if (error) throw error

    // Also delete auth user
    const { error: authError } = await supabase.auth.admin.deleteUser(userId)
    if (authError) throw authError
  },

  // Admin: Get all users
  async getAllUsers() {
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as User[]
  },

  // Admin: Ban user
  async banUser(userId: string) {
    const { data, error } = await supabase
      .from('users')
      .update({ is_banned: true })
      .eq('id', userId)
      .select()
      .single()

    if (error) throw error
    return data as User
  },

  // Admin: Unban user
  async unbanUser(userId: string) {
    const { data, error } = await supabase
      .from('users')
      .update({ is_banned: false })
      .eq('id', userId)
      .select()
      .single()

    if (error) throw error
    return data as User
  }
}