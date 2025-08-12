import { supabase } from '../supabase'
import { Book, BookOwnership } from '@/types'

export const booksApi = {
  // Get all books
  async getAll() {
    const { data, error } = await supabase
      .from('books')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as Book[]
  },

  // Get book by ID
  async getById(id: string) {
    const { data, error } = await supabase
      .from('books')
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data as Book
  },

  // Create book
  async create(book: Omit<Book, 'id' | 'created_at' | 'updated_at'>) {
    const { data, error } = await supabase
      .from('books')
      .insert(book)
      .select()
      .single()

    if (error) throw error
    return data as Book
  },

  // Update book
  async update(id: string, updates: Partial<Book>) {
    const { data, error } = await supabase
      .from('books')
      .update(updates)
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data as Book
  },

  // Delete book
  async delete(id: string) {
    const { error } = await supabase
      .from('books')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Get book owners
  async getOwners(bookId: string) {
    const { data, error } = await supabase
      .from('book_ownership')
      .select(`
        *,
        user:users(id, username, avatar_url)
      `)
      .eq('book_id', bookId)
      .order('purchase_date', { ascending: false })

    if (error) throw error
    return data as BookOwnership[]
  },

  // Check book ownership
  async checkOwnership(bookId: string, userId: string) {
    const { data, error } = await supabase
      .from('book_ownership')
      .select('id')
      .eq('book_id', bookId)
      .eq('user_id', userId)
      .single()

    if (error && error.code !== 'PGRST116') throw error
    return !!data
  },

  // Purchase book
  async purchase(bookId: string, userId: string, transactionId: string) {
    const { data, error } = await supabase
      .from('book_ownership')
      .insert({
        book_id: bookId,
        user_id: userId,
        transaction_id: transactionId,
        purchase_date: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data as BookOwnership
  },

  // Gift book
  async gift(bookId: string, gifterId: string, recipientId: string, message?: string) {
    const { data, error } = await supabase
      .from('book_ownership')
      .insert({
        book_id: bookId,
        user_id: recipientId,
        gifter_id: gifterId,
        gift_message: message,
        is_gift: true,
        purchase_date: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data as BookOwnership
  },

  // Get user's books
  async getUserBooks(userId: string) {
    const { data, error } = await supabase
      .from('book_ownership')
      .select(`
        *,
        book:books(*),
        gifter:users!book_ownership_gifter_id_fkey(id, username, avatar_url)
      `)
      .eq('user_id', userId)
      .order('purchase_date', { ascending: false })

    if (error) throw error
    return data as BookOwnership[]
  }
}