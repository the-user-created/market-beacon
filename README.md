# Market Beacon - Bitget Trade Analyzer

[![CI/CD Pipeline](https://img.shields.io/github/actions/workflow/status/the-user-created/market-beacon/dev_ci.yml?branch=main&style=flat-square&logo=githubactions&logoColor=white)](https://github.com/the-user-created/market-beacon/actions/workflows/dev_ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.12-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3120/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Gitleaks](https://img.shields.io/badge/protected%20by-gitleaks-blue?style=flat-square)](https://github.com/gitleaks/gitleaks)
[![License: MIT](https://img.shields.io/github/license/the-user-created/market-beacon?style=flat-square)](https://opensource.org/licenses/MIT)

Market Beacon is a Python-based tool designed to connect to the Bitget
cryptocurrency exchange via its API. It retrieves real-time and
historical trade data for specified cryptocurrency pairs, calculates key
trading statistics and metrics, and provides valuable market insights.

## ✨ Key Features

- **Secure API Integration**: Safely connects to the Bitget API using
  best practices for key management via environment variables.
- **Trade Data Retrieval**: Fetches recent trade history for any specified
  trading symbol (e.g., `BTCUSDT`).
- **Statistical Analysis (Planned)**: Will calculate metrics like Volume
  Weighted Average Price (VWAP), moving averages, and trade frequency.
- **Modern Tooling**: Built with a professional-grade stack including
  Docker, `pre-commit` for quality control, and `ruff` for
  high-performance linting and formatting.
- **CI/CD Ready**: Integrated with GitHub Actions for continuous
  integration and testing.

## 🚀 Project Status

This project is currently in the initial development phase. The core
structure, configuration, and CI/CD pipeline are established. The next
steps involve implementing the API client logic, data processing, and
statistical calculations.

## 🏁 Getting Started

Follow these steps to get your local development environment set up.

### Prerequisites

- [Git](https://git-scm.com/)
- [Python 3.12](https://www.python.org/downloads/release/python-3120/)
- [Docker](https://www.docker.com/) (Optional, for containerized execution)
- [Make](https://www.gnu.org/software/make/)

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/the-user-created/market-beacon.git
   cd market-beacon
   ```

2. **Configure API Credentials:**

   The application requires API credentials to connect to Bitget. Create a
   `.env` file from the example and add your keys.

   ```sh
   cp .env.example .env
   ```

3. **Install the Project:**

   Simply run the `install` command from the Makefile. This will create a
   virtual environment in `./.market-beacon-venv`, install all
   dependencies, and set up the pre-commit hooks.

   ```sh
   make install
   ```

   Your environment is now ready! If you aren't using the `make` commands
   for subsequent actions, remember to activate the virtual environment:

   ```sh
   # Activate on macOS/Linux
   source .market-beacon-venv/bin/activate
   # Activate on Windows
   .\.market-beacon-venv\Scripts\activate
   ```

## 🤖 Usage

You can run the application directly through the `Makefile` or via Python's
module execution flag.

**Using Make (Recommended):**

```sh
# Run with the default symbol (BTCUSDT)
make run

# Run with a custom symbol
make run args="--symbol ETHUSDT"
```

**Using Python:**

```sh
# Ensure the virtual environment is activated
source .market-beacon-venv/bin/activate

# Run with a custom symbol
python -m market_beacon --symbol BTCUSDT
```

## 🧰 Development & Tooling

### Makefile Commands

This project includes a `Makefile` to streamline common development tasks.
Run `make help` to see a full list of commands with their descriptions.

- `make install`: Sets up the complete development environment.
- `make lint`: Formats code and lints for errors, applying automatic
  fixes.
- `make check`: Runs the formatter and linter in check-only mode (ideal
  for CI).
- `make test`: Executes the test suite using `pytest`.
- `make run`: Runs the main application. Pass arguments like so:
  `make run args="--symbol ETHUSDT"`.
- `make version-[major|minor|patch]`: Bumps the project version using
  `bump-my-version`.
- `make docker-build`: Builds the production Docker image.
- `make docker-run`: Runs the application inside a Docker container.
- `make clean`: Removes the virtual environment and all cache files.

### Code Quality Workflow

We use a suite of tools to maintain high code quality, all of which are
managed by `pre-commit` and can be run via the `Makefile`.

- **Linting and Formatting with Ruff:** `ruff` is used for both formatting
  and linting. The `make lint` command will automatically fix most issues.
- **Spell Checking with Codespell:** `codespell` runs automatically on
  commit to catch common misspellings in code and documentation.
- **Secret Scanning with Gitleaks:** The CI pipeline includes a step to
  run `gitleaks`, which scans for any accidentally committed secrets.

## 🛠️ Tooling Stack

This project is built with a focus on modern development practices and
automation.

| Tool                                                                      | Purpose                                                                    |
|---------------------------------------------------------------------------|----------------------------------------------------------------------------|
| [**pip**](https://pip.pypa.io/en/stable/) & `pyproject.toml`              | Dependency and project management (PEP 621).                               |
| [**Ruff**](https://github.com/astral-sh/ruff)                             | High-performance linting, formatting, and import sorting.                  |
| [**pytest**](https://docs.pytest.org/)                                    | A powerful framework for writing and running automated tests.              |
| [**pre-commit**](https://pre-commit.com/)                                 | A framework for managing and maintaining multi-language pre-commit hooks.  |
| [**bump-my-version**](https://github.com/callowayproject/bump-my-version) | A tool for version string management and automated bumping.                |
| [**codespell**](https://github.com/codespell-project/codespell)           | Automated spell checking for source code and documentation.                |
| [**gitleaks**](https://github.com/gitleaks/gitleaks)                      | Scans git history for secrets and sensitive data.                          |
| [**GitHub Actions**](https://github.com/features/actions)                 | Continuous Integration (CI) to run tests and quality checks on every push. |
| [**Docker**](https://www.docker.com/)                                     | Containerization for consistent development and deployment environments.   |
| [**Makefile**](https://www.gnu.org/software/make/manual/make.html)        | A simple command runner for automating common development tasks.           |

## ❤️ Contributing

Contributions are welcome! If you'd like to contribute, please follow
these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them with a descriptive message.
4. Push to your branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.

Please also feel free to open an issue for any bugs or feature requests.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE)
file for details.
