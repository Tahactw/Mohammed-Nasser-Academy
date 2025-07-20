# Mohammed Nasser Academy - Setup Guide

## 🚀 Quick Start

### 1. Set up Supabase

1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Go to Settings > API to get your keys

### 2. Configure Environment

```bash
# Copy the example file
cp server/.env.example server/.env

# Edit with your Supabase credentials
nano server/.env
```

Required variables:
- `SUPABASE_URL`: Your project URL
- `SUPABASE_ANON_KEY`: Public anon key
- `SUPABASE_SERVICE_ROLE_KEY`: Service role key (keep secret!)

### 3. Run Database Migration

1. Open Supabase SQL Editor
2. Copy contents of `supabase_schema.sql`
3. Paste and run

### 4. Install & Run

```bash
# Install dependencies
cd server && npm install
cd ../client && npm install

# Start development
cd .. && npm run dev
```

## 📚 Project Structure

```
server/
├── routes/         # API endpoints (ES modules)
├── lib/           # Supabase helpers
├── middleware/    # Express middleware
├── config/        # Configuration files
└── server.js      # Main server (ES modules)
```

## ✅ Features

- Full ES modules support
- Supabase integration
- Row Level Security
- Real-time ready
- Type-safe queries

## 🛠️ Common Issues

**Import errors**: Make sure all imports use `.js` extension
**Env variables**: Check `.env` file has all required variables
**CORS issues**: Update `ALLOWED_ORIGINS` in `.env`
