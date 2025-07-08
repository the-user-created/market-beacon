.PHONY: help
.DEFAULT_GOAL := help

# ==============================================================================
#                              Variables
# ==============================================================================
PACKAGE_NAME := market-beacon
IMAGE_NAME := market-beacon
PROJECT_VERSION := $(shell awk '/^\[project\]$$/{f=1} f==1&&/^version/{print;exit}' pyproject.toml | cut -d '"' -f 2)

# ==============================================================================
#                              Setup & Installation
# ==============================================================================
install: ## Installs project dependencies and sets up the environment with uv.
	@echo "--> Syncing environment with uv.lock..."
	@uv sync --all-extras --dev
	@echo "--> Installing pre-commit hooks..."
	@uv run pre-commit install
	@echo "--> Installation complete."

# ==============================================================================
#                              Code Quality & Testing
# ==============================================================================
lint: ## Runs the ruff linter and formatter (with auto-fix).
	@echo "--> Running Ruff Formatter..."
	@uv run ruff format .
	@echo "--> Running Ruff Linter (with auto-fix)..."
	@uv run ruff check --fix .

check: ## Runs ruff in check-only mode (for CI).
	@echo "--> Checking formatting with Ruff..."
	@uv run ruff format . --check
	@echo "--> Checking linting with Ruff..."
	@uv run ruff check .

test: ## Runs all tests with pytest.
	@echo "--> Running tests with pytest..."
	@uv run pytest tests/

# ==============================================================================
#                              Versioning
# ==============================================================================
version-major: ## Bumps the major version number.
	@echo "--> Bumping MAJOR version..."
	@uv run bump-my-version bump major

version-minor: ## Bumps the minor version number.
	@echo "--> Bumping MINOR version..."
	@uv run bump-my-version bump minor

version-patch: ## Bumps the patch version number.
	@echo "--> Bumping PATCH version..."
	@uv run bump-my-version bump patch

# ==============================================================================
#                       Application & Docker Execution
# ==============================================================================
run: ## Runs the application. Pass args with 'make run args="..."'.
	@echo "--> Running application: $(PACKAGE_NAME)"
	@uv run python -m market_beacon $(args)

docker-build: ## Builds the Docker image with the correct version.
	@echo "--> Building Docker image: $(IMAGE_NAME):latest and $(IMAGE_NAME):$(PROJECT_VERSION)"
	@docker build \
	  --build-arg APP_VERSION=$(PROJECT_VERSION) \
	  -t $(IMAGE_NAME):latest \
	  -t $(IMAGE_NAME):$(PROJECT_VERSION) \
	  .

docker-run: ## Runs the application inside a Docker container.
	@echo "--> Running Docker container: $(IMAGE_NAME)"
	@docker run --rm -it --env-file .env $(IMAGE_NAME):latest

# ==============================================================================
#                              Cleanup
# ==============================================================================
clean: ## Removes virtual environment and cache files.
	@echo "--> Cleaning up..."
	rm -rf .venv/
	rm -rf .ruff_cache/ .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf src/*.egg-info

help: ## Shows this help message.
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
