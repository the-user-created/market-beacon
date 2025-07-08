# Market Beacon

A Python bot to retrieve and analyze trade data from the Bitget cryptocurrency exchange.

## Features

- **Modern Tooling**: Uses `Ruff` for extremely fast linting, formatting, and import sorting.
- **Robust Packaging**: Managed with `pyproject.toml` and `setuptools` following PEP 621.
- **Automated Quality Checks**: Pre-commit hooks for automated code quality enforcement.
- **Continuous Integration**: GitHub Actions workflow for automated testing and linting on every push.
- **Containerized**: Multi-stage `Dockerfile` for lean, secure, and reproducible production images.
- **Developer-Friendly**: `Makefile` for easy access to common commands like installation, testing, and running.

## Getting Started

### Prerequisites

- Python 3.12
- Docker (for containerization)
- `make` (for using the Makefile commands)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/the-user-created/market-beacon.git
   cd market-beacon
   ```

2. **Create virtual environment and install dependencies:**
   This command will create a local virtual environment (`.market-beacon-venv/`) and install all required main and
   development packages.
   ```bash
   make install
   ```

3. **Activate the virtual environment:**
   ```bash
   source .market-beacon-venv/bin/activate
   ```

### Usage

To run the application locally:

```bash
make run
```

You can also pass arguments to the application:

```bash
make run args="--symbol BTCUSDT"
```

## Development

This project uses a suite of tools to ensure code quality and consistency.

### Code Formatting and Linting

`Ruff` is used for linting and formatting. The `Makefile` provides a simple command to apply formatting and fix lint
errors automatically.

```bash
make lint
```

To just check for issues without applying changes (as is done in CI):

```bash
make check
```

The pre-commit hooks will run these checks automatically every time you commit.

### Running Tests

Tests are managed with `pytest`. To run the full test suite:

```bash
make test
```

This will run all files matching `tests/test_*.py`.

### Versioning

The project version is managed in `CODE_VERSION.cfg` and `pyproject.toml`. Use the `Makefile` to increment the version
number according to semantic versioning. These commands will create a new git commit and tag.

```bash
make version-patch  # For bug fixes (0.0.1 -> 0.0.2)
make version-minor  # For new features (0.1.0 -> 0.2.0)
make version-major  # For breaking changes (1.0.0 -> 2.0.0)
```

## Running with Docker

The project includes a multi-stage `Dockerfile` for building optimized production images.

1. **Build the Docker image:**
   ```bash
   make docker-build
   ```
   *This is equivalent to `docker build -t market-beacon:latest .`*

2. **Run the Docker container:**
   ```bash
   make docker-run
   ```
   *This is equivalent to `docker run --rm -it market-beacon:latest`*

You can also run tests or other commands inside the container:

```bash
docker run --rm -it market-beacon:latest test
docker run --rm -it market-beacon:latest bash
```

## Continuous Integration

The CI pipeline is defined in `.github/workflows/dev_ci.yml`. It automatically runs `make check` and `make test` on all
pushes and pull requests to the `main` branch, ensuring that code merged into the main branch meets quality standards.
