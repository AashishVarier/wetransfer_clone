#!/bin/bash
# dev.sh - Local development helper

set -e

echo "═══════════════════════════════════════"
echo "  WeTransfer Clone - Local Development"
echo "═══════════════════════════════════════"
echo ""

# Change to repo root
cd "$(dirname "$0")/.." || exit 1

# Parse arguments
MODE="${1:-help}"

case "$MODE" in
  setup)
    echo "📦 Setting up development environment..."
    
    # Frontend setup
    echo ""
    echo "Frontend setup:"
    cd frontend
    npm install
    if [ ! -f .env.local ]; then
      cp .env.example .env.local
      echo "✓ Created frontend/.env.local (edit with your values)"
    fi
    cd ..
    
    # Backend setup
    echo ""
    echo "Backend setup:"
    cd backend
    if [ ! -d venv ]; then
      python3 -m venv venv
      echo "✓ Created Python venv"
    fi
    source venv/bin/activate
    pip install -r requirements.txt >/dev/null 2>&1
    echo "✓ Installed Python dependencies"
    if [ ! -f .env ]; then
      cp .env.example .env
      echo "✓ Created backend/.env (edit with your values)"
    fi
    cd ..
    
    echo ""
    echo "✅ Setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Edit frontend/.env.local"
    echo "2. Edit backend/.env"
    echo "3. Run: bash scripts/dev.sh frontend"
    echo "4. In another terminal: bash scripts/dev.sh backend"
    ;;
    
  frontend)
    echo "🚀 Starting frontend development server..."
    cd frontend
    npm run dev
    ;;
    
  backend)
    echo "🚀 Starting backend tests..."
    cd backend
    source venv/bin/activate 2>/dev/null || python3 -m venv venv && source venv/bin/activate
    pytest tests/ --tb=short -v
    ;;

  test|tests)
    echo "🧪 Running all tests..."
    
    echo ""
    echo "Frontend tests:"
    cd frontend
    npm run test:watch || npm run test
    cd ..
    
    echo ""
    echo "Backend tests:"
    cd backend
    source venv/bin/activate 2>/dev/null || python3 -m venv venv && source venv/bin/activate
    pytest tests/ --cov=src/ --tb=short -v
    cd ..
    ;;

  clean)
    echo "🧹 Cleaning build artifacts..."
    cd frontend && rm -rf node_modules dist .next || true
    cd ../backend && rm -rf venv __pycache__ .pytest_cache *.egg-info || true
    cd ..
    echo "✅ Cleaned!"
    ;;

  *)
    echo "Usage: bash scripts/dev.sh <command>"
    echo ""
    echo "Commands:"
    echo "  setup      - Initialize development environment"
    echo "  frontend   - Start frontend dev server (http://localhost:5173)"
    echo "  backend    - Run backend tests"
    echo "  test|tests - Run all tests"
    echo "  clean      - Remove build artifacts"
    echo ""
    echo "Examples:"
    echo "  bash scripts/dev.sh setup"
    echo "  bash scripts/dev.sh frontend"
    echo "  bash scripts/dev.sh backend"
    ;;
esac
