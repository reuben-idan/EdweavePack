@echo off
echo Enhanced AI EdweavePack - Docker Deployment
echo ==========================================

echo Stopping existing containers...
docker-compose -f docker-compose.prod.yml down

echo Cleaning up old images...
docker system prune -f

echo Building fresh containers...
docker-compose -f docker-compose.prod.yml build --no-cache

echo Starting services...
docker-compose -f docker-compose.prod.yml up -d

echo Waiting for services to initialize...
timeout /t 30 /nobreak

echo Checking service status...
docker-compose -f docker-compose.prod.yml ps

echo.
echo Deployment complete!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Testing endpoints...
curl -s http://localhost:8000/health
curl -s http://localhost:3000

pause