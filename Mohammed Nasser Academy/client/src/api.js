import axios from 'axios';
import { supabase } from './supabase';

// Detect if we're in GitHub Codespaces
const isCodespaces = window.location.hostname.includes('.github.dev');
const codespaceName = window.location.hostname.split('.')[0];

// Determine API URL based on environment
const getApiUrl = () => {
  if (import.meta.env.VITE_API_URL && import.meta.env.VITE_API_URL !== 'auto') {
    return import.meta.env.VITE_API_URL;
  }
  
  if (isCodespaces) {
    return `https://${codespaceName}-5000.app.github.dev`;
  }
  
  return 'http://localhost:5000';
};

const API_URL = getApiUrl();

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  async (config) => {
    // Get the current session
    const { data: { session } } = await supabase.auth.getSession();
    
    if (session?.access_token) {
      config.headers.Authorization = `Bearer ${session.access_token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Try to refresh the session
      const { data: { session } } = await supabase.auth.refreshSession();
      if (session) {
        // Retry the request with new token
        error.config.headers.Authorization = `Bearer ${session.access_token}`;
        return api.request(error.config);
      }
    }
    return Promise.reject(error);
  }
);

export default api;