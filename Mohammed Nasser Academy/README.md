# Writer & Instructor Platform

A full-stack platform for writers and instructors featuring courses, books, and community interaction.

## Tech Stack
- Frontend: React + Vite + Material-UI
- Backend: Node.js + Express + MongoDB
- Auth & Storage: Supabase
- Payment: Paymob
- Deployment: Vercel

## Setup

### Prerequisites
- Node.js 18+
- MongoDB
- Supabase account
- Paymob account

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   # Install server dependencies
   cd server && npm install
   
   # Install client dependencies
   cd ../client && npm install
   ```

3. Set up environment variables (see .env.example files)

4. Run the development servers:
   ```bash
   # Start backend (from server directory)
   npm run dev
   
   # Start frontend (from client directory)
   npm run dev
   ```

## Features
- Interactive hero page
- Pay What You Want book purchases
- Sequential course progression
- User profiles with badges
- Community discussions
- Admin panel for course management

## 🚀 Quick Setup

### Prerequisites
- Node.js (v18 or higher)
- Supabase account (free tier works)
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "Mohammed Nasser Academy"
   ```

2. **Set up environment variables**
   - Copy `server/.env.example` to `server/.env`
   - Copy `client/.env.example` to `client/.env`
   - Fill in your Supabase credentials and other required values

3. **Run the setup script**
   ```bash
   ./setup.sh
   ```

4. **Set up the database**
   - Go to your Supabase project dashboard
   - Navigate to SQL Editor
   - Copy the contents of `supabase_schema.sql`
   - Paste and run in the SQL editor

5. **Start the development server**
   ```bash
   npm run dev
   ```

The application will be available at:
- Frontend: http://localhost:5173
- Backend: http://localhost:5000

## 🔧 Troubleshooting

If you encounter issues:
1. Check environment variables: `node check-env.js`
2. Check server logs: `cat server.log`
3. Refer to `TROUBLESHOOTING.md` for common issues
