import axios from 'axios';
import { supabase } from './supabase';

// Dynamically determine API URL with better Codespaces support
const getApiUrl = () => {
  // Check if we have an explicit API URL set
  if (import.meta.env.VITE_API_URL && import.meta.env.VITE_API_URL !== 'auto') {
    console.log('Using configured API URL:', import.meta.env.VITE_API_URL);
    return import.meta.env.VITE_API_URL;
  }
  
  // Detect GitHub Codespaces
  const hostname = window.location.hostname;
  if (hostname.includes('github.dev') || hostname.includes('app.github.dev')) {
    // In Codespaces, construct the backend URL by replacing port
    const backendUrl = window.location.origin.replace('-3000', '-5000');
    console.log('Detected Codespaces, using:', backendUrl);
    return backendUrl;
  }
  
  // Check if we're on localhost
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    console.log('Using localhost API');
    return 'http://localhost:5000';
  }
  
  // For production deployments
  if (window.location.protocol === 'https:') {
    // Assume API is on same domain but different port or path
    console.log('Using production API');
    return window.location.origin.replace(':3000', ':5000');
  }
  
  // Default fallback
  return 'http://localhost:5000';
};

const API_URL = getApiUrl();
console.log('API Base URL:', API_URL);

// Create axios instance with proper configuration
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for CORS with credentials
  timeout: 30000, // 30 second timeout
});

// Request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    try {
      // Get current session from Supabase
      const { data: { session } } = await supabase.auth.getSession();
      if (session?.access_token) {
        config.headers.Authorization = `Bearer ${session.access_token}`;
      }
      
      // Add timestamp to prevent caching issues
      if (config.method === 'get') {
        config.params = {
          ...config.params,
          _t: Date.now()
        };
      }
      
      // Log requests in development
      if (import.meta.env.DEV) {
        console.log(`📤 API Request: ${config.method?.toUpperCase()} ${config.url}`);
      }
    } catch (error) {
      console.error('Error in request interceptor:', error);
    }
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    // Log successful responses in development
    if (import.meta.env.DEV) {
      console.log(`📥 API Response: ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`);
    }
    return response;
  },
  async (error) => {
    // Enhanced error logging
    if (error.response) {
      // Server responded with error status
      console.error(`❌ API Error Response: ${error.response.status} - ${error.response.data?.error?.message || error.message}`);
      console.error('Error details:', {
        url: error.config?.url,
        method: error.config?.method,
        status: error.response.status,
        data: error.response.data
      });
      
      // Handle 401 Unauthorized
      if (error.response.status === 401) {
        const currentPath = window.location.pathname;
        if (!currentPath.includes('/login') && !currentPath.includes('/register')) {
          // Clear session and redirect to login
          await supabase.auth.signOut();
          window.location.href = '/login';
        }
      }
    } else if (error.request) {
      // Request made but no response received
      console.error('❌ API Error: No response received');
      console.error('Request details:', {
        url: error.config?.url,
        method: error.config?.method,
        baseURL: error.config?.baseURL
      });
      
      // Check if it's a CORS error
      if (error.message === 'Network Error') {
        console.error('Possible CORS issue. Check server CORS configuration and ensure backend is running.');
      }
    } else {
      // Error in request setup
      console.error('❌ API Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// Test function to verify API connectivity
export const testApiConnection = async () => {
  try {
    const response = await api.get('/health');
    console.log('✅ API connection test successful:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ API connection test failed:', error);
    throw error;
  }
};

// Export the configured instance
export default api;
