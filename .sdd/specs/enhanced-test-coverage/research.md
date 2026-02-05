# Research & Design Decisions: Enhanced Test Coverage

## Summary
- **Feature**: `enhanced-test-coverage`
- **Discovery Scope**: Extension (existing test framework with new tests and infrastructure)
- **Key Findings**:
  - SWAPI provides 6 resource types (people, films, starships, vehicles, species, planets), all with paginated collection endpoints and individual resource endpoints
  - `responses` library is optimal for mocking HTTP behavior including retry, timeout, and rate limiting scenarios
  - pytest-xdist parallel execution requires careful handling of session-scoped fixtures and VCR cassettes

## Research Log

### API Endpoint Discovery
- **Context**: Need to identify all SWAPI endpoints for comprehensive smoke and contract test coverage (Requirements 1 & 2)
- **Sources Consulted**: https://swapi.dev/documentation
- **Findings**:
  - **6 Resource Types**: people, films, starships, vehicles, species, planets
  - **Endpoint Pattern**: Each resource has:
    - Collection endpoint: `GET /{resource}/` (paginated)
    - Individual endpoint: `GET /{resource}/{id}/`
    - Schema endpoint: `GET /{resource}/schema/` (provides JSON schema)
  - **HTTP Methods**: GET only (read-only API)
  - **Authentication**: None (public API)
  - **Rate Limiting**: 10,000 requests/day per IP
  - **Search Support**: All resources support `?search=` parameter with case-insensitive partial matching
  - **Pagination**: All collection endpoints paginated with same structure as existing people endpoint
- **Implications**:
  - Need 5 additional schema files (films, starships, vehicles, species, planets)
  - Smoke tests expand from 1 to 6 resource endpoints
  - Contract tests expand to cover all 6 resources
  - Pagination tests can be generalized across all collection endpoints
  - No authentication testing possible (401 tests must be mocked)
  - Rate limiting tests must verify RATE_LIMIT_SLEEP effectiveness

### Mocking Library Selection
- **Context**: Requirements 3 & 5 need mocking for resilience testing (retry, timeout, 429, 5xx responses)
- **Sources Consulted**: https://github.com/getsentry/responses, gap analysis recommendations
- **Findings**:
  - **responses library** provides:
    - Decorator-based activation (`@responses.activate`)
    - Context manager support for pytest fixtures
    - Multiple response registration for same endpoint (enables retry testing)
    - Request matchers for JSON, query params, headers, timeout validation
    - No conflicts with VCR.py (can coexist)
  - **Alternative**: requests-mock (similar features, slightly different API)
  - **pytest-mock**: Lower-level, requires more setup, better for unit testing internals
- **Implications**:
  - Add `responses` to requirements.txt
  - Create `tests/mocks/` directory for mock response definitions
  - Use `responses.add()` to register multiple responses for retry testing
  - Use `responses.matchers.request_kwargs_matcher()` to validate timeout parameters
  - Session-scoped APIClient fixture compatible (responses activates per test/context)

### Pagination Testing Strategy
- **Context**: Requirement 4 needs boundary condition testing and multi-endpoint validation
- **Sources Consulted**: Existing `iter_pages()` helper, gap analysis
- **Findings**:
  - Current `iter_pages()` works for all paginated endpoints (accepts any starting path)
  - Boundary conditions to test: page=0, page=-1, page=999999, invalid page parameter
  - Skipped test indicates API pagination structure may have changed
  - Need to verify `previous` link traversal (current tests only check `next`)
- **Implications**:
  - No changes needed to `iter_pages()` helper
  - Add parametrized tests for boundary conditions
  - Create pagination validator helper to verify duplicate detection and count consistency
  - Test both `next` and `previous` link traversal
  - Consider making pagination tests more resilient to API structure changes

### VCR and Parallel Execution Compatibility
- **Context**: Requirements 6 & 10 interact - VCR cassettes and pytest-xdist parallel testing
- **Sources Consulted**: Existing VCR configuration in conftest.py, pytest-xdist documentation
- **Findings**:
  - **Session-scoped fixtures**: pytest-xdist creates separate fixture instances per worker, so session-scoped `http` fixture is safe
  - **VCR cassettes**: Cassette files are read-only during replay, safe for parallel reads
  - **Cassette recording**: Recording mode "once" is safe (creates cassette only if missing, atomic file operations)
  - **Risk**: Tests that modify shared state or write to same cassette simultaneously may conflict
- **Implications**:
  - Session-scoped APIClient fixture is safe for parallel execution
  - VCR replay mode is safe for parallel execution
  - Add test marker for tests that must run serially (e.g., `@pytest.mark.serial`)
  - Document parallel safety in test organization
  - Consider separate cassette directories per test category to reduce contention

### Test Data Management Strategy
- **Context**: Requirement 8 needs centralized, reusable test data
- **Sources Consulted**: Existing `tests/data/activities.py`, gap analysis recommendations
- **Findings**:
  - Current pattern: Python modules with constants (e.g., `ACTIVITIES_POST_DATA`)
  - JSON files provide better separation and easier external editing
  - Factory functions useful for dynamic test data generation
  - Fixtures provide better isolation and teardown
- **Implications**:
  - Create `tests/fixtures/` module structure:
    - `tests/fixtures/__init__.py` - Fixture exports
    - `tests/fixtures/factories.py` - Factory functions for dynamic data
    - `tests/fixtures/data/` - JSON files for complex static data
  - Maintain existing `tests/data/*.py` pattern for simple constants
  - Re-export fixtures from conftest.py for convenience
  - Use pytest's `tmp_path` fixture for test isolation when needed

### Error Schema Discovery
- **Context**: Requirements 2 & 3 need error response validation
- **Sources Consulted**: SWAPI documentation, existing negative tests
- **Findings**:
  - SWAPI error format not documented in official docs
  - Existing negative test accepts both 404 and 200 (with empty results)
  - Need to test actual API behavior for 404, 400, 429 responses
  - Read-only API means 405 (Method Not Allowed) testing requires mocked responses
- **Implications**:
  - Create `error_schema.py` based on empirical testing
  - Error schema may be simple (e.g., `{"detail": "Not found"}`) or missing
  - Some error scenarios (401, 405, 400 with POST/PUT/DELETE) must be mocked
  - Document that SWAPI error format is reverse-engineered, not official

## Architecture Pattern Evaluation

| Option | Description | Strengths | Risks / Limitations | Decision |
|--------|-------------|-----------|---------------------|----------|
| **Flat Extension** | Add all new tests to existing test files | Minimal file changes, quick implementation | Files become large, harder to navigate | ❌ Not selected |
| **New Test Categories** | Create new directories (test-resilience, test-vcr) for new test types | Clean separation, clear organization | More files to manage | ✅ Partially - only for resilience/VCR |
| **Hybrid (Phased)** | Phase 1: Extend existing, Phase 2: New infrastructure, Phase 3: Advanced mocking | Incremental delivery, low risk | Requires coordination | ✅ **Selected** |

**Rationale**: Hybrid approach balances immediate value (Phase 1 extensions) with long-term maintainability (Phase 2 infrastructure). Phased implementation reduces risk and allows incremental testing of changes.

## Design Decisions

### Decision: Mocking Library - `responses`
- **Context**: Need to simulate HTTP errors, timeouts, and retry behavior for resilience testing
- **Alternatives Considered**:
  1. **responses** - Decorator-based, simple API, wide adoption
  2. **requests-mock** - More flexibility, similar features, different API
  3. **pytest-mock** - Lower-level, more setup, better for internal mocking
- **Selected Approach**: `responses` library
- **Rationale**:
  - Most popular (high community support, well-maintained)
  - Simple API aligns with existing pytest patterns
  - Excellent documentation for retry and timeout testing
  - Compatible with existing VCR.py setup (no conflicts)
  - Request matchers support validation of timeout parameters
- **Trade-offs**:
  - ✅ Easy to use, less boilerplate
  - ✅ Well-documented retry scenario testing
  - ✅ Active maintenance and community
  - ❌ Slightly less flexible than requests-mock (acceptable for our use cases)
- **Follow-up**: Verify `responses` works with session-scoped fixture in testing

### Decision: Schema Organization - Flat Structure with Registry
- **Context**: Need to add 5 new schema files (films, starships, vehicles, species, planets)
- **Alternatives Considered**:
  1. **Flat structure** - Simple, no changes to imports
  2. **Subdirectories by resource** - Organized but adds complexity
  3. **Registry pattern** - Centralized access via `__init__.py`
- **Selected Approach**: Flat structure with optional registry in `__init__.py`
- **Rationale**:
  - Existing pattern uses flat structure (page_schema.py, people_schema.py)
  - Adding 5 files keeps total at 7 schemas (manageable)
  - Registry provides convenience without forcing change to existing code
- **Trade-offs**:
  - ✅ Minimal disruption to existing imports
  - ✅ Scales well to ~10 schema files
  - ✅ Registry optional (backward compatible)
  - ❌ May need refactoring if schemas exceed 15+ files (unlikely)
- **Follow-up**: None

### Decision: Test Data Strategy - Hybrid (Constants + JSON + Factories)
- **Context**: Need reusable test data for various test scenarios
- **Alternatives Considered**:
  1. **Python constants only** - Current pattern, simple
  2. **JSON files only** - External data, easier to edit
  3. **Factory functions only** - Dynamic generation
  4. **Hybrid approach** - Use best tool for each case
- **Selected Approach**: Hybrid strategy
  - **Python constants** (`tests/data/*.py`) - Simple static data (e.g., list of endpoint paths)
  - **JSON files** (`tests/fixtures/data/*.json`) - Complex structures (e.g., full API responses)
  - **Factory functions** (`tests/fixtures/factories.py`) - Dynamic data generation (e.g., parametrized test data)
- **Rationale**:
  - Existing pattern works well for simple constants
  - JSON files better for complex, externally editable data
  - Factories best for dynamic, parameterized test scenarios
- **Trade-offs**:
  - ✅ Use best tool for each scenario
  - ✅ Maintains backward compatibility
  - ✅ Flexible for future needs
  - ❌ Requires understanding when to use each approach (document in README)
- **Follow-up**: Create documentation for test data strategy

### Decision: Fixture Organization - Extract to tests/fixtures/
- **Context**: conftest.py may become large with new fixtures (Requirement 8)
- **Alternatives Considered**:
  1. **Keep all in conftest.py** - Simple, single location
  2. **Extract to tests/fixtures/__init__.py** - Separate module, better organization
  3. **pytest plugin** - Most flexible, most complex
- **Selected Approach**: Extract to `tests/fixtures/__init__.py` when conftest.py exceeds 150 lines
- **Rationale**:
  - Current conftest.py is ~23 lines (manageable)
  - New fixtures will add ~50-100 lines
  - Threshold of 150 lines balances simplicity with organization
  - Import and re-export pattern maintains convenience
- **Trade-offs**:
  - ✅ Keeps conftest.py focused on configuration
  - ✅ Better organization for complex fixtures
  - ✅ Backward compatible (re-export in conftest.py)
  - ❌ Slightly more files (acceptable)
- **Follow-up**: None (implement during Phase 2)

### Decision: Resilience Test Organization - Separate Directory
- **Context**: HTTP client resilience tests (Requirement 5) are distinct from API tests
- **Alternatives Considered**:
  1. **Add to test-negative/** - Related to error scenarios
  2. **Create test-resilience/** - Separate directory for framework tests
  3. **Add to test-smoke/** - Related to availability
- **Selected Approach**: Create `tests/test-resilience/` directory
- **Rationale**:
  - Resilience tests validate APIClient behavior, not API responses
  - Different concern (framework testing vs. API testing)
  - May use different fixtures (mocked responses vs. live API)
  - Clearer intent and organization
- **Trade-offs**:
  - ✅ Clear separation of concerns
  - ✅ Easy to run independently
  - ✅ Aligns with test categorization pattern
  - ❌ One more directory (acceptable given benefit)
- **Follow-up**: None

## Risks & Mitigations

### Risk 1: API Schema Changes
- **Impact**: Existing skipped tests indicate API structure changes broke tests
- **Mitigation**:
  - Expand VCR usage for deterministic testing (reduce live API dependency)
  - Create schema validation helpers with detailed error messages
  - Document schema versions in cassettes
  - Consider schema tolerance for optional fields

### Risk 2: VCR Cassette Maintenance
- **Impact**: Cassettes may become stale if API changes
- **Mitigation**:
  - Use `record_mode="once"` to prevent accidental overwrites
  - Document cassette refresh process
  - Consider CI job to verify cassettes against live API periodically
  - Organize cassettes by test category for easier management

### Risk 3: Parallel Execution Conflicts
- **Impact**: Tests may conflict when running in parallel (cassette writes, shared state)
- **Mitigation**:
  - Mark tests requiring serial execution with `@pytest.mark.serial`
  - Use separate cassette directories per test category
  - Document parallel safety requirements
  - Test parallel execution in CI

### Risk 4: Test Execution Time
- **Impact**: Expanded test coverage may exceed acceptable execution time
- **Mitigation**:
  - Use `@pytest.mark.heavy` for slow tests
  - Leverage VCR to avoid live API calls (faster replay)
  - Use pytest-xdist for parallel execution
  - Monitor and optimize slow tests
  - Set 30-second target for smoke tests (Requirement 1.4)

### Risk 5: Mock Complexity
- **Impact**: Complex mocking scenarios may be hard to maintain
- **Mitigation**:
  - Create reusable mock fixtures
  - Document mock setup patterns
  - Keep mocks simple and focused
  - Use helper functions for common mock scenarios

## References
- [SWAPI Documentation](https://swapi.dev/documentation) — Official API documentation, endpoint catalog
- [responses Library](https://github.com/getsentry/responses) — Python requests mocking library
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/) — Parallel test execution
- [VCR.py Documentation](https://vcrpy.readthedocs.io/) — HTTP interaction recording
- [jsonschema Documentation](https://python-jsonschema.readthedocs.io/) — JSON schema validation
- [Pytest Documentation](https://docs.pytest.org/) — Testing framework
