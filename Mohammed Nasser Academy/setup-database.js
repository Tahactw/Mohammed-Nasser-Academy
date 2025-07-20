import { createClient } from '@supabase/supabase-js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables
dotenv.config({ path: './server/.env' });

async function setupDatabase() {
  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  
  if (!supabaseUrl || !supabaseServiceKey) {
    console.error('❌ Missing Supabase environment variables!');
    console.error('Please make sure SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set in server/.env');
    process.exit(1);
  }
  
  console.log('🚀 Setting up Supabase database...');
  console.log('');
  console.log('📝 Database Setup Instructions:');
  console.log('1. Go to your Supabase project dashboard');
  console.log('2. Navigate to SQL Editor');
  console.log('3. Copy the contents of supabase_schema.sql');
  console.log('4. Paste and run in the SQL editor');
  console.log('');
  console.log('The schema file is located at: ./supabase_schema.sql');
  console.log('');
  
  // Initialize Supabase client to test connection
  const supabase = createClient(supabaseUrl, supabaseServiceKey);
  
  try {
    // Test connection by checking if users table exists
    const { data, error } = await supabase
      .from('users')
      .select('count')
      .limit(1);
    
    if (error && error.code === '42P01') {
      console.log('❌ Database tables not found. Please run the SQL schema first.');
    } else if (error) {
      console.log('❌ Database connection error:', error.message);
    } else {
      console.log('✅ Database connection successful!');
      console.log('✅ Tables are set up correctly.');
    }
  } catch (error) {
    console.error('❌ Error connecting to database:', error.message);
  }
}

setupDatabase();
