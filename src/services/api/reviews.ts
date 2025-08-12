import { supabase } from '../supabase'
import { Review, ReviewReply } from '@/types'

export const reviewsApi = {
  // Get book reviews
  async getBookReviews(bookId: string) {
    const { data, error } = await supabase
      .from('reviews')
      .select(`
        *,
        user:users!reviews_user_id_fkey(id, username, avatar_url, is_banned),
        likes:review_likes(user_id)
      `)
      .eq('book_id', bookId)
      .order('created_at', { ascending: false })

    if (error) throw error
    
    // Filter out reviews from banned users
    const filteredData = (data || []).filter(review => !review.user?.is_banned)
    
    // Add likes count and user_has_liked
    const currentUser = await supabase.auth.getUser()
    const userId = currentUser.data.user?.id

    return filteredData.map(review => ({
      ...review,
      likes_count: review.likes?.length || 0,
      user_has_liked: userId ? review.likes?.some((like: any) => like.user_id === userId) : false
    })) as Review[]
  },

  // Get review replies
  async getReviewReplies(reviewId: string) {
    const { data, error } = await supabase
      .from('review_replies')
      .select(`
        *,
        user:users(id, username, avatar_url)
      `)
      .eq('review_id', reviewId)
      .order('created_at', { ascending: true })

    if (error) throw error
    return data as ReviewReply[]
  },

  // Create review
  async createReview(review: Omit<Review, 'id' | 'created_at' | 'updated_at' | 'likes_count' | 'user_has_liked'>) {
    const { data, error } = await supabase
      .from('reviews')
      .insert(review)
      .select()
      .single()

    if (error) throw error
    return data as Review
  },

  // Update review
  async updateReview(id: string, updates: Partial<Review>) {
    const { data, error } = await supabase
      .from('reviews')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as Review
  },

  // Delete review
  async deleteReview(id: string) {
    const { error } = await supabase
      .from('reviews')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Like review
  async likeReview(reviewId: string, userId: string) {
    const { error } = await supabase
      .from('review_likes')
      .insert({
        review_id: reviewId,
        user_id: userId
      })

    if (error) throw error
  },

  // Unlike review
  async unlikeReview(reviewId: string, userId: string) {
    const { error } = await supabase
      .from('review_likes')
      .delete()
      .eq('review_id', reviewId)
      .eq('user_id', userId)

    if (error) throw error
  },

  // Create reply
  async createReply(reply: Omit<ReviewReply, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('review_replies')
      .insert(reply)
      .select()
      .single()

    if (error) throw error
    return data as ReviewReply
  },

  // Delete reply
  async deleteReply(id: string) {
    const { error } = await supabase
      .from('review_replies')
      .delete()
      .eq('id', id)

    if (error) throw error
  }
}