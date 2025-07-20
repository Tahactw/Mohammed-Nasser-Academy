#!/usr/bin/env node
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Check both server and client env files
dotenv.config({ path: './server/.env' });
const clientEnv = dotenv.config({ path: './client/.env' });

console.log('🔍 Checking environment configuration...');
console.log('');

const requiredServerVars = [
  'SUPABASE_URL',
  'SUPABASE_ANON_KEY',
  'SUPABASE_SERVICE_ROLE_KEY',
  'JWT_SECRET',
  'PORT'
];

const requiredClientVars = [
  'VITE_SUPABASE_URL',
  'VITE_SUPABASE_ANON_KEY',
  'VITE_API_URL'
];

let hasErrors = false;

console.log('📋 Server Environment Variables:');
requiredServerVars.forEach(varName => {
  if (process.env[varName]) {
    console.log(`✅ ${varName}: Set`);
  } else {
    console.log(`❌ ${varName}: Missing`);
    hasErrors = true;
  }
});

console.log('');
console.log('📋 Client Environment Variables:');
// Need to re-read for client vars
const clientVars = dotenv.parse(require('fs').readFileSync('./client/.env'));
requiredClientVars.forEach(varName => {
  if (clientVars[varName] || process.env[varName]) {
    console.log(`✅ ${varName}: Set`);
  } else {
    console.log(`❌ ${varName}: Missing`);
    hasErrors = true;
  }
});

if (hasErrors) {
  console.log('');
  console.log('❌ Some environment variables are missing!');
  console.log('Please check your .env files in both /server and /client directories.');
  process.exit(1);
} else {
  console.log('');
  console.log('✅ All required environment variables are set!');
}
