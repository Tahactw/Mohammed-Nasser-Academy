#!/bin/bash
echo "🚀 Setting up Mohammed Nasser Academy..."
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check environment files
if [ ! -f "server/.env" ]; then
    echo "❌ server/.env file not found!"
    echo "Please copy server/.env.example to server/.env and fill in your values."
    exit 1
fi

if [ ! -f "client/.env" ]; then
    echo "❌ client/.env file not found!"
    echo "Please copy client/.env.example to client/.env and fill in your values."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install
cd server && npm install && cd ..
cd client && npm install && cd ..

# Check environment variables
echo ""
echo "🔍 Checking environment configuration..."
node check-env.js

# Set up database
echo ""
echo "🗄️ Setting up database..."
node setup-database.js

# Set up storage
echo ""
echo "💾 Setting up storage buckets..."
node setup-storage.js

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the development server, run:"
echo "  npm run dev"
