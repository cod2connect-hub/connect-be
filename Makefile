UV ?= uv
UV_CACHE_DIR ?= $(CURDIR)/.uv-cache
PYTEST ?= $(UV) run pytest
COMPOSE ?= docker compose

export UV_CACHE_DIR

.DEFAULT_GOAL := help

.PHONY: help install dev worker services-up services-down services-logs migrate migration \
	test test-unit test-integration test-e2e lint format invariants check clean

help:
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_-]+:.*## / {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install locked development dependencies
	$(UV) sync --frozen --all-extras

dev: ## Run the FastAPI development server
	$(UV) run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

worker: ## Run the ARQ worker
	$(UV) run arq app.workers.main.WorkerSettings

services-up: ## Start Redis, Mailpit, and MinIO
	$(COMPOSE) up -d

services-down: ## Stop local supporting services
	$(COMPOSE) down

services-logs: ## Follow local service logs
	$(COMPOSE) logs -f

migrate: ## Apply all database migrations
	$(UV) run alembic -c migrations/alembic.ini upgrade head

migration: ## Create a migration: make migration name=short_description
	@test -n "$(name)" || (echo "name is required" && exit 1)
	$(UV) run alembic -c migrations/alembic.ini revision -m "$(name)"

test: ## Run the normal suite, excluding end-to-end tests
	$(PYTEST) -q -m "not e2e"

test-unit: ## Run unit and application tests
	$(PYTEST) -q tests/unit tests/application

test-integration: ## Run integration, interface, contract, architecture, and security tests
	$(PYTEST) -q tests/infrastructure tests/interface tests/contract tests/architecture tests/security

test-e2e: ## Run end-to-end tests
	$(PYTEST) -q -m e2e tests/e2e

lint: ## Lint application, tests, migrations, and scripts
	$(UV) run ruff check app tests migrations scripts

format: ## Format application, tests, migrations, and scripts
	$(UV) run ruff format app tests migrations scripts

invariants: ## Check architecture, permissions, SQL safety, and RLS coverage
	$(UV) run python scripts/check_invariants.py

check: lint invariants test ## Run the local CI-equivalent checks
	$(UV) run python -m compileall -q app tests migrations scripts

clean: ## Remove local Python and test caches
	find app tests migrations scripts -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov
