# DevDocAI Database System Makefile
# Simplifies common operations for the multi-database system

.PHONY: help install setup start stop clean test ingest query server logs backup restore

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)DevDocAI Database System Commands:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Install Python dependencies
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

setup: ## Set up environment and databases
	@echo "$(BLUE)Setting up environment...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(YELLOW)⚠ Created .env file. Please configure with your API keys.$(NC)"; \
	fi
	@echo "$(BLUE)Starting Docker services...$(NC)"
	docker-compose up -d
	@echo "$(BLUE)Waiting for services to be ready...$(NC)"
	@sleep 10
	@echo "$(BLUE)Initializing databases...$(NC)"
	python setup_databases.py
	@echo "$(GREEN)✓ Setup complete$(NC)"

start: ## Start all Docker services
	@echo "$(BLUE)Starting Docker services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Services started$(NC)"
	@docker-compose ps

stop: ## Stop all Docker services
	@echo "$(BLUE)Stopping Docker services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

clean: ## Clean up all data and containers
	@echo "$(RED)⚠ Warning: This will delete all data!$(NC)"
	@read -p "Are you sure? (y/N) " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)Cleaning up...$(NC)"; \
		docker-compose down -v; \
		rm -rf data/; \
		rm -rf logs/; \
		rm -rf __pycache__/; \
		find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true; \
		echo "$(GREEN)✓ Cleanup complete$(NC)"; \
	else \
		echo "$(YELLOW)Cleanup cancelled$(NC)"; \
	fi

test: ## Run system tests
	@echo "$(BLUE)Running system tests...$(NC)"
	python main.py test --config config.yaml
	@echo "$(GREEN)✓ Tests complete$(NC)"

ingest: ## Ingest DevDocAI documentation
	@echo "$(BLUE)Ingesting documentation...$(NC)"
	python document_ingestion.py --documents ../../../Docs
	@echo "$(GREEN)✓ Ingestion complete$(NC)"

query: ## Run interactive query interface
	@echo "$(BLUE)Starting interactive query interface...$(NC)"
	python ai_agent_interface.py --interactive

server: ## Start the FastAPI server
	@echo "$(BLUE)Starting FastAPI server...$(NC)"
	python main.py server --host 0.0.0.0 --port 8000

logs: ## Show Docker service logs
	@echo "$(BLUE)Showing logs (Ctrl+C to exit)...$(NC)"
	docker-compose logs -f

backup: ## Backup all databases
	@echo "$(BLUE)Creating backups...$(NC)"
	@mkdir -p backups
	@echo "  Backing up PostgreSQL..."
	@docker-compose exec -T postgres pg_dump -U postgres devdocai > backups/postgres_$$(date +%Y%m%d_%H%M%S).sql
	@echo "  Backing up Neo4j..."
	@docker-compose exec -T neo4j neo4j-admin database dump neo4j --to-stdout > backups/neo4j_$$(date +%Y%m%d_%H%M%S).dump
	@echo "  Backing up Redis..."
	@docker-compose exec -T redis redis-cli SAVE
	@docker cp $$(docker-compose ps -q redis):/data/dump.rdb backups/redis_$$(date +%Y%m%d_%H%M%S).rdb
	@echo "$(GREEN)✓ Backups created in ./backups/$(NC)"

restore: ## Restore databases from backup
	@echo "$(BLUE)Available backups:$(NC)"
	@ls -la backups/
	@echo ""
	@read -p "Enter backup date (YYYYMMDD_HHMMSS): " backup_date; \
	if [ -f "backups/postgres_$$backup_date.sql" ]; then \
		echo "$(BLUE)Restoring PostgreSQL...$(NC)"; \
		docker-compose exec -T postgres psql -U postgres devdocai < backups/postgres_$$backup_date.sql; \
		echo "$(GREEN)✓ PostgreSQL restored$(NC)"; \
	else \
		echo "$(RED)✗ PostgreSQL backup not found$(NC)"; \
	fi

status: ## Check system status
	@echo "$(BLUE)System Status:$(NC)"
	@echo ""
	@echo "$(BLUE)Docker Services:$(NC)"
	@docker-compose ps
	@echo ""
	@echo "$(BLUE)Database Connections:$(NC)"
	@python -c "from setup_databases import DatabaseSetup; s = DatabaseSetup(); v = s.verify_setup(); [print(f'  {'✅' if status else '❌'} {db}') for db, status in v.items()]" 2>/dev/null || echo "  $(RED)Unable to verify$(NC)"
	@echo ""
	@echo "$(BLUE)API Health:$(NC)"
	@curl -s http://localhost:8080/health | python -m json.tool 2>/dev/null || echo "  $(YELLOW)API not running$(NC)"

dev: ## Start development environment
	@echo "$(BLUE)Starting development environment...$(NC)"
	@make start
	@sleep 5
	@make test
	@echo "$(BLUE)Starting server in development mode...$(NC)"
	@python main.py server --host 0.0.0.0 --port 8000

prod: ## Start production environment
	@echo "$(BLUE)Starting production environment...$(NC)"
	@if [ ! -f config.prod.yaml ]; then \
		echo "$(RED)✗ config.prod.yaml not found$(NC)"; \
		exit 1; \
	fi
	@cp config.prod.yaml config.yaml
	@make start
	@sleep 10
	@python setup_databases.py
	@echo "$(BLUE)Starting server in production mode...$(NC)"
	@gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

monitor: ## Open monitoring dashboards
	@echo "$(BLUE)Opening monitoring dashboards...$(NC)"
	@echo "  Grafana: http://localhost:3000 (admin/admin)"
	@echo "  Prometheus: http://localhost:9090"
	@echo "  Kibana: http://localhost:5601"
	@echo "  Neo4j Browser: http://localhost:7474"

benchmark: ## Run performance benchmarks
	@echo "$(BLUE)Running performance benchmarks...$(NC)"
	@python -m pytest tests/test_performance.py --benchmark-only --benchmark-autosave
	@echo "$(GREEN)✓ Benchmarks complete$(NC)"

format: ## Format Python code
	@echo "$(BLUE)Formatting Python code...$(NC)"
	@black *.py
	@isort *.py
	@echo "$(GREEN)✓ Code formatted$(NC)"

lint: ## Run code linting
	@echo "$(BLUE)Running linters...$(NC)"
	@flake8 *.py --max-line-length=120
	@mypy *.py --ignore-missing-imports
	@echo "$(GREEN)✓ Linting complete$(NC)"

security: ## Run security checks
	@echo "$(BLUE)Running security checks...$(NC)"
	@bandit -r . -ll
	@safety check
	@echo "$(GREEN)✓ Security checks complete$(NC)"

docs: ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(NC)"
	@sphinx-build -b html docs/ docs/_build/
	@echo "$(GREEN)✓ Documentation generated in docs/_build/$(NC)"

docker-build: ## Build Docker image for the application
	@echo "$(BLUE)Building Docker image...$(NC)"
	@docker build -t devdocai-app:latest .
	@echo "$(GREEN)✓ Docker image built$(NC)"

docker-push: ## Push Docker image to registry
	@echo "$(BLUE)Pushing Docker image...$(NC)"
	@docker tag devdocai-app:latest your-registry/devdocai-app:latest
	@docker push your-registry/devdocai-app:latest
	@echo "$(GREEN)✓ Docker image pushed$(NC)"

# Default target
.DEFAULT_GOAL := help