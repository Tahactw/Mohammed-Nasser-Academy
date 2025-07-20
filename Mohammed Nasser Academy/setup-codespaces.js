#!/usr/bin/env node

import fs from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Detect if running in GitHub Codespaces
const isCodespaces = process.env.CODESPACES === 'true';
const codespaceHost = process.env.CODESPACE_NAME;

if (isCodespaces && codespaceHost) {
  console.log('🚀 Detected GitHub Codespaces environment');
  
  // Generate URLs
  const frontendUrl = `https://${codespaceHost}-3000.app.github.dev`;
  const backendUrl = `https://${codespaceHost}-5000.app.github.dev`;
  
  // Update client .env
  const clientEnvPath = join(__dirname, 'client', '.env');
  let clientEnv = fs.readFileSync(clientEnvPath, 'utf8');
  clientEnv = clientEnv.replace(/VITE_API_URL=.*/g, `VITE_API_URL=${backendUrl}`);
  fs.writeFileSync(clientEnvPath, clientEnv);
  
  // Update server .env
  const serverEnvPath = join(__dirname, 'server', '.env');
  let serverEnv = fs.readFileSync(serverEnvPath, 'utf8');
  serverEnv = serverEnv.replace(/FRONTEND_URL=.*/g, `FRONTEND_URL=${frontendUrl}`);
  fs.writeFileSync(serverEnvPath, serverEnv);
  
  console.log(`✅ Updated environment variables:`);
  console.log(`   Frontend URL: ${frontendUrl}`);
  console.log(`   Backend URL: ${backendUrl}`);
} else {
  console.log('📍 Running in local environment');
}
