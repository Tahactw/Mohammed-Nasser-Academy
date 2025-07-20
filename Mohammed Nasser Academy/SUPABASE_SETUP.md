# Mohammed Nasser Academy - Supabase Setup

## 🚀 Quick Start

### 1. Set up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Get your project URL and keys from Settings > API

### 2. Configure Environment

```bash
# Copy the template
cp server/.env.template server/.env

# Edit with your Supabase credentials
nano server/.env
```

### 3. Run Database Migration

1. Open your Supabase project dashboard
2. Go to SQL Editor
3. Copy contents of `supabase_schema.sql`
4. Paste and run in SQL Editor

### 4. Install Dependencies

```bash
# Install server dependencies
cd server && npm install

# Install client dependencies  
cd ../client && npm install
```

### 5. Start Development Server

```bash
# From project root
npm run dev
```

## 📁 Project Structure

```
server/
├── routes/          # API endpoints (Supabase integrated)
├── lib/            # Supabase helpers and utilities
├── middleware/     # Auth and error handling
└── server.js       # Express server (no MongoDB!)
```

## 🔑 Key Features

- ✅ Full Supabase integration
- ✅ Row Level Security (RLS)
- ✅ Real-time subscriptions ready
- ✅ No MongoDB required
- ✅ Type-safe queries
- ✅ Automatic timestamps

## 🛠️ Common Tasks

### Add a new user
```javascript
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123'
});
```

### Get user progress
```javascript
const progress = await supabaseHelpers.getUserCourseProgress(userId, courseId);
```

### Purchase a book
```javascript
await supabaseHelpers.purchaseBook(userId, bookId);
```

## 🚨 Troubleshooting

- **"Missing Supabase credentials"**: Check your .env file
- **"Permission denied"**: Check RLS policies in Supabase
- **"Table not found"**: Run the migration SQL

## 📚 Resources

- [Supabase Docs](https://supabase.com/docs)
- [RLS Guide](https://supabase.com/docs/guides/auth/row-level-security)
