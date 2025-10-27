# PyPI Deployment Guide

## Prerequisites

1. **Install build tools:**
```bash
pip install build twine
```

2. **Get PyPI API token:**
   - Create account at https://pypi.org/account/register/
   - Go to Account Settings → API tokens
   - Create token for "FlashRecord" project

3. **Configure credentials:**
```bash
# Copy template
cp .pypirc.template ~/.pypirc

# Edit with your token
nano ~/.pypirc
```

## Build Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distribution packages
python -m build
```

This creates:
- `dist/flashrecord-0.3.4-py3-none-any.whl` (wheel)
- `dist/flashrecord-0.3.4.tar.gz` (source)

## Test on TestPyPI (Optional)

```bash
# Upload to test PyPI
python -m twine upload --repository testpypi dist/*

# Test install
pip install -i https://test.pypi.org/simple/ flashrecord
```

## Deploy to PyPI

```bash
# Upload to production PyPI
python -m twine upload dist/*

# Verify
pip install flashrecord
```

## Post-Deployment

1. **Test installation:**
```bash
pip install flashrecord
flashrecord --help
```

2. **Create GitHub release:**
```bash
gh release create v0.3.4 \
    --title "FlashRecord v0.3.4 - Production Quality" \
    --notes "See CHANGELOG.md for details" \
    dist/*
```

## Troubleshooting

**Build fails:**
- Ensure pyproject.toml is valid
- Check all dependencies are declared

**Upload fails:**
- Verify API token in ~/.pypirc
- Check version number is incremented
- Ensure no existing version on PyPI

**Import fails after install:**
- Check package structure: `flashrecord` module in `src/flashrecord/`
- Verify __init__.py exports
