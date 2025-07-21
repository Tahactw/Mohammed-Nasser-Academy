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

  // Get single book
  async getById(id: string) {
    const { data, error } = await supabase
      .from('books')
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data as Book
  },

  // Search books
  async search(query: string) {
    const { data, error } = await supabase
      .from('books')
      .select('*')
      .or(`title.ilike.%${query}%,description.ilike.%${query}%`)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data as Book[]
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

  // Check if user owns book
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

  // Get user's books
  async getUserBooks(userId: string) {
    const { data, error } = await supabase
      .from('book_ownership')
      .select(`
        *,
        book:books(*)
      `)
      .eq('user_id', userId)
      .order('purchase_date', { ascending: false })

    if (error) throw error
    return data as BookOwnership[]
  },

  // Create book (admin)
  async create(book: Omit<Book, 'id' | 'created_at' | 'updated_at'>) {
    const { data, error } = await supabase
      .from('books')
      .insert(book)
      .select()
      .single()

    if (error) throw error
    return data as Book
  },

  // Update book (admin)
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

  // Delete book (admin)
  async delete(id: string) {
    const { error } = await supabase
      .from('books')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Gift book
  async gift(bookId: string, recipientId: string, message: string, gifterId: string) {
    // Check if recipient already owns the book
    const ownership = await this.checkOwnership(bookId, recipientId)
    if (ownership) {
      throw new Error('Recipient already owns this book')
    }

    const { data, error } = await supabase
      .from('book_ownership')
      .insert({
        book_id: bookId,
        user_id: recipientId,
        is_gift: true,
        gifted_by: gifterId,
        gift_message: message,
        purchase_date: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data as BookOwnership
  }
}