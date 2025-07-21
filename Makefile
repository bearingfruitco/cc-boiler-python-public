# Python Agent System Makefile

.PHONY: help install dev test lint format clean security docs api cli setup

# Default target
help:
	@echo "Python Agent System - Available Commands"
	@echo "======================================="
	@echo "Setup & Installation:"
	@echo "  make install    - Install production dependencies"
	@echo "  make dev        - Install dev dependencies & pre-commit"
	@echo "  make setup      - Full project setup"
	@echo ""
	@echo "Development:"
	@echo "  make test       - Run tests with coverage"
	@echo "  make lint       - Run linting (ruff + mypy)"
	@echo "  make format     - Auto-format code"
	@echo "  make security   - Run security scans"
	@echo "  make clean      - Clean generated files"
	@echo ""
	@echo "Running:"
	@echo "  make cli        - Show CLI help"
	@echo "  make api        - Start API server"
	@echo "  make chat       - Start agent chat"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs       - Build documentation"
	@echo "  make docs-serve - Serve docs locally"

# Installation targets
install:
	poetry install --no-dev

dev:
	poetry install
	poetry run pre-commit install
	@echo "✅ Development environment ready!"

setup: dev
	cp .env.example .env
	mkdir -p .claude/sessions
	mkdir -p .claude/research
	mkdir -p data
	mkdir -p logs
	@echo "✅ Project setup complete! Edit .env with your API keys."

# Testing
test:
	poetry run pytest -v --cov=src --cov-report=html --cov-report=term

test-watch:
	poetry run ptw -- -v

test-unit:
	poetry run pytest -v -m unit

test-integration:
	poetry run pytest -v -m integration

# Code quality
lint:
	poetry run ruff check src tests
	poetry run mypy src

format:
	poetry run black src tests
	poetry run ruff check --fix src tests
	poetry run isort src tests

# Security
security:
	poetry run bandit -r src
	poetry run safety check
	poetry run pip-audit

# Cleaning
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov .pytest_cache .mypy_cache .ruff_cache
	rm -rf dist build *.egg-info

# Running services
cli:
	poetry run agent --help

api:
	poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

api-prod:
	poetry run uvicorn src.api.main:app --workers 4 --host 0.0.0.0 --port 8000

chat:
	poetry run agent agent chat --role data_analyst

# Documentation
docs:
	poetry run mkdocs build

docs-serve:
	poetry run mkdocs serve

# Docker
docker-build:
	docker build -t python-agent-system .

docker-run:
	docker run -p 8000:8000 --env-file .env python-agent-system

# Database
db-upgrade:
	poetry run alembic upgrade head

db-migrate:
	poetry run alembic revision --autogenerate -m "$(message)"

db-downgrade:
	poetry run alembic downgrade -1

# Utilities
shell:
	poetry run ipython

notebook:
	poetry run jupyter notebook

update-deps:
	poetry update
	poetry export -f requirements.txt --output requirements.txt --without-hashes

check-all: lint test security
	@echo "✅ All checks passed!"

# Git hooks
pre-commit: format lint test
	@echo "✅ Ready to commit!"

pre-push: check-all
	@echo "✅ Ready to push!"