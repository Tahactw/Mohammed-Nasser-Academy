import { createClient } from '@supabase/supabase-js';

let supabase = null;
let supabaseAdmin = null;

// Initialize Supabase clients lazily
export function getSupabase() {
  if (!supabase) {
    if (!process.env.SUPABASE_URL || !process.env.SUPABASE_ANON_KEY) {
      throw new Error('Supabase environment variables not set. Make sure SUPABASE_URL and SUPABASE_ANON_KEY are defined.');
    }
    supabase = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_ANON_KEY
    );
  }
  return supabase;
}

export function getSupabaseAdmin() {
  if (!supabaseAdmin) {
    if (!process.env.SUPABASE_URL || !process.env.SUPABASE_SERVICE_ROLE_KEY) {
      throw new Error('Supabase admin environment variables not set. Make sure SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are defined.');
    }
    supabaseAdmin = createClient(
      process.env.SUPABASE_URL,
      process.env.SUPABASE_SERVICE_ROLE_KEY
    );
  }
  return supabaseAdmin;
}

// Helper to verify environment is loaded
export function checkEnvironment() {
  const required = ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY'];
  const missing = required.filter(key => !process.env[key]);
  
  if (missing.length > 0) {
    console.error('❌ Missing environment variables:', missing.join(', '));
    console.error('Make sure .env file exists and is loaded before importing routes');
    return false;
  }
  
  console.log('✅ Supabase environment variables loaded');
  return true;
}
