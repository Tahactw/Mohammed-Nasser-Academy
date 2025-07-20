#!/bin/bash

echo "🚀 Mohammed Nasser Academy Setup Script"
echo "======================================"

# Check if running from project root
if [ ! -d "client" ] || [ ! -d "server" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📦 Installing dependencies..."

# Install server dependencies
echo "Installing server dependencies..."
cd server
npm install
cd ..

# Install client dependencies
echo "Installing client dependencies..."
cd client
npm install
cd ..

echo "🗄️ Setting up database..."
echo "Please run the updated schema in your Supabase SQL editor:"
echo "File: supabase_schema_updated.sql"

echo ""
echo "⚙️ Configuration needed:"
echo "1. Make sure your .env files are properly configured"
echo "2. Update Supabase URL and keys in both client and server"
echo "3. Create storage buckets in Supabase: 'avatars', 'books', 'courses'"
echo "4. Set admin user email to 'admin@admin.com' in database"

echo ""
echo "✅ Setup complete! To start the application:"
echo "   Terminal 1: cd server && npm run dev"
echo "   Terminal 2: cd client && npm run dev"

echo ""
echo "📱 Social media links in Navbar.jsx need to be updated with your actual URLs"
echo ""
echo "🎉 Happy coding!"
