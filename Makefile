# ==============================================================================
# SpatialAIFlow — Makefile
# ==============================================================================
# Common development commands. Run `make help` to see all targets.
# ==============================================================================

.DEFAULT_GOAL := help
.PHONY: help install dev lint format test test-cov docs clean

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in editable mode
	pip install -e .

dev:  ## Install with all development dependencies
	pip install -e ".[all,dev,docs]"
	pre-commit install

lint:  ## Run linter (ruff check + format check)
	ruff check src/ tests/
	ruff format --check src/ tests/

format:  ## Auto-format code
	ruff check --fix src/ tests/
	ruff format src/ tests/

test:  ## Run test suite
	pytest

test-cov:  ## Run tests with coverage report
	pytest --cov=spatialaiflow --cov-report=term-missing --cov-report=html

typecheck:  ## Run mypy type checker
	mypy src/spatialaiflow

docs:  ## Build documentation
	sphinx-build -b html docs/ docs/_build/html

clean:  ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/ htmlcov/
	rm -rf docs/_build/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
