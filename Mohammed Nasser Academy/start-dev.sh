#!/bin/bash

echo "🚀 Starting Mohammed Nasser Academy Development Environment..."
echo "📝 MongoDB is optional — the app will work without it"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if port is in use
check_port() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1
}

# Kill processes on given ports
echo "🧹 Cleaning up ports 3000 and 5000 if needed..."
for port in 3000 5000; do
    if check_port $port; then
        echo "⚠️ Killing process on port $port"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
    fi
done

# Install all dependencies if needed
if [ ! -d "server/node_modules" ] || [ ! -d "client/node_modules" ]; then
    echo "📦 Installing all dependencies..."
    npm run install:all
fi

# Start backend
echo -e "${GREEN}🚀 Starting backend server...${NC}"
cd server
npm run dev > ../server.log 2>&1 &
SERVER_PID=$!
cd ..

# Wait a bit for backend
sleep 5
if ! check_port 5000; then
    echo -e "${RED}❌ Backend failed to start. Check server.log${NC}"
    cat server.log
    exit 1
fi
echo -e "${GREEN}✅ Backend is running!${NC}"
npm run test:api

# Start frontend
echo -e "${GREEN}🚀 Starting frontend...${NC}"
cd client
npm run dev > ../client.log 2>&1 &
CLIENT_PID=$!
cd ..

# Wait for frontend
sleep 5
if ! check_port 3000; then
    echo -e "${RED}❌ Frontend failed to start. Check client.log${NC}"
    cat client.log
    exit 1
fi

# Final summary
echo -e "
${GREEN}✅ Development environment is ready!${NC}

📡 Access:
  - Frontend: ${YELLOW}http://localhost:3000${NC}
  - Backend:  ${YELLOW}http://localhost:5000${NC}

🛠️ Commands:
  - Backend logs:  ${YELLOW}npm run logs:server${NC}
  - Frontend logs: ${YELLOW}npm run logs:client${NC}
  - Stop all:      ${YELLOW}kill $SERVER_PID $CLIENT_PID${NC}

Press Ctrl+C to stop all services...
"

# Handle exit
trap "echo '⛔ Stopping...'; kill $SERVER_PID $CLIENT_PID 2>/dev/null; exit" INT TERM

# Keep processes alive
wait $SERVER_PID $CLIENT_PID
