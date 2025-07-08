# Python Microservice Template

## Overview
This repository serves as a template for creating Python-based microservices. It includes essential configurations and files for code quality, continuous integration, and containerization.

## Features
- Pre-commit hooks for code quality checks
- Continuous Integration (CI) setup with GitHub Actions
- Flake8 for code linting
- Dependabot configuration for dependency management
- Basic Python project structure with a sample module

## Getting Started

### Prerequisites
- Python 3.11
- Docker (for containerization)
- [Additional prerequisites, if applicable]

### Installation
Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```
Install dependencies:

```bash
pip install -r requirements.txt
```
###  Usage

To run the sample Python script:

```bash
python template.py
```
### Running with Docker

Build the Docker image:

```bash
docker build -t [image-name] .
```
Run the Docker container:

```bash
docker run -p 8000:8000 [image-name]
```
## Development
### Code Formatting and Linting

Run pre-commit hooks:

```bash
pre-commit run --all-files
```
Run Flake8 linting:

```bash
flake8 .
```

### Running Tests
(Include instructions on how to run tests, if applicable)

## Continuous Integration
The repository is configured with a CI pipeline using GitHub Actions (`dev_ci.yml`), which automates testing and other checks upon pushing to the repository.

## Versioning

We use `CODE_VERSION.cfg` for semantic versioning. The versioning is handled by using these rules:
- MAJOR version when you make incompatible API changes,
- MINOR version when you add functionality in a backwards compatible manner, and
- PATCH version when you make backwards compatible bug fixes.

To increment the version, run the following commands:

```bash
- make increment-major-version
- make increment-minor-version
- make increment-patch-version
```
