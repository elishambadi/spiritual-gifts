# Docker Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker installed (https://docs.docker.com/get-docker/)
- Docker Compose installed (usually comes with Docker Desktop)

### Running the Application

1. **Build and start all services**:
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode** (background):
   ```bash
   docker-compose up -d
   ```

3. **Access the application**:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/

### Managing the Application

**Stop the application**:
```bash
docker-compose down
```

**Stop and remove volumes** (clears database):
```bash
docker-compose down -v
```

**View logs**:
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

**Restart a service**:
```bash
docker-compose restart backend
docker-compose restart frontend
```

**Rebuild after code changes**:
```bash
docker-compose up --build
```

### Create Admin User in Docker

```bash
docker-compose exec backend python manage.py createsuperuser
```

### Running Management Commands

**Populate data**:
```bash
docker-compose exec backend python manage.py populate_data
```

**Run migrations**:
```bash
docker-compose exec backend python manage.py migrate
```

**Create migrations**:
```bash
docker-compose exec backend python manage.py makemigrations
```

### Development vs Production

#### Development Setup (Current)
- Uses Django development server
- Hot reload enabled for backend
- Debug mode enabled
- SQLite database

#### Production Recommendations
1. Use PostgreSQL instead of SQLite
2. Set DEBUG=False
3. Configure proper SECRET_KEY
4. Use gunicorn/uWSGI for Django
5. Set up proper static file serving
6. Configure HTTPS/SSL
7. Use environment variables for secrets

### Docker Architecture

```
┌─────────────────────────────────────┐
│         Docker Compose              │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────┐  ┌──────────────┐│
│  │   Frontend   │  │   Backend    ││
│  │   (Nginx)    │  │  (Django)    ││
│  │   Port: 80   │  │  Port: 8000  ││
│  └──────┬───────┘  └──────┬───────┘│
│         │                  │        │
│         └──────────────────┘        │
│         spiritual-gifts-network     │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   SQLite Volume              │  │
│  │   (Persistent Storage)       │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Troubleshooting

**Port already in use**:
```bash
# Change ports in docker-compose.yml
# For frontend: "3000:80" instead of "80:80"
# For backend: "8001:8000" instead of "8000:8000"
```

**Database not populated**:
```bash
docker-compose exec backend python manage.py populate_data
```

**Container won't start**:
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Remove old containers and rebuild
docker-compose down
docker-compose up --build
```

**Clear everything and start fresh**:
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Backend
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@db:5432/spiritual_gifts

# Frontend
VITE_API_URL=http://localhost:8000
```

### Production Docker Compose

For production, create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=spiritual_gifts
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=changeme
    volumes:
      - postgres-data:/var/lib/postgresql/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    command: gunicorn spiritual_gifts.wsgi:application --bind 0.0.0.0:8000
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:changeme@db:5432/spiritual_gifts
    depends_on:
      - db

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend

volumes:
  postgres-data:
```

### Backup and Restore

**Backup database**:
```bash
docker-compose exec backend python manage.py dumpdata > backup.json
```

**Restore database**:
```bash
docker-compose exec -T backend python manage.py loaddata < backup.json
```

### Performance Optimization

1. **Use multi-stage builds** (already implemented in Dockerfile)
2. **Optimize image size**:
   - Use alpine-based images
   - Clean up apt/apk cache
3. **Volume mounting for development**:
   - Code changes reflect immediately
4. **Use Docker layer caching**:
   - Install dependencies before copying code

### Monitoring

**Check container status**:
```bash
docker-compose ps
```

**Monitor resource usage**:
```bash
docker stats
```

**Health checks**:
```bash
docker-compose exec backend curl http://localhost:8000/api/
```

---

## Summary

With Docker, you can:
- ✅ Deploy with one command: `docker-compose up`
- ✅ Ensure consistent environment across machines
- ✅ Easily scale services
- ✅ Simplify dependency management
- ✅ Quick teardown and rebuild

The application is now fully containerized and ready for deployment!
