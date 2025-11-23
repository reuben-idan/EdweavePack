# EdweavePack Setup Guide

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Git

### One-Command Setup
```bash
git clone https://github.com/reuben-idan/EdweavePack.git
cd EdweavePack
make demo
```

**Access Points:**
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs
- Flower (Celery): http://localhost:5555

## 📋 Detailed Setup

### 1. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Required Environment Variables:**
```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/edweavepack
REDIS_URL=redis://localhost:6379

# AWS (for production)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET=edweavepack-storage

# Security
JWT_SECRET=your-super-secret-jwt-key
SECRET_KEY=your-app-secret-key

# AI Services
OPENAI_API_KEY=your_openai_key  # Optional fallback
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 4. Background Services
```bash
# Start Redis (if not using Docker)
redis-server

# Start Celery worker
cd backend
celery -A main.celery worker --loglevel=info

# Start Celery flower (monitoring)
celery -A main.celery flower
```

## 🐳 Docker Development

### Full Stack with Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Services
```bash
# Backend only
docker-compose up backend postgres redis

# Frontend only
docker-compose up frontend

# Workers only
docker-compose up celery flower
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test

# Coverage report
npm test -- --coverage --watchAll=false
```

### Integration Tests
```bash
# Full test suite
make test

# Individual components
make test-backend
make test-frontend
```

## 🔧 Development Tools

### Database Management
```bash
# Create migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Quality
```bash
# Backend linting
cd backend
flake8 .
black .

# Frontend linting
cd frontend
npm run lint
npm run format
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 📊 Monitoring & Debugging

### Local Monitoring
- **Flower (Celery)**: http://localhost:5555
- **Database**: Use pgAdmin or similar tool
- **Redis**: Use Redis CLI or GUI tool

### Logging
```bash
# View application logs
docker-compose logs -f backend

# View worker logs
docker-compose logs -f celery

# View all logs
docker-compose logs -f
```

### Debug Mode
```bash
# Backend debug mode
export DEBUG=True
uvicorn main:app --reload --log-level debug

# Frontend debug mode
export REACT_APP_DEBUG=true
npm start
```

## 🚀 Production Deployment

### AWS Infrastructure
```bash
# Deploy infrastructure
cd infrastructure
terraform init
terraform apply

# Build and deploy
./deploy.sh all
```

### Manual Deployment
```bash
# Build Docker images
docker build -t edweavepack-backend ./backend
docker build -t edweavepack-frontend ./frontend

# Push to registry
docker tag edweavepack-backend:latest your-registry/backend:latest
docker push your-registry/backend:latest
```

## 🔍 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check PostgreSQL status
docker-compose ps postgres

# Reset database
docker-compose down -v
docker-compose up postgres
```

**Redis Connection Error**
```bash
# Check Redis status
docker-compose ps redis

# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL
```

**Frontend Build Errors**
```bash
# Clear node modules
rm -rf node_modules package-lock.json
npm install

# Clear React cache
npm start -- --reset-cache
```

**Celery Worker Issues**
```bash
# Restart workers
docker-compose restart celery

# Check worker status
celery -A main.celery inspect active
```

### Performance Optimization

**Database Performance**
```sql
-- Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 10;

-- Add indexes for common queries
CREATE INDEX idx_curriculum_user_id ON curricula(user_id);
CREATE INDEX idx_assessment_curriculum_id ON assessments(curriculum_id);
```

**Redis Optimization**
```bash
# Monitor Redis memory usage
redis-cli info memory

# Set memory policy
redis-cli config set maxmemory-policy allkeys-lru
```

## 📚 Additional Resources

- [API Documentation](http://localhost:8000/docs)
- [Architecture Overview](docs/architecture.md)
- [Deployment Guide](docs/deployment.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Demo Assets](demo/)

## 🆘 Getting Help

1. **Check Documentation**: Review setup guide and troubleshooting
2. **Search Issues**: Look for similar problems in GitHub issues
3. **Create Issue**: Provide detailed error logs and environment info
4. **Community**: Join our Discord/Slack for real-time help

## 🔄 Development Workflow

1. **Fork Repository**: Create your own fork
2. **Create Branch**: `git checkout -b feature/your-feature`
3. **Make Changes**: Follow coding standards
4. **Run Tests**: Ensure all tests pass
5. **Submit PR**: Include description and tests
6. **Code Review**: Address feedback
7. **Merge**: Squash and merge when approved