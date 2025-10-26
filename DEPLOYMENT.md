# FlashRecord Deployment Guide

**Version**: v0.3.3
**Last Updated**: 2025-10-26

This guide covers deployment methods for FlashRecord across different environments.

---

## Table of Contents

- [PyPI Installation](#pypi-installation)
- [Docker Deployment](#docker-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Release Process](#release-process)
- [Environment Configuration](#environment-configuration)

---

## PyPI Installation

### End Users

```bash
# Install from PyPI
pip install flashrecord

# Verify installation
flashrecord --version

# Run CLI
flashrecord
```

### Developers

```bash
# Clone repository
git clone https://github.com/Flamehaven/flashrecord.git
cd flashrecord

# Install with poetry
poetry install --with dev

# Run in development mode
poetry run flashrecord
```

---

## Docker Deployment

### Pull from Docker Hub

```bash
# Pull latest image
docker pull flamehaven/flashrecord:latest

# Pull specific version
docker pull flamehaven/flashrecord:0.3.3

# Run container
docker run -it --rm \
  -v $(pwd)/output:/output \
  flamehaven/flashrecord:latest
```

### Build Locally

```bash
# Build image
docker build -t flashrecord:local .

# Run with docker-compose
docker-compose up flashrecord

# Development mode
docker-compose up flashrecord-dev
```

### Docker Run Examples

```bash
# Interactive CLI mode
docker run -it --rm \
  -v $(pwd)/flashrecord-save:/output \
  -e DISPLAY=:99 \
  flamehaven/flashrecord:latest

# Take screenshot
docker run --rm \
  -v $(pwd)/output:/output \
  flamehaven/flashrecord:latest @sc

# Record GIF (10 seconds, 10fps)
docker run --rm \
  -v $(pwd)/output:/output \
  flamehaven/flashrecord:latest @sv 10 10
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

The repository includes a comprehensive CI/CD pipeline (`.github/workflows/ci.yml`):

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Release creation

**Jobs**:

1. **Test** (Matrix: Python 3.8-3.12, Ubuntu/Windows/macOS)
   - Linting with ruff and black
   - Type checking with mypy
   - Unit and integration tests with pytest
   - Coverage reporting to Codecov

2. **Build**
   - Package building with poetry
   - Artifact upload for distribution

3. **Publish to PyPI** (on release)
   - Automatic PyPI publication
   - Requires `PYPI_API_TOKEN` secret

4. **Docker Build & Push** (on release)
   - Multi-arch build (amd64, arm64)
   - Push to Docker Hub
   - Requires `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets

### Required Secrets

Configure in GitHub Settings → Secrets and variables → Actions:

```
PYPI_API_TOKEN          # PyPI API token for publishing
DOCKER_USERNAME         # Docker Hub username
DOCKER_PASSWORD         # Docker Hub password/token
```

---

## Release Process

### 1. Version Bump

Update version in:
- `pyproject.toml` (line 3)
- `flashrecord/__init__.py` (__version__)
- `flashrecord/cli.py` (docstring and help text)

### 2. Update CHANGELOG

```bash
# Add release notes to CHANGELOG.md
## [0.3.3] - 2025-10-26

### Added
- PNG compression support (Phase 1+2)
- CLI flags for compression modes
...
```

### 3. Commit Changes

```bash
git add .
git commit -m "chore: Bump version to v0.3.3"
git push origin main
```

### 4. Create Git Tag

```bash
# Create annotated tag
git tag -a v0.3.3 -m "Release v0.3.3: PNG compression support"

# Push tag
git push origin v0.3.3
```

### 5. Create GitHub Release

1. Go to GitHub repository → Releases
2. Click "Create a new release"
3. Select tag: `v0.3.3`
4. Release title: `v0.3.3 - PNG Compression Support`
5. Description: Copy from CHANGELOG.md
6. Publish release

**This automatically triggers**:
- PyPI publication
- Docker image build and push
- Asset uploads

### 6. Verify Deployment

```bash
# Check PyPI
pip install flashrecord==0.3.3

# Check Docker Hub
docker pull flamehaven/flashrecord:0.3.3
```

---

## Environment Configuration

### Development Environment

```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Run linting
poetry run ruff check flashrecord/
poetry run black flashrecord/

# Run type checking
poetry run mypy flashrecord/

# Build package
poetry build
```

### Production Environment

```bash
# Install from wheel
pip install dist/flashrecord-0.3.3-py3-none-any.whl

# Or from PyPI
pip install flashrecord==0.3.3
```

### Environment Variables

```bash
# Output directory (default: ./flashrecord-save)
export FLASHRECORD_SAVE_DIR=/path/to/output

# Display for X11 (Docker headless mode)
export DISPLAY=:99
```

---

## Testing Before Release

### Run Full Test Suite

```bash
# Unit tests
poetry run pytest tests/unit/ -v

# Integration tests
poetry run pytest tests/integration/ -v

# Coverage report
poetry run pytest --cov=flashrecord --cov-report=html
open htmlcov/index.html
```

### Manual Testing

```bash
# Test screenshot
poetry run flashrecord
> @sc
> @sc -c
> @sc -c high

# Test GIF recording
> @sv
# Follow prompts
```

### Build Verification

```bash
# Build package
poetry build

# Install in clean environment
python -m venv test_env
source test_env/bin/activate
pip install dist/flashrecord-0.3.3-py3-none-any.whl

# Test installation
flashrecord --version
flashrecord --help
```

### Docker Verification

```bash
# Build image
docker build -t flashrecord:test .

# Test run
docker run -it --rm flashrecord:test --version
docker run -it --rm flashrecord:test --help
```

---

## Rollback Procedure

### PyPI Rollback

```bash
# PyPI doesn't support deletion/rollback
# Best practice: Release hotfix version

# Create hotfix
git checkout -b hotfix/v0.3.4
# Fix issue
git commit -m "fix: Critical bug in compression"
git tag v0.3.4
git push origin v0.3.4

# Create new GitHub release → triggers PyPI upload
```

### Docker Rollback

```bash
# Docker Hub supports tag management
# Users can pull previous version
docker pull flamehaven/flashrecord:0.3.2

# Update docker-compose.yml to pin version
services:
  flashrecord:
    image: flamehaven/flashrecord:0.3.2  # Pin to stable version
```

---

## Troubleshooting

### CI/CD Failures

**Test Failures**:
- Check test logs in GitHub Actions
- Run tests locally: `poetry run pytest -v`
- Verify Python version compatibility

**Build Failures**:
- Check pyproject.toml syntax
- Verify poetry.lock is up to date: `poetry lock`

**PyPI Upload Failures**:
- Verify PYPI_API_TOKEN is set correctly
- Check PyPI for version conflicts
- Ensure version is unique

**Docker Build Failures**:
- Check Dockerfile syntax
- Verify base image availability
- Test build locally: `docker build .`

### Installation Issues

**Missing Dependencies**:
```bash
# Linux: Install system dependencies
sudo apt-get install gnome-screenshot scrot imagemagick

# macOS: No additional dependencies
# Windows: No additional dependencies (uses PIL)
```

**Permission Errors**:
```bash
# Use --user flag
pip install --user flashrecord

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install flashrecord
```

---

## Platform-Specific Notes

### Windows

- Screenshot uses PIL ImageGrab (no external dependencies)
- GIF recording works natively
- Docker requires WSL2 or Docker Desktop

### macOS

- Screenshot uses `screencapture` command (built-in)
- GIF recording works natively
- Docker runs via Docker Desktop or Colima

### Linux

- Screenshot requires one of: `gnome-screenshot`, `scrot`, or `imagemagick`
- GIF recording works natively
- Docker runs natively

---

## Security Considerations

### PyPI API Token

```bash
# Create scoped token on PyPI
# Settings → Account settings → API tokens
# Scope: "Entire account" or specific project
# Add as PYPI_API_TOKEN in GitHub Secrets
```

### Docker Hub Credentials

```bash
# Use access token instead of password
# Docker Hub → Account Settings → Security → Access Tokens
# Create token with "Read & Write" permissions
# Add as DOCKER_USERNAME and DOCKER_PASSWORD in GitHub Secrets
```

### Dependency Security

```bash
# Check for vulnerabilities
poetry run pip-audit

# Update dependencies
poetry update

# Lock dependencies
poetry lock
```

---

## Monitoring

### PyPI Download Statistics

- https://pypistats.org/packages/flashrecord
- GitHub Insights → Traffic

### Docker Pull Statistics

- Docker Hub dashboard
- https://hub.docker.com/r/flamehaven/flashrecord/tags

### CI/CD Status

- GitHub Actions → Workflows
- Badge: ![CI/CD](https://github.com/Flamehaven/flashrecord/workflows/CI%2FCD%20Pipeline/badge.svg)

---

## Support

- GitHub Issues: https://github.com/Flamehaven/flashrecord/issues
- Documentation: README.md
- Contributing: CONTRIBUTING.md

---

**Last Updated**: 2025-10-26
**Maintainer**: Flamehaven
