.PHONY: help
.DEFAULT_GOAL := help

# ==============================================================================
#                              Variables
# ==============================================================================
PACKAGE_NAME := market-beacon
IMAGE_NAME := market-beacon
VENV_NAME := ".$(PACKAGE_NAME)-venv"
PYTHON := $(VENV_NAME)/bin/python
BUMP := $(VENV_NAME)/bin/bump-my-version

# ==============================================================================
#                              Setup & Installation
# ==============================================================================
venv: ## Creates development virtual environment.
	@echo "--> Creating virtual environment..."
	python3.12 -m venv $(VENV_NAME)
	@echo "--> Upgrading pip..."
	@$(PYTHON) -m pip install -U pip setuptools wheel
	@echo "--> venv created in $(VENV_NAME)"

install: venv ## Installs project dependencies for development.
	@echo "--> Installing dependencies from pyproject.toml..."
	@$(PYTHON) -m pip install -e ".[dev]"
	@echo "--> Installing pre-commit hooks..."
	@$(VENV_NAME)/bin/pre-commit install
	@echo "--> Installation complete."

# ==============================================================================
#                              Code Quality & Testing
# ==============================================================================
lint: ## Runs the ruff linter and formatter (with auto-fix).
	@echo "--> Running Ruff Formatter..."
	@$(PYTHON) -m ruff format .
	@echo "--> Running Ruff Linter (with auto-fix)..."
	@$(PYTHON) -m ruff check --fix .

check: ## Runs ruff in check-only mode (for CI).
	@echo "--> Checking formatting with Ruff..."
	@$(PYTHON) -m ruff format . --check
	@echo "--> Checking linting with Ruff..."
	@$(PYTHON) -m ruff check .

test: ## Runs all tests with pytest.
	@echo "--> Running tests with pytest..."
	@$(PYTHON) -m pytest tests/

# ==============================================================================
#                              Versioning
# ==============================================================================
version-major: ## Bumps the major version number.
	@echo "--> Bumping MAJOR version..."
	@$(BUMP) bump major

version-minor: ## Bumps the minor version number.
	@echo "--> Bumping MINOR version..."
	@$(BUMP) bump minor

version-patch: ## Bumps the patch version number.
	@echo "--> Bumping PATCH version..."
	@$(BUMP) bump patch

# ==============================================================================
#                       Application & Docker Execution
# ==============================================================================
run: ## Runs the application. Pass args with 'make run args="..."'.
	@echo "--> Running application: $(PACKAGE_NAME)"
	@$(PYTHON) -m market_beacon $(args)

docker-build: ## Builds the Docker image.
	@echo "--> Building Docker image: $(IMAGE_NAME):latest"
	@docker build -t $(IMAGE_NAME):latest .

docker-run: ## Runs the application inside a Docker container.
	@echo "--> Running Docker container: $(IMAGE_NAME)"
	@docker run --rm -it --env-file .env $(IMAGE_NAME):latest

# ==============================================================================
#                              Cleanup
# ==============================================================================
clean: ## Removes virtual environment and cache files.
	@echo "--> Cleaning up..."
	rm -rf $(VENV_NAME)
	rm -rf .ruff_cache/ .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf src/*.egg-info

help: ## Shows this help message.
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
