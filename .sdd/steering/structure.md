# Project Structure

## Organization Philosophy

Test-category-first organization: tests grouped by type (smoke, contract, pagination, negative) for clear test intent and selective execution. Core API abstractions separated from test code, with supporting modules (helpers, schemas, data) under their respective parent directories.

## Directory Patterns

### Source Code (`/src/`)
**Location**: `/src/`
**Purpose**: Core API client, endpoint definitions, helpers, and schemas
**Example**:
- `api_client.py` - HTTP client with retry/rate limiting
- `api_endpoints.py` - Centralized endpoint constants
- `helpers/` - Test utilities (pagination, etc.)
- `schemas/` - JSON schema definitions for validation

### Test Suites (`/tests/`)
**Location**: `/tests/`
**Purpose**: Test files organized by category with pytest markers
**Example**:
- `test-smoke/` - Quick availability tests (`@pytest.mark.smoke`)
- `test-contract/` - Schema validation tests (`@pytest.mark.contract`)
- `test-pagination/` - Pagination tests (`@pytest.mark.pagination`)
- `test-negative/` - Error/edge case tests (`@pytest.mark.negative`)

### Test Support Files
**Location**: `/tests/cassettes/`, `/tests/data/`
**Purpose**: VCR recordings and test data files
**Example**:
- `cassettes/` - Recorded HTTP interactions for deterministic tests
- `data/` - Static test data (activities, fixtures, etc.)

### Configuration (`/config/`)
**Location**: `/config/`
**Purpose**: Environment-based settings management
**Example**: `settings.py` - Loads BASE_URL, timeouts, retry config from env vars

### Reports (`/reports/`)
**Location**: `/reports/`
**Purpose**: Generated test reports (HTML, etc.)
**Example**: `html1-report.html` - pytest HTML report output

## Naming Conventions

- **Files**: snake_case for all Python files (`api_client.py`, `test_smoke.py`)
- **Classes**: PascalCase (`APIClient`, `Endpoints`)
- **Functions**: snake_case (`test_api_available`, `_build_url`)
- **Test files**: `test_*.py` prefix required by pytest
- **Test directories**: kebab-case with `test-` prefix (`test-smoke/`, `test-contract/`)

## Import Organization

```python
# Standard library imports first
import os
import time
from typing import Dict, Generator

# Third-party imports
import pytest
import requests
from dotenv import load_dotenv

# Local imports - absolute from root
from config import settings
from src.api_client import APIClient, http
from src.api_endpoints import Endpoints
```

**Path Resolution**:
- No path aliases configured
- Use absolute imports from project root (`src/`, `config/`, `tests/`)
- Relative imports only within same module (e.g., `tests/conftest.py` importing from `src.api_client`)

## Code Organization Principles

**Fixture Re-export Pattern**: Core fixtures defined in `src/api_client.py` and re-exported through `tests/conftest.py` for test access

**Session Scope for Expensive Resources**: APIClient fixture uses `scope="session"` to reuse connection pool

**Centralized Endpoints**: All API paths in `src/api_endpoints.py` as class constants for maintainability

**Test Categorization**: Pytest markers (`smoke`, `contract`, `pagination`, `negative`, `heavy`, `vcr`) enable selective test execution

**Separation of Concerns**:
- `/src/` - Framework code (no test logic)
- `/tests/` - Test logic only (no production code)
- `/config/` - Environment config (no business logic)

---
_Document patterns, not file trees. New files following patterns shouldn't require updates_
