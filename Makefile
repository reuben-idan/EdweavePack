.PHONY: help build up down test deploy clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker images
	docker-compose build

up: ## Start development environment
	docker-compose up -d

down: ## Stop development environment
	docker-compose down

logs: ## Show logs
	docker-compose logs -f

test: ## Run all tests
	$(MAKE) test-backend
	$(MAKE) test-frontend

test-backend: ## Run backend tests
	cd backend && python -m pytest

test-frontend: ## Run frontend tests
	cd frontend && npm test -- --watchAll=false

lint: ## Run linting
	cd backend && flake8 . && black --check .
	cd frontend && npm run lint

format: ## Format code
	cd backend && black .
	cd frontend && npm run format

deploy-infra: ## Deploy infrastructure
	cd infrastructure && terraform init && terraform apply

deploy-prod: ## Deploy to production
	docker-compose -f docker-compose.prod.yml up -d

clean: ## Clean up containers and images
	docker-compose down -v
	docker system prune -f

demo: ## Run demo with sample data
	$(MAKE) up
	sleep 10
	docker-compose exec backend python scripts/seed_demo_data.py