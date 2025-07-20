import { getSupabaseAdmin } from '../config/supabase.js';

export const supabaseHelpers = {
  async getUserById(userId) {
    const supabase = getSupabaseAdmin();
    const { data, error } = await supabase
      .from('users')
      .select('*')
      .eq('id', userId)
      .single();
    
    if (error) return null;
    return data;
  },

  async createUser(userData) {
    const supabase = getSupabaseAdmin();
    const { data, error } = await supabase
      .from('users')
      .insert(userData)
      .select()
      .single();
    
    if (error) throw error;
    return data;
  },

  async updateUser(userId, updates) {
    const supabase = getSupabaseAdmin();
    const { data, error } = await supabase
      .from('users')
      .update(updates)
      .eq('id', userId)
      .select()
      .single();
    
    if (error) throw error;
    return data;
  },

  async getUserBadges(userId) {
    const supabase = getSupabaseAdmin();
    const { data, error } = await supabase
      .from('user_badges')
      .select('*, badge:badge_templates(*)')
      .eq('user_id', userId);
    
    if (error) return [];
    return data;
  }
};