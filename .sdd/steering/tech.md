# Technology Stack

## Architecture

Python-based testing framework using pytest as the core test runner. Client-server architecture with HTTP abstraction layer for API communication. Configuration-driven approach using environment variables.

## Core Technologies

- **Language**: Python 3.x
- **Framework**: Pytest (with pytest-xdist for parallel execution)
- **Runtime**: Python virtual environment (venv)
- **HTTP Client**: Requests library with retry and adapter patterns

## Key Libraries

- **pytest**: Core testing framework with fixtures and markers
- **requests**: HTTP client with session management
- **jsonschema**: Response validation against JSON schemas
- **vcrpy**: Record/replay HTTP interactions for deterministic tests
- **pytest-xdist**: Parallel test execution
- **pytest-sugar**: Enhanced test output formatting
- **python-dotenv**: Environment variable management
- **mypy**: Static type checking

## Development Standards

### Type Safety
- Type hints required for function signatures
- Full type annotations in core modules (`APIClient`, helpers, schemas)
- Mypy static type checking configured via `mypy.ini`

### Code Quality
- Pytest conventions: `test_*.py` files, `test_*` functions, `Test*` classes
- Session-scoped fixtures for expensive resources (HTTP client, base URL)
- VCR cassettes stored in `tests/cassettes/` for recorded interactions
- Test data separated into `tests/data/` directory

### Testing
- Test markers for categorization: `@pytest.mark.smoke`, `@pytest.mark.contract`, `@pytest.mark.pagination`, `@pytest.mark.negative`, `@pytest.mark.heavy`, `@pytest.mark.vcr`
- HTML report generation via pytest-reporter-html1
- Test isolation through pytest fixtures

## Development Environment

### Required Tools
- Python 3.x
- Virtual environment (venv)
- pip for dependency management

### Common Commands
```bash
# Dev: Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install: Install dependencies
pip install -r requirements.txt

# Test: Run all tests
pytest

# Test: Run specific markers
pytest -m smoke

# Test: Generate HTML report
pytest --html=reports/html1-report.html

# Type check: Run mypy
mypy src/
```

## Key Technical Decisions

**HTTP Retry Strategy**: Using `urllib3.Retry` with exponential backoff (0.5s factor) for resilience against transient failures (429, 5xx errors)

**Rate Limiting**: Sleep-based rate limiting (`rate_sleep`) between requests to respect API limits without complex token bucket logic

**Configuration Pattern**: Environment variables with sensible defaults in `config/settings.py` for flexible deployment

**Fixture Scope**: Session-scoped fixtures for APIClient to reuse connection pool across test suite

**Import Pattern**: Absolute imports from `src/` and `config/`, with fixtures re-exported through `tests/conftest.py`

---
_Document standards and patterns, not every dependency_
