# Api Batch Test Framework

A comprehensive testing framework built with Python and Pytest for API testing in huge scale.

## 📋 Project Overview

This project provides a robust framework for testing REST. It follows Python best practices and Pytest conventions.

### Key Features

- **API Testing**: Client abstraction for REST API endpoints (GET, POST, PUT, DELETE)
- **Test Fixtures**: Reusable Pytest fixtures for API client
- **Type Hints**: Full type annotations for better IDE support and code clarity
- **Error Handling**: Comprehensive error handling and logging throughout the framework

## 🏗️ Architecture

### Project Structure

```
API-BATCH-TEST/
├── api-batch-test/
│   ├── config/                   # Configuration files   
│   ├── src/
│   │   ├── helpers/              # Helper functions for tests
│   │   ├── schemas/              # JSON schemas for response validation
│   │   ├── api_client.py         # REST API client abstraction
│   │   └── api_endpoints.py      # API endpoint definitions
│   │
│   ├── tests/
│   │   ├── cassettes/            # VCR.py cassettes for recorded HTTP interactions
│   │   ├── data/                 # Test data files
│   │   ├── test-contract/        # Contract tests
│   │   ├── test-negative/        # Negative tests
│   │   ├── test-pagination/      # Pagination tests
│   │   ├── test-smoke/           # Smoke tests
│   │   └── conftest.py           # Pytest fixtures and configuration
│   │
│   ├── pyproject.toml            # Project metadata and dependencies
│   ├── pyvenv.cfg                # Virtual environment configuration
│   └── requirements.txt          # Python dependencies
│   
├── reports/                      # Test reports
├── mypy.ini                      # Mypy configuration
├── pytest.ini                    # Pytest configuration
└── README.md
```

### Core Components

#### 1. **API Client** (`src/api_client.py`)
Provides a simple abstraction for HTTP operations:
- `APIClient.get()` - Retrieve data
- `APIClient.post()` - Create resources
- `APIClient.put()` - Update resources
- `APIClient.delete()` - Remove resources

Supports URL path parameters and query strings.

#### 2. **Pytest Fixtures** (`tests/conftest.py`)
Reusable test fixtures:
- `__all__ = ["base_url", "http"]` - Expose fixtures for test modules

## 🚀 Installation & Execution

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies**:
- `pytest` - Testing framework
- `requests` - HTTP client library
- `psycopg2-binary` - PostgreSQL adapter for Python
- `mypy` - Static type checker
- `pytest-reporter-html1` - HTML test report generation
- `pytest-xdist` - Parallel test execution
- `pytest-sugar` - Enhanced test output
- `jsonschema` - JSON schema validation
- `python-dotenv` - Environment variable management
- `vcrpy` - HTTP interaction recording

### 2. Run Tests

```bash
# Run all tests
pytest

# Run tests with @pytest.mark (example: smoke)
pytest -m smoke

# Run with verbose output
pytest -v

# Run with print statements visible
pytest -s -v

# Run specific test file
pytest tests/test_smoke/test_sample_smoke.py -v

# Generate HTML report
pytest --html=reports/html1-report.html
```
### Testing API Endpoints

```python
def test_api_available(http, base_url):
    r = http.get(Endpoints.PEOPLE)
    assert r.status_code == 200
    assert r.headers.get("Content-Type", "").startswith("application/json")
```

## 🔒 Best Practices

- **Fixtures**: Leverage Pytest fixtures for setup and teardown
- **Type Hints**: Use type annotations for better code documentation
- **Error Handling**: Catch and log errors appropriately
- **Test Isolation**: Each test should be independent and repeatable
- **Async Support**: For I/O-bound tests, consider using `pytest-asyncio`

## 📚 Dependencies

See `requirements.txt` for the complete list. Key dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | Latest | Testing framework |
| requests | Latest | HTTP client |
| psycopg2-binary | Latest | PostgreSQL adapter |
| mypy | Latest | Type checking |
| pytest-reporter-html1 | Latest | HTML reports |
| pytest-xdist | Latest | Parallel test execution |
| pytest-sugar | Latest | Enhanced output |
| jsonschema | Latest | JSON schema validation |
| python-dotenv | Latest | Environment variables |

## 🛠️ Troubleshooting

### Import Errors
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Test Failures
- Use `-v` flag for verbose output
- Use `-s` flag to see print statements

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

AlexAlexandreAlves

---

**Happy Testing! 🧪**