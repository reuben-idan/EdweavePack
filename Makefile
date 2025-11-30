.PHONY: help build up down logs test clean

help:
	@echo "EdweavePack - Local Development"
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start local development"
	@echo "  down      - Stop all services"
	@echo "  logs      - View logs"
	@echo "  test      - Run tests"
	@echo "  clean     - Clean up resources"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	cd backend && python -m pytest
	cd frontend && npm test

clean:
	docker-compose down -v
	docker system prune -f