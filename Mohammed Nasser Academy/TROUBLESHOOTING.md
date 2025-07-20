# Troubleshooting Guide

## Common Issues and Solutions

### 1. CORS Errors

If you're getting CORS errors:

1. **Check that the backend is running**:
   ```bash
   cd server
   npm run dev
   ```

2. **Verify the backend URL**:
   - Open browser console
   - Check the "API URL:" log message
   - Make sure it matches your backend URL

3. **For GitHub Codespaces**:
   - Make sure port 5000 is forwarded
   - Set visibility to "Public" in the Ports tab
   - The URL should be: `https://[codespace-name]-5000.app.github.dev`

### 2. MongoDB Connection Issues

1. **For local development**:
   ```bash
   # Start MongoDB
   mongod
   
   # Initialize database
   node init-db.js
   ```

2. **For GitHub Codespaces**:
   - Use MongoDB Atlas (cloud database)
   - Update MONGODB_URI in server/.env

### 3. 302 Redirect Errors

This usually happens when:
- The backend port is not properly forwarded in Codespaces
- The backend is not running

Solution:
1. Check the Ports tab in Codespaces
2. Make sure port 5000 is forwarded and public
3. Restart the backend server

### 4. Authentication Issues

1. **Clear browser storage**:
   ```javascript
   localStorage.clear();
   sessionStorage.clear();
   ```

2. **Check Supabase credentials**:
   - Verify SUPABASE_URL and keys are correct
   - Check Supabase dashboard for any issues

### 5. API Request Failures

1. **Check browser console** for detailed error messages
2. **Check backend logs** for server-side errors
3. **Verify API endpoints** match between frontend and backend

## Development Tips

1. **Always run both servers**:
   ```bash
   npm run dev  # From root directory
   ```

2. **Check environment variables**:
   - Client: `.env` and `.env.development`
   - Server: `.env`

3. **For GitHub Codespaces**:
   - Use the "Ports" tab to manage port forwarding
   - Set ports to "Public" for external access
   - Use HTTPS URLs for API calls

4. **Debug mode**:
   ```bash
   # Run backend with debug logs
   cd server
   npm run dev:debug
   ```

## Quick Fixes

### Reset Everything
```bash
# Stop all servers
# Clear node_modules
rm -rf node_modules server/node_modules client/node_modules

# Reinstall
npm run install:all

# Start fresh
npm run dev
```

### Test Backend Health
```bash
# Check if backend is running
curl http://localhost:5000/health

# For Codespaces
curl https://[codespace-name]-5000.app.github.dev/health
```
