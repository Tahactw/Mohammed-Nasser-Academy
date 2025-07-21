import { supabase } from '../supabase'
import { Message } from '@/types'

export const messagesApi = {
  // Get user's messages
  async getUserMessages(userId: string) {
    const { data, error } = await supabase
      .from('messages')
      .select(`
        *,
        sender:users!messages_sender_id_fkey(id, username, avatar_url),
        recipient:users!messages_recipient_id_fkey(id, username, avatar_url)
      `)
      .or(`sender_id.eq.${userId},recipient_id.eq.${userId}`)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as Message[]
  },

  // Get conversation
  async getConversation(userId1: string, userId2: string) {
    const { data, error } = await supabase
      .from('messages')
      .select(`
        *,
        sender:users!messages_sender_id_fkey(id, username, avatar_url),
        recipient:users!messages_recipient_id_fkey(id, username, avatar_url)
      `)
      .or(`and(sender_id.eq.${userId1},recipient_id.eq.${userId2}),and(sender_id.eq.${userId2},recipient_id.eq.${userId1})`)
      .order('created_at', { ascending: true })

    if (error) throw error
    return data as Message[]
  },

  // Send message
  async sendMessage(senderId: string, recipientId: string, content: string) {
    // Check if blocked
    const { data: blockData } = await supabase
      .from('blocked_users')
      .select('id')
      .or(`and(blocker_id.eq.${recipientId},blocked_id.eq.${senderId}),and(blocker_id.eq.${senderId},blocked_id.eq.${recipientId})`)
      .single()

    if (blockData) {
      throw new Error('Cannot send message to blocked user')
    }

    const { data, error } = await supabase
      .from('messages')
      .insert({
        sender_id: senderId,
        recipient_id: recipientId,
        content
      })
      .select()
      .single()

    if (error) throw error
    return data as Message
  },

  // Mark as read
  async markAsRead(messageId: string) {
    const { data, error } = await supabase
      .from('messages')
      .update({ read_at: new Date().toISOString() })
      .eq('id', messageId)
      .select()
      .single()

    if (error) throw error
    return data as Message
  },

  // Delete message
  async deleteMessage(messageId: string) {
    const { error } = await supabase
      .from('messages')
      .delete()
      .eq('id', messageId)

    if (error) throw error
  },

  // Get unread count
  async getUnreadCount(userId: string) {
    const { count, error } = await supabase
      .from('messages')
      .select('*', { count: 'exact', head: true })
      .eq('recipient_id', userId)
      .is('read_at', null)

    if (error) throw error
    return count || 0
  }
}