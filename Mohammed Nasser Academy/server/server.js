import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

// Load environment variables
dotenv.config();

// ES Module compatibility
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize app BEFORE using it
const app = express();
const PORT = process.env.PORT || 5000;
const HOST = '0.0.0.0'; // <--- Make backend publicly accessible

// Import routes
import authRoutes from './routes/auth.js';
import userRoutes from './routes/users.js';
import courseRoutes from './routes/courses.js';
import bookRoutes from './routes/books.js';
import reviewRoutes from './routes/reviews.js';
import paymentRoutes from './routes/payment.js';
import adminRoutes from './routes/admin.js';

// Import middleware
import errorHandler from './middleware/errorHandler.js';


// Dynamic CORS configuration for GitHub Codespaces
const getCorsOrigin = () => {
  if (process.env.CODESPACES === 'true') {
    const codespaceName = process.env.CODESPACE_NAME;
    if (codespaceName) {
      return [
        `https://${codespaceName}-3000.app.github.dev`,
        `https://${codespaceName}-5173.app.github.dev`,
        'http://localhost:3000',
        'http://localhost:5173'
      ];
    }
  }
  return process.env.CLIENT_URL || ['http://localhost:3000', 'http://localhost:5173'];
};

// Middleware
app.use(cors({
  origin: (origin, callback) => {
    const allowedOrigins = Array.isArray(getCorsOrigin()) ? getCorsOrigin() : [getCorsOrigin()];
    if (!origin) return callback(null, true);
    if (allowedOrigins.some(allowed => origin.startsWith(allowed))) {
      callback(null, true);
    } else {
      console.log(`CORS blocked origin: ${origin}`);
      console.log(`Allowed origins:`, allowedOrigins);
      callback(null, true); // Allow all for dev
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/courses', courseRoutes);
app.use('/api/books', bookRoutes);
app.use('/api/reviews', reviewRoutes);
app.use('/api/payment', paymentRoutes);
app.use('/api/admin', adminRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development',
    codespaces: process.env.CODESPACES === 'true',
    cors: getCorsOrigin()
  });
});

// Error handling
app.use(errorHandler);

// Start server publicly on 0.0.0.0
app.listen(PORT, HOST, () => {
  console.log(`✅ Server running on http://${HOST}:${PORT}`);
  console.log(`📚 Mohammed Nasser Academy API is ready`);
  if (process.env.CODESPACES === 'true') {
    console.log(`🌐 Running in GitHub Codespaces`);
    console.log(`🔗 Accepting requests from:`, getCorsOrigin());
  }
});
