# Market Beacon - Bitget Trade Analyzer

<p align="center">
  <a href="https://github.com/the-user-created/market-beacon/actions/workflows/ci.yml">
    <img alt="CI Pipeline" src="https://img.shields.io/github/actions/workflow/status/the-user-created/market-beacon/ci.yml?branch=main&logo=githubactions&logoColor=white">
  </a>
  <a href="https://www.python.org/downloads/release/python-3120/">
    <img alt="Python Version" src="https://img.shields.io/badge/python-3.12-blue.svg?logo=python&logoColor=white">
  </a>
  <a href="https://pre-commit.com/">
    <img alt="pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white">
  </a>
<br>
  <a href="https://conventionalcommits.org">
    <img alt="Conventional Commits" src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img alt="Code style: ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json">
  </a>
  <a href="https://github.com/the-user-created/market-beacon/blob/main/Dockerfile">
    <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white">
  </a>
</p>

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
  Docker, `pre-commit` for quality control, and `uv` for
  high-performance dependency management.
- **Automated CI/CD & Releases**: Fully automated pipeline for testing, quality checks, and versioned releases with
  auto-generated changelogs.

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
- [uv](https://github.com/astral-sh/uv) (Python package manager)
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

   Simply run the `install` command from the Makefile. This uses `uv` to
   create a virtual environment in `./.venv`, install all dependencies
   from `uv.lock`, and set up the pre-commit hooks.

   ```sh
   make install
   ```

   Your environment is now ready! If you aren't using the `make` commands
   for subsequent actions, remember to activate the virtual environment:

   ```sh
   # Activate on macOS/Linux
   source .venv/bin/activate
   # Activate on Windows
   .\.venv\Scripts\activate
   ```

## 🤖 Usage

You can run the application directly through the `Makefile` or via `uv run`.

**Using Make (Recommended):**

```sh
# Run with the default symbol (BTCUSDT)
make run

# Run with a custom symbol
make run args="--symbol ETHUSDT"
```

**Using uv:**

```sh
# Ensure the virtual environment is activated
source .venv/bin/activate

# Run with a custom symbol
uv run python -m market_beacon --symbol BTCUSDT
```

## 🧰 Development & Automation

This project uses a combination of `make`, `pre-commit`, and GitHub Actions to automate development, testing, and
release workflows.

### Makefile Commands

This project includes a `Makefile` to streamline common development tasks. Run `make help` to see a full list of
commands with their descriptions.

- `make install`: Sets up the complete development environment using `uv`.
- `make lint`: Formats code and lints for errors, applying automatic fixes.
- `make check`: Runs the formatter and linter in check-only mode (ideal for CI).
- `make test`: Executes the test suite using `pytest`.
- `make run`: Runs the main application. Pass arguments like so: `make run args="--symbol ETHUSDT"`.
- `make version-[major|minor|patch]`: Bumps the project version using `bump-my-version` and creates a Git tag.
- `make docker-build`: Builds the production Docker image.
- `make docker-run`: Runs the application inside a Docker container.
- `make clean`: Removes the virtual environment and all cache files.

### Automation & Release Workflow

- **PR Validation**: Every pull request title is automatically checked to ensure it follows
  the [Conventional Commits](https://www.conventionalcommits.org) specification.
- **Automated Labeling**: Pull requests are automatically labeled based on their conventional commit type (e.g., `feat`,
  `fix`, `chore`).
- **Automated Release Drafting**: When changes are merged to `main`, a draft release is automatically updated with a
  categorized changelog.
- **Automated Publishing**: Pushing a new version tag (e.g., `v1.0.0`) triggers a workflow that publishes the final
  release notes and builds/pushes a versioned Docker image to the GitHub Container Registry.

## 🛠️ Tooling Stack

This project is built with a focus on modern development practices and automation.

| Tool                                                                      | Purpose                                                                    |
|---------------------------------------------------------------------------|----------------------------------------------------------------------------|
| [**uv**](https://github.com/astral-sh/uv) & `pyproject.toml`              | High-performance dependency and project management.                        |
| [**Ruff**](https://github.com/astral-sh/ruff)                             | High-performance linting, formatting, and import sorting.                  |
| [**pytest**](https://docs.pytest.org/)                                    | A powerful framework for writing and running automated tests.              |
| [**pre-commit**](https://pre-commit.com/)                                 | Manages and maintains multi-language pre-commit hooks for quality control. |
| [**bump-my-version**](https://github.com/callowayproject/bump-my-version) | A tool for version string management and automated bumping.                |
| [**Release Drafter**](https://github.com/release-drafter/release-drafter) | Automatically generates release notes and changelogs from PRs.             |
| [**Gitleaks**](https://github.com/gitleaks/gitleaks)                      | Scans git history for secrets and sensitive data.                          |
| [**GitHub Actions**](https://github.com/features/actions)                 | Continuous Integration (CI) and automated release deployment (CD).         |
| [**Docker**](https://www.docker.com/)                                     | Containerization for consistent development and deployment environments.   |
| [**Makefile**](https://www.gnu.org/software/make/manual/make.html)        | A simple command runner for automating common development tasks.           |

## ❤️ Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

This project follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

### Reporting Issues

If you encounter a bug or have a feature request, please use the appropriate issue template.

- **[🐛 Bug Report](https://github.com/the-user-created/market-beacon/issues/new?template=bug_report.yml)**: For
  reporting something that's broken or not working as expected.
- **[✨ Feature Request](https://github.com/the-user-created/market-beacon/issues/new?template=feature_request.yml)**:
  For suggesting a new feature or enhancement.
- For questions, please start a [discussion](https://github.com/the-user-created/market-beacon/discussions).

### Development Workflow

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally: `git clone https://github.com/YOUR-USERNAME/market-beacon.git`
3. **Set up the environment**: Run `make install` to install dependencies and pre-commit hooks.
4. **Create a new branch**: `git checkout -b feat/your-awesome-feature`
5. **Make your changes**. Remember to add tests for any new functionality.
6. **Verify your changes**: Run `make check` and `make test` to ensure everything is working correctly.
7. **Commit your changes**: `git commit -m "feat: Add some amazing feature"`.
8. **Push to your branch**: `git push origin feat/your-awesome-feature`
9. **Open a Pull Request**: Go to the original repository and open a pull request. The title of your PR **must** also
   follow the Conventional Commits specification for the release automation to work correctly.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
