.PHONY: help build up down logs test clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

test-backend: ## Run backend tests
	cd backend && python -m pytest tests/ -v

test-frontend: ## Run frontend tests
	cd frontend && npm test

test: test-backend test-frontend ## Run all tests

clean: ## Clean up Docker resources
	docker-compose down -v
	docker system prune -f

dev-setup: ## Set up development environment
	@echo "Setting up Edweave Pack development environment..."
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	@echo "Development environment ready!"

deploy-infra: ## Deploy infrastructure with Terraform
	cd infrastructure && terraform init && terraform plan && terraform apply

demo: ## Start demo environment
	@echo "Starting Edweave Pack demo..."
	docker-compose up -d
	@echo "Demo available at http://localhost:3000"
	@echo "API documentation at http://localhost:8000/docs"