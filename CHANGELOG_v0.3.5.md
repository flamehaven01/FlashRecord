# FlashRecord v0.3.5 Release Notes

**Release Date:** 2025-10-27
**Focus:** Docker Build Fix & PyPI Deployment

## 🎯 Overview

v0.3.5 is a patch release that fixes critical Dockerfile issues preventing Docker image builds and enables automated PyPI deployment.

## 🐛 Bug Fixes

### Docker Image Build (Critical Fix)
- **Fixed COPY path**: `flashrecord` → `src/flashrecord`
  - Dockerfile was trying to copy from wrong directory
  - Caused "no such file or directory" error in CI/CD
  - Now correctly copies from `src/flashrecord` where code actually lives

- **Updated version label**: `0.3.3` → `0.3.4` → `0.3.5`
  - Ensures Docker image metadata matches release version

### PyPI Deployment
- **Configured GitHub Secret**: `PYPI_API_TOKEN`
  - Enables automated PyPI publishing on release
  - Token securely stored in GitHub repository secrets
  - Will auto-deploy on future releases

## 📦 Deployment Status

### Docker Hub
- **Image**: `flamehaven/flashrecord:0.3.5`
- **Tags**: `0.3.5`, `0.3`, `latest`
- **Platforms**: `linux/amd64`, `linux/arm64`
- **Status**: Building in CI/CD

### PyPI
- **Package**: `flashrecord`
- **Version**: `0.3.5`
- **Status**: Publishing in CI/CD

## 🔄 Upgrade Instructions

### From PyPI
```bash
pip install --upgrade flashrecord
```

### From Docker
```bash
docker pull flamehaven/flashrecord:latest
docker run --rm -v $(pwd)/output:/output flamehaven/flashrecord:latest --help
```

## 🎓 Breaking Changes

**None.** This is a fully backward-compatible patch release.

## 📊 Quality Metrics

- **GitHub Stars**: 40+ ⭐
- **CI/CD Pass Rate**: 100% (15/15 jobs)
- **Test Coverage**: 61+ tests
- **Python Support**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Platform Support**: Windows, macOS, Linux
- **Code Quality**: Linting ✅ | Type Checking ✅

## 🔗 Links

- **GitHub Release**: https://github.com/Flamehaven/FlashRecord/releases/tag/v0.3.5
- **PyPI Package**: https://pypi.org/project/flashrecord/
- **Docker Hub**: https://hub.docker.com/r/flamehaven/flashrecord
- **Documentation**: https://github.com/Flamehaven/FlashRecord#readme

---

**Full Changelog**: https://github.com/Flamehaven/FlashRecord/compare/v0.3.4...v0.3.5
