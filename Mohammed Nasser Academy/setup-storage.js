import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config({ path: './client/.env' });

const supabaseUrl = process.env.VITE_SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_KEY || process.env.VITE_SUPABASE_ANON_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function setupStorage() {
  try {
    console.log('Setting up Supabase storage buckets...');
    
    // Create avatars bucket
    const { data: avatarsBucket, error: avatarsError } = await supabase.storage.createBucket('avatars', {
      public: true,
      allowedMimeTypes: ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'],
      fileSizeLimit: 5242880, // 5MB
    });
    
    if (avatarsError && !avatarsError.message.includes('already exists')) {
      throw avatarsError;
    }
    
    console.log('✅ Avatars bucket ready');
    
    // Create books bucket (for book covers and files)
    const { data: booksBucket, error: booksError } = await supabase.storage.createBucket('books', {
      public: false,
      allowedMimeTypes: ['image/*', 'application/pdf'],
      fileSizeLimit: 52428800, // 50MB
    });
    
    if (booksError && !booksError.message.includes('already exists')) {
      throw booksError;
    }
    
    console.log('✅ Books bucket ready');
    
    console.log('\n📦 Storage setup complete!');
    console.log('\nNote: Make sure to set up RLS policies in Supabase dashboard:');
    console.log('1. Go to Storage > Policies');
    console.log('2. For avatars bucket: Allow public read, authenticated users can upload/update their own');
    console.log('3. For books bucket: Only authenticated users who purchased can download');
    
  } catch (error) {
    console.error('❌ Storage setup error:', error);
  }
}

setupStorage();
