import { createClient } from '@supabase/supabase-js';

// Use the service role key from server .env
const supabaseUrl = 'https://qkfgvniqkwbrvolkedsv.supabase.co';
const supabaseServiceKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFrZmd2bmlxa3dicnZvbGtlZHN2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Mjc3NTA4MywiZXhwIjoyMDY4MzUxMDgzfQ.n4y_Q9ysQwnrZLifjEoOO4bLD28AYe4eQdhoD-oKNz4';

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function createBuckets() {
  try {
    console.log('Creating storage buckets...');
    
    // List existing buckets
    const { data: existingBuckets } = await supabase.storage.listBuckets();
    console.log('Existing buckets:', existingBuckets?.map(b => b.name) || []);
    
    // Create avatars bucket if it doesn't exist
    const avatarsBucketExists = existingBuckets?.some(b => b.name === 'avatars');
    
    if (!avatarsBucketExists) {
      const { data: avatarsBucket, error: avatarsError } = await supabase.storage.createBucket('avatars', {
        public: true,
        allowedMimeTypes: ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'],
        fileSizeLimit: 5242880, // 5MB
      });
      
      if (avatarsError) {
        console.error('Error creating avatars bucket:', avatarsError);
      } else {
        console.log('✅ Avatars bucket created');
      }
    } else {
      console.log('✅ Avatars bucket already exists');
    }
    
    // Create books bucket if it doesn't exist
    const booksBucketExists = existingBuckets?.some(b => b.name === 'books');
    
    if (!booksBucketExists) {
      const { data: booksBucket, error: booksError } = await supabase.storage.createBucket('books', {
        public: false,
        allowedMimeTypes: ['image/*', 'application/pdf'],
        fileSizeLimit: 52428800, // 50MB
      });
      
      if (booksError) {
        console.error('Error creating books bucket:', booksError);
      } else {
        console.log('✅ Books bucket created');
      }
    } else {
      console.log('✅ Books bucket already exists');
    }
    
    console.log('\n✅ Storage setup complete!');
    console.log('\n📝 Next steps:');
    console.log('1. Go to your Supabase dashboard');
    console.log('2. Navigate to Storage > Policies');
    console.log('3. For the "avatars" bucket, create a policy:');
    console.log('   - Allow public SELECT (read)');
    console.log('   - Allow authenticated INSERT and UPDATE');
    console.log('4. For the "books" bucket, create policies for authenticated access');
    
  } catch (error) {
    console.error('❌ Error setting up storage:', error);
  }
}

createBuckets();
