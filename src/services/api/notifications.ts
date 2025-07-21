import { supabase } from '../supabase'
import { Notification } from '@/types'

export const notificationsApi = {
  // Get user notifications
  async getUserNotifications(userId: string) {
    const { data, error } = await supabase
      .from('notifications')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(50)

    if (error) throw error
    return data as Notification[]
  },

  // Create notification
  async create(notification: Omit<Notification, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('notifications')
      .insert(notification)
      .select()
      .single()

    if (error) throw error
    return data as Notification
  },

  // Mark as read
  async markAsRead(notificationId: string) {
    const { data, error } = await supabase
      .from('notifications')
      .update({ read_at: new Date().toISOString() })
      .eq('id', notificationId)
      .select()
      .single()

    if (error) throw error
    return data as Notification
  },

  // Mark all as read
  async markAllAsRead(userId: string) {
    const { error } = await supabase
      .from('notifications')
      .update({ read_at: new Date().toISOString() })
      .eq('user_id', userId)
      .is('read_at', null)

    if (error) throw error
  },

  // Delete notification
  async delete(notificationId: string) {
    const { error } = await supabase
      .from('notifications')
      .delete()
      .eq('id', notificationId)

    if (error) throw error
  },

  // Get unread count
  async getUnreadCount(userId: string) {
    const { count, error } = await supabase
      .from('notifications')
      .select('*', { count: 'exact', head: true })
      .eq('user_id', userId)
      .is('read_at', null)

    if (error) throw error
    return count || 0
  },

  // Create notification helpers
  async notifyGiftReceived(recipientId: string, gifterId: string, bookTitle: string) {
    return this.create({
      user_id: recipientId,
      type: 'gift',
      title: 'Gift Received',
      content: `You received "${bookTitle}" as a gift`,
      data: { gifterId, bookTitle }
    })
  },

  async notifyNewMessage(recipientId: string, senderId: string, senderName: string) {
    return this.create({
      user_id: recipientId,
      type: 'message',
      title: 'New Message',
      content: `${senderName} sent you a message`,
      data: { senderId }
    })
  },

  async notifyReviewLike(reviewerId: string, likerId: string, likerName: string) {
    return this.create({
      user_id: reviewerId,
      type: 'review_like',
      title: 'Review Liked',
      content: `${likerName} liked your review`,
      data: { likerId }
    })
  },

  async notifyReviewReply(reviewerId: string, replierId: string, replierName: string) {
    return this.create({
      user_id: reviewerId,
      type: 'review_reply',
      title: 'New Reply',
      content: `${replierName} replied to your review`,
      data: { replierId }
    })
  },

  async notifyProfileVisit(profileUserId: string, visitorId: string, visitorName: string) {
    return this.create({
      user_id: profileUserId,
      type: 'profile_visit',
      title: 'Profile Visit',
      content: `${visitorName} visited your profile`,
      data: { visitorId }
    })
  },

  async notifyCourseComplete(userId: string, courseTitle: string) {
    return this.create({
      user_id: userId,
      type: 'course_complete',
      title: 'Course Completed',
      content: `Congratulations! You completed "${courseTitle}"`,
      data: { courseTitle }
    })
  },

  async notifyCertificateIssued(userId: string, courseTitle: string) {
    return this.create({
      user_id: userId,
      type: 'certificate',
      title: 'Certificate Issued',
      content: `Your certificate for "${courseTitle}" is ready`,
      data: { courseTitle }
    })
  }
}