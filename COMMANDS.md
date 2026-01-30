# Quick Reference - All Commands

## First Time Setup

### Option 1: Automated Setup (Recommended)
```bash
cd /Users/stone/Documents/Projects/spiritual-gifts
./setup.sh
```

### Option 2: Manual Setup
```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_data

# Frontend
cd ../frontend
npm install
```

## Running the Application

### Option 1: Using Docker (Production-Ready)
```bash
# Start everything
docker-compose up --build

# Run in background
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

**Access:**
- Frontend: http://localhost
- Backend API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

### Option 2: Local Development
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

### Option 3: Automated Start Script
```bash
./start.sh
```

## Common Commands

### Backend
```bash
cd backend
source venv/bin/activate  # Activate virtual environment

# Database
python manage.py migrate           # Apply migrations
python manage.py makemigrations    # Create new migrations
python manage.py populate_data     # Load questions from questions.md

# Admin
python manage.py createsuperuser   # Create admin user

# Server
python manage.py runserver         # Start development server
```

### Frontend
```bash
cd frontend

# Development
npm install                        # Install dependencies
npm run dev                        # Start dev server

# Production
npm run build                      # Build for production
npm run preview                    # Preview production build
```

### Docker
```bash
# Build and start
docker-compose up --build          # Build and start all services
docker-compose up -d               # Run in background

# Management
docker-compose down                # Stop all services
docker-compose down -v             # Stop and remove volumes
docker-compose restart backend     # Restart backend service
docker-compose restart frontend    # Restart frontend service

# Logs
docker-compose logs -f             # All logs
docker-compose logs -f backend     # Backend logs only
docker-compose logs -f frontend    # Frontend logs only

# Execute commands
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py populate_data
docker-compose exec backend python manage.py migrate
```

## Updating Questions

1. Edit `questions.md` with your changes
2. Run populate command:
   ```bash
   # Local
   cd backend
   python manage.py populate_data
   
   # Docker
   docker-compose exec backend python manage.py populate_data
   ```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9

# Kill process on port 80 (Docker frontend)
lsof -ti:80 | xargs kill -9
```

### Reset Database
```bash
# Local
cd backend
rm db.sqlite3
python manage.py migrate
python manage.py populate_data

# Docker
docker-compose down -v
docker-compose up --build
```

### Migration Issues
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### Frontend Build Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues
```bash
# Remove all containers and images
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose up --build
```

## File Locations

### Configuration
- Backend settings: `backend/spiritual_gifts/settings.py`
- Frontend config: `frontend/vite.config.js`
- Docker config: `docker-compose.yml`
- Questions source: `questions.md`

### Code
- Backend models: `backend/survey/models.py`
- Backend API: `backend/survey/views.py`
- Frontend survey: `frontend/src/views/SurveyView.vue`
- Frontend results: `frontend/src/views/ResultsView.vue`

### Database
- Local: `backend/db.sqlite3`
- Docker: Volume `sqlite-data`

## URLs

### Local Development
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/
- API Questions: http://localhost:8000/api/questions/
- API Gifts: http://localhost:8000/api/spiritual-gifts/

### Docker Deployment
- Frontend: http://localhost
- Backend API: http://localhost:8000/api/ or http://localhost/api/
- Admin Panel: http://localhost:8000/admin/ or http://localhost/admin/

## Key Features

- ✅ 80 survey questions
- ✅ 16 spiritual gifts
- ✅ 5-point rating scale
- ✅ Automatic scoring
- ✅ Beautiful results visualization
- ✅ Mobile responsive
- ✅ Docker ready
- ✅ Questions from questions.md
- ✅ Data persistence

## Quick Test

```bash
# Start the app (choose one)
./start.sh                    # Local
docker-compose up -d          # Docker

# Visit in browser
open http://localhost:5173    # Local
open http://localhost         # Docker

# Create admin user
python manage.py createsuperuser                      # Local
docker-compose exec backend python manage.py createsuperuser  # Docker

# Check admin panel
open http://localhost:8000/admin/                     # Local
open http://localhost/admin/                          # Docker
```

## Support

- Full docs: `README.md`
- Quick start: `QUICKSTART.md`
- Docker guide: `DOCKER.md`
- Implementation: `IMPLEMENTATION_SUMMARY.md`
- Features: `FEATURES_OVERVIEW.md`
- Changes: `improvements.md`

---

**Most Common Workflow:**

```bash
# First time
./setup.sh

# Every time after
./start.sh

# Or with Docker
docker-compose up -d
```

That's it! 🎉
