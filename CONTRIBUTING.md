# Contributing to SpatialAIFlow

Thank you for your interest in contributing to **SpatialAIFlow**! This document
explains how to get involved, from reporting bugs to submitting pull requests.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Submitting Changes](#submitting-changes)
6. [Release Process](#release-process)

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you agree to uphold its standards of respectful and inclusive
collaboration.

---

## How Can I Contribute?

### Reporting Bugs

- Search [existing issues](../../issues) to avoid duplicates.
- Use the **Bug Report** template when opening a new issue.
- Include: Python version, OS, package versions (`pip freeze`), and a minimal
  reproducible example.

### Suggesting Features

- Use the **Feature Request** template.
- Describe the biological or computational motivation for the feature.

### Improving Documentation

- Typo fixes, docstring improvements, and tutorial contributions are always
  welcome.

### Contributing Code

- See [Submitting Changes](#submitting-changes) below.

---

## Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/<your-username>/SpatialAIFlow.git
cd SpatialAIFlow

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install in editable mode with development dependencies
pip install -e ".[dev]"

# 4. Install pre-commit hooks
pre-commit install
```

---

## Coding Standards

| Area | Tool | Config |
|---|---|---|
| Linting & formatting | [Ruff](https://docs.astral.sh/ruff/) | `pyproject.toml` |
| Type checking | [mypy](https://mypy.readthedocs.io/) | `pyproject.toml` |
| Testing | [pytest](https://docs.pytest.org/) | `pyproject.toml` |
| Docstrings | [numpydoc](https://numpydoc.readthedocs.io/) | — |

**Key rules:**

- Follow [PEP 8](https://peps.python.org/pep-0008/) via Ruff.
- Use type hints for all public function signatures.
- Write NumPy-style docstrings for all public functions and classes.
- Aim for >80% test coverage on new code.

---

## Submitting Changes

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```
2. **Make your changes** in small, focused commits.
3. **Run quality checks**:
   ```bash
   make lint    # ruff check + ruff format --check
   make test    # pytest
   ```
4. **Push and open a Pull Request** against `main`.
5. Fill in the PR template checklist.
6. Wait for CI to pass and a maintainer review.

---

## Release Process

Releases follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking API changes
- **MINOR**: New features, backward-compatible
- **PATCH**: Bug fixes, backward-compatible

The [CHANGELOG](CHANGELOG.md) is updated with each release following the
[Keep a Changelog](https://keepachangelog.com/) format.

---

*Thank you for helping make spatial transcriptomics analysis more accessible!*
