# Contributing to FlashRecord

Thank you for your interest in contributing to FlashRecord! This guide will help you get started.

## Table of Contents

- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Code Style](#code-style)
- [Testing Your Changes](#testing-your-changes)
- [Submitting a PR](#submitting-a-pr)
- [Project Architecture](#project-architecture)

---

## Development Setup

### Prerequisites

- Python 3.8+
- Poetry (for dependency management)
- Git

### Local Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/flashrecord.git
   cd flashrecord
   ```

2. **Install Poetry** (if not already installed)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Activate virtual environment**
   ```bash
   poetry shell
   ```

### Verify Installation

```bash
# Run tests to verify setup
pytest tests/ -v

# Check code style
ruff check flashrecord/
```

---

## Running Tests

### Run All Tests

```bash
poetry run pytest tests/ -v
```

### Run Specific Test File

```bash
poetry run pytest tests/test_cli.py -v
```

### Run with Coverage

```bash
poetry run pytest tests/ --cov=flashrecord --cov-report=term-missing
```

### Expected Output

```
====== 38 passed in 0.18s ======
```

All tests must pass before submitting a PR.

---

## Code Style

### Linting with Ruff

Check for style issues:

```bash
poetry run ruff check flashrecord/
```

Fix automatically (where possible):

```bash
poetry run ruff check flashrecord/ --fix
```

### Guidelines

- **Line Length**: Max 100 characters
- **Naming**:
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
- **Imports**: Group as stdlib, third-party, local (alphabetical within groups)
- **Docstrings**: One-line for simple functions, multi-line for complex ones

### Example

```python
"""
Module docstring - one line summary
"""

from typing import Optional

from pydantic import BaseModel


class ConfigManager(BaseModel):
    """Configuration management with validation"""

    name: str
    value: Optional[int] = None

    def load(self) -> dict:
        """Load configuration and return as dict"""
        return {"name": self.name, "value": self.value}
```

---

## Testing Your Changes

### Before You Start

1. Create a new branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests locally
   ```bash
   poetry run pytest tests/ -v --cov=flashrecord
   ```

### Adding New Tests

When adding new functionality, include tests:

```python
# tests/test_your_feature.py

import pytest
from flashrecord.your_module import YourClass


def test_basic_functionality():
    """Test basic functionality"""
    obj = YourClass()
    assert obj.method() is not None


def test_error_handling():
    """Test error handling"""
    obj = YourClass()
    with pytest.raises(ValueError):
        obj.method(invalid_input)
```

### Minimum Coverage

- New code should have **at least 80% test coverage**
- Critical paths should have **100% coverage**

---

## Submitting a PR

### Before Submitting

1. **Run full test suite**
   ```bash
   poetry run pytest tests/ -v --cov=flashrecord --cov-report=html
   ```

2. **Check code style**
   ```bash
   poetry run ruff check flashrecord/
   ```

3. **Update documentation**
   - Update README.md if user-facing changes
   - Update docstrings if API changes
   - Update CHANGELOG.md

### PR Title Format

```
[AREA] Brief description

Examples:
[CLI] Add new command style 'compact'
[CONFIG] Implement Pydantic validation
[API] Add new /recording/gif endpoint
[DOCS] Update README with API examples
[TEST] Improve coverage for manager.py
```

### PR Description Template

```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Coverage maintained (>80%)

## Checklist
- [ ] Code follows style guidelines
- [ ] Docstrings updated
- [ ] README updated (if user-facing)
- [ ] No breaking changes (or documented)
```

---

## Project Architecture

### Directory Structure

```
flashrecord/
├── flashrecord/          # Main package
│   ├── __init__.py       # Package init
│   ├── cli.py            # CLI interface
│   ├── api.py            # REST API (FastAPI)
│   ├── config.py         # Configuration (Pydantic)
│   ├── screenshot.py     # Screenshot capture
│   ├── video_recorder.py # Video recording
│   ├── ai_prompt.py      # AI session saving
│   ├── manager.py        # File management
│   ├── utils.py          # Utilities
│   └── install.py        # Setup wizard
├── tests/                # Test suite
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_screenshot.py
│   ├── test_video_recorder.py
│   ├── test_manager.py
│   ├── test_utils.py
│   └── test_ai_prompt.py
├── flashrecord-save/     # User data (auto-created)
├── .github/workflows/    # CI/CD
├── pyproject.toml        # Poetry config
├── README.md             # User guide
├── CONTRIBUTING.md       # This file
└── LICENSE               # MIT License
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| **cli.py** | User input processing and command routing |
| **api.py** | REST API endpoints for programmatic access |
| **config.py** | Configuration loading and validation (Pydantic) |
| **screenshot.py** | Screen capture integration with hcap |
| **video_recorder.py** | Terminal recording and GIF conversion |
| **ai_prompt.py** | Session markdown file management |
| **manager.py** | File lifecycle and cleanup |
| **utils.py** | Timestamp and formatting utilities |
| **install.py** | First-time setup wizard |

### Data Flow

```
User Input (CLI/API)
    ↓
Command Router (cli.py or api.py)
    ↓
Action Handler (screenshot/video_recorder/ai_prompt)
    ↓
File Manager (manager.py)
    ↓
Output (flashrecord-save/)
```

### Configuration Flow

```
config.json
    ↓
Config class (Pydantic validation)
    ↓
FlashRecordConfig (type-safe model)
    ↓
Available in CLI/API
```

---

## Development Tips

### Using the API for Testing

Start the API server:

```bash
poetry run python -m flashrecord.api
```

Visit `http://localhost:8000/docs` for interactive API documentation.

### Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Tasks

**Add a new command style:**
1. Update `FlashRecordConfig.command_style` Literal in `config.py`
2. Add mapping in `cli.py:map_command()`
3. Add tests in `test_cli.py`
4. Update README.md

**Add a new API endpoint:**
1. Create endpoint function in `api.py`
2. Use Pydantic models for request/response
3. Add tests (or use `/docs` to test manually)
4. Document in README.md

**Improve performance:**
1. Profile with `cProfile` or `py-spy`
2. Write benchmarks
3. Submit with measurements

---

## Code Review Process

All PRs require:

1. ✅ All tests pass
2. ✅ Code coverage > 80%
3. ✅ Ruff check passes
4. ✅ Documentation updated
5. ✅ At least one approval

---

## Questions or Issues?

- Open an issue on GitHub
- Check existing issues first
- Include error messages and reproduction steps

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to FlashRecord!**

---

## Additional Resources

- **DEPLOYMENT.md**: Detailed deployment and release instructions
- **README.md**: User-facing documentation
- **.DEVELOPMENT_ROADMAP.md**: Future development plans (contributors only)

For questions, open an issue or discussion on GitHub.
