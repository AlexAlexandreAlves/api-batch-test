# Implementation Plan: Enhanced Test Coverage

## Phase Overview

This implementation follows a three-phase hybrid approach:
- **Phase 1**: Extend existing test categories (low risk, immediate value)
- **Phase 2**: Build test infrastructure (helpers, fixtures, mocks)
- **Phase 3**: Advanced testing with mocking (resilience, VCR functionality)

## Implementation Tasks

### Phase 1: Extend Existing Test Categories

- [ ] 1. Expand API endpoint constants
- [x] 1.1 (P) Add new resource endpoint constants to Endpoints class
  - Add collection endpoints for films, starships, vehicles, species, and planets
  - Add individual resource endpoints with ID placeholders for all new resources
  - Add optional schema endpoints for future use
  - Use Final type hints for all constants
  - Follow existing pattern (paths start and end with `/`)
  - _Requirements: 1.1_

- [ ] 2. Create resource schema definitions
- [ ] 2.1 (P) Create films resource schema
  - Define JSON schema with all required fields from SWAPI films endpoint
  - Include validation for title, episode_id, opening_crawl, director, producer, release_date
  - Add array fields for characters, planets, starships, vehicles, species relationships
  - Use string pattern validation for URLs and ISO dates
  - Set additionalProperties to False for strict validation
  - _Requirements: 2.4_

- [ ] 2.2 (P) Create starships resource schema
  - Define JSON schema with required fields for starship properties
  - Include name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed
  - Add crew, passengers, cargo_capacity, consumables, hyperdrive_rating, MGLT, starship_class
  - Include array fields for pilots and films relationships
  - Handle "unknown" values in string fields appropriately
  - _Requirements: 2.4_

- [ ] 2.3 (P) Create vehicles resource schema
  - Define JSON schema for vehicle resource type
  - Include name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed
  - Add crew, passengers, cargo_capacity, consumables, vehicle_class fields
  - Include array fields for pilots and films relationships
  - Follow same pattern as starships schema for consistency
  - _Requirements: 2.4_

- [ ] 2.4 (P) Create species resource schema
  - Define JSON schema for species resource type
  - Include name, classification, designation, average_height, skin_colors, hair_colors, eye_colors
  - Add average_lifespan, homeworld (nullable), language fields
  - Include array fields for people and films relationships
  - Handle null homeworld values in schema validation
  - _Requirements: 2.4_

- [ ] 2.5 (P) Create planets resource schema
  - Define JSON schema for planets resource type
  - Include name, rotation_period, orbital_period, diameter, climate, gravity, terrain
  - Add surface_water, population fields
  - Include array fields for residents and films relationships
  - Use string type for numeric fields to match API format
  - _Requirements: 2.4_

- [ ] 2.6 (P) Create error response schema
  - Define flexible JSON schema for API error responses
  - Support multiple error field names (detail, message, error)
  - Allow optional error code field (string or integer)
  - Set minProperties to 1 to require at least one error field
  - Enable additionalProperties for API flexibility
  - _Requirements: 2.5, 3.6_

- [ ] 3. Extend smoke test coverage
- [ ] 3.1 Add parametrized smoke tests for all resources
  - Create parametrized test with all 6 resource endpoints (people, films, starships, vehicles, species, planets)
  - Validate 2xx status codes for each endpoint
  - Validate Content-Type headers match application/json
  - Use descriptive test IDs for each resource
  - Add VCR marker with record_mode="once" for deterministic testing
  - Add smoke marker for selective execution
  - Include diagnostic information in assertions (endpoint, expected, actual)
  - _Requirements: 1.1, 1.2, 1.3, 1.5_

- [ ] 3.2* Verify smoke test performance constraint
  - Run all smoke tests with timing measurement
  - Verify total execution time is under 30 seconds
  - Use pytest --durations=0 to identify slow tests
  - Document any tests exceeding 5 seconds individually
  - _Requirements: 1.4_

- [ ] 4. Expand contract validation tests
- [ ] 4.1 Add parametrized contract tests for resource collections
  - Create parametrized test for all 6 resource collection endpoints
  - Validate pagination schema (PAGE_SCHEMA) for all collections
  - Validate individual item schemas for each resource type
  - Iterate through results array and validate each item
  - Use descriptive test IDs matching resource names
  - Add contract marker for selective execution
  - _Requirements: 2.1, 2.2, 2.3_

- [ ] 4.2 (P) Add parametrized contract tests for individual resources
  - Create parametrized test for individual resource endpoints (with ID)
  - Test with valid IDs for each resource type (e.g., /people/1, /films/1)
  - Validate individual resource schema for each type
  - Verify response is object (not array)
  - Add contract marker for selective execution
  - _Requirements: 2.3_

- [ ] 5. Enhance negative testing scenarios
- [ ] 5.1 Add parametrized tests for error scenarios
  - Extend existing parametrize with 404 tests for all resource types
  - Add tests for invalid resource IDs (99999) across all endpoints
  - Add tests for out-of-bounds pagination (page=999) for all collections
  - Validate responses are either 404 or 200 with empty results
  - Use descriptive test IDs for each scenario
  - Add negative marker for selective execution
  - _Requirements: 3.2_

- [ ] 5.2 (P) Add boundary condition tests for query parameters
  - Test negative page numbers (page=-1)
  - Test zero page number (page=0)
  - Test extremely large page numbers (page=999999)
  - Test special characters in search parameters
  - Verify API handles gracefully (404, 400, or 200 with empty results)
  - _Requirements: 3.9_

- [ ] 6. Extend pagination testing
- [ ] 6.1 Add boundary condition pagination tests
  - Test first page validation (previous field is null)
  - Test last page validation (next field is null)
  - Test page=0 boundary condition
  - Test negative page number handling
  - Test page beyond total pages
  - Verify appropriate error or empty result handling
  - _Requirements: 4.4, 4.5, 4.9_

- [ ] 6.2 Add previous link traversal tests
  - Verify previous URL is valid when present
  - Test following previous link returns 200 OK
  - Validate previous link pagination consistency
  - Complement existing next link tests
  - _Requirements: 4.7_

### Phase 2: Build Test Infrastructure

- [ ] 7. Create schema validation helpers
- [ ] 7.1 Implement enhanced schema validator with error formatting
  - Create validate_schema function returning (bool, Optional[str]) tuple
  - Wrap jsonschema.validate with try/except for ValidationError
  - Create format_validation_error function with path extraction
  - Format error messages with schema label, path, message, and expected type
  - Use absolute_path from ValidationError for nested field errors
  - _Requirements: 2.5, 2.6, 2.7_

- [ ] 7.2 Implement pytest-friendly assertion helper
  - Create assert_valid_schema function that raises AssertionError
  - Use validate_schema internally for validation
  - Include detailed diagnostic message in assertion failures
  - Provide optional schema_name parameter for error context
  - Ensure error messages are pytest-friendly with clear failure information
  - _Requirements: 2.5, 9.2, 9.3_

- [ ] 8. Create test data management utilities
- [ ] 8.1 (P) Implement JSON test data loader
  - Create load_json_data function with Optional return type
  - Accept filename and optional data_dir parameter
  - Default to tests/fixtures/data/ directory
  - Return None if file not found (graceful handling)
  - Raise json.JSONDecodeError for invalid JSON
  - Use pathlib for cross-platform path handling
  - _Requirements: 8.3_

- [ ] 8.2 (P) Implement required JSON data loader variant
  - Create load_json_data_required function
  - Raise FileNotFoundError if file doesn't exist (strict handling)
  - Reuse load_json_data internally for parsing
  - Provide clear error message with filename
  - Return typed Dict[str, Any] for type safety
  - _Requirements: 8.3_

- [ ] 8.3 (P) Create test fixtures directory structure
  - Create tests/fixtures/ directory
  - Create tests/fixtures/__init__.py for fixture exports
  - Create tests/fixtures/data/ subdirectory for JSON files
  - Add __init__.py files for proper Python package structure
  - _Requirements: 8.1, 8.2_

- [ ] 9. Set up mocking infrastructure
- [ ] 9.1 Install responses library
  - Add responses library to requirements.txt (version 0.25+)
  - Document mocking library choice in comments
  - Verify compatibility with existing requests version
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

- [ ] 9.2 Create mock response fixtures
  - Create tests/mocks/ directory
  - Create tests/mocks/__init__.py for fixture definitions
  - _Requirements: 3.1, 3.3, 3.4, 3.5, 3.7, 3.8, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [ ] 9.3 Implement mock_responses base fixture
  - Create pytest fixture activating responses.RequestsMock context
  - Yield rsps object for test use
  - Ensure automatic cleanup between tests
  - Document fixture usage in docstring
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [ ] 9.4 (P) Implement mock_retry_scenario fixture
  - Create fixture accepting endpoint, failures list, success_status, success_body
  - Register multiple responses for same endpoint (retry testing)
  - Support list of failure status codes (e.g., [503, 502])
  - Register final success response
  - Return registration function for test use
  - _Requirements: 5.2, 5.3_

- [ ] 9.5 (P) Implement mock_timeout_scenario fixture
  - Create fixture accepting endpoint and timeout_type parameter
  - Support "connect" and "read" timeout types
  - Register ConnectTimeout or ReadTimeout exception
  - Return registration function for test use
  - _Requirements: 5.5, 5.6_

- [ ] 9.6 (P) Implement mock_rate_limit fixture
  - Create fixture accepting endpoint and retry_after parameter
  - Register 429 status response
  - Include Retry-After header with configurable value
  - Add error body with rate limit message
  - Return registration function for test use
  - _Requirements: 5.1_

- [ ] 9.7 (P) Implement mock_error_responses fixture
  - Create fixture accepting endpoint, status_code, optional error_body
  - Support 400, 401, 404, 405 status codes
  - Provide default error messages for each status code
  - Allow custom error body override
  - Return registration function for test use
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 10. Update conftest.py with new fixtures
- [ ] 10.1 Import and re-export new fixtures
  - Import validators from src.helpers.validators
  - Import test_data utilities from src.helpers.test_data
  - Import mock fixtures from tests.mocks
  - Re-export for convenience in test files
  - Maintain existing fixture exports (http, base_url, vcr_config, vcr_cassette_dir)
  - _Requirements: 8.2, 8.5_

### Phase 3: Advanced Testing

- [ ] 11. Create HTTP client resilience tests
- [ ] 11.1 Set up resilience test directory
  - Create tests/test-resilience/ directory
  - Create tests/test-resilience/__init__.py
  - Document that resilience tests validate APIClient features, not API
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

- [ ] 11.2 Implement retry behavior tests
  - Test retry on 5xx errors with exponential backoff
  - Register multiple 5xx responses followed by success
  - Measure elapsed time to verify backoff occurred
  - Verify final success response received
  - Assert elapsed time exceeds expected backoff duration
  - Add resilience marker for selective execution
  - _Requirements: 5.2, 5.3_

- [ ] 11.3 Implement timeout handling tests
  - Test connection timeout exception handling
  - Test read timeout exception handling
  - Register timeout exceptions using mock_timeout_scenario
  - Verify APIClient raises ConnectTimeout or ReadTimeout
  - Use pytest.raises context manager
  - Add resilience marker for selective execution
  - _Requirements: 5.5, 5.6_

- [ ] 11.4 Implement rate limiting tests
  - Test 429 response handling
  - Verify Retry-After header is present
  - Register rate limit response using mock_rate_limit fixture
  - Validate status code and header values
  - Document that actual retry-after delay respecting is APIClient responsibility
  - Add resilience marker for selective execution
  - _Requirements: 5.1, 5.4_

- [ ] 11.5* Implement connection pooling validation
  - Test session adapter maintains connection pool across requests
  - Make multiple requests to same endpoint
  - Verify requests use same session (implementation detail)
  - Document connection pooling benefits
  - _Requirements: 5.7_

- [ ] 12. Create VCR functionality tests
- [ ] 12.1 Set up VCR test directory
  - Create tests/test-vcr/ directory
  - Create tests/test-vcr/__init__.py
  - Document that VCR tests validate recording/replay features
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_

- [ ] 12.2 Implement VCR recording and replay tests
  - Test cassette creation on first run
  - Test cassette replay on subsequent runs
  - Verify no live API calls during replay
  - Test record_mode="once" behavior
  - Validate cassette storage in tests/cassettes/ directory
  - Add vcr marker for selective execution
  - _Requirements: 6.1, 6.2, 6.7, 6.8_

- [ ] 12.3 Implement VCR filtering tests
  - Test Authorization header filtering from cassettes
  - Test api_key query parameter filtering
  - Test token query parameter filtering
  - Verify sensitive data not stored in cassette files
  - Validate vcr_config fixture settings
  - _Requirements: 6.3, 6.4_

- [ ] 12.4 Implement VCR matching tests
  - Test request matching on method
  - Test request matching on scheme, host, port, path
  - Test request matching on query parameters
  - Verify decode_compressed_response setting works
  - Validate match_on configuration from vcr_config
  - _Requirements: 6.5, 6.6_

- [ ] 13. Add advanced negative tests with mocking
- [ ] 13.1 Implement authentication error tests (mocked)
  - Test 401 Unauthorized response handling
  - Use mock_error_responses fixture for 401 status
  - Verify error response validation
  - Document that SWAPI has no auth (mock-only test)
  - Add negative marker for selective execution
  - _Requirements: 3.1_

- [ ] 13.2 Implement method not allowed tests (mocked)
  - Test 405 Method Not Allowed response handling
  - Use mock_error_responses fixture for 405 status
  - Test POST, PUT, DELETE methods (not supported by SWAPI)
  - Verify error response validation
  - Document read-only API limitation
  - Add negative marker for selective execution
  - _Requirements: 3.3_

- [ ] 13.3 Implement bad request tests (mocked)
  - Test 400 Bad Request response handling
  - Use mock_error_responses fixture for 400 status
  - Test malformed request payloads
  - Test invalid data types in request bodies
  - Verify error schema validation
  - Add negative marker for selective execution
  - _Requirements: 3.4, 3.10_

- [ ] 13.4 Implement timeout scenario tests (mocked)
  - Test connection timeout handling using mock_timeout_scenario
  - Test read timeout handling using mock_timeout_scenario
  - Verify APIClient raises appropriate exceptions
  - Test both timeout types separately
  - Add negative marker for selective execution
  - _Requirements: 3.7_

- [ ] 13.5 Implement server error retry tests (mocked)
  - Test retry behavior on 5xx errors using mock_retry_scenario
  - Verify retry mechanism attempts configured number of retries
  - Test eventual success after retries
  - Test failure after max retries exceeded
  - Add negative marker for selective execution
  - _Requirements: 3.8_

- [ ] 14. Validate parallel execution compatibility
- [ ] 14.1* Verify pytest-xdist compatibility
  - Run test suite with pytest -n4 for parallel execution
  - Verify session-scoped fixtures work correctly in parallel
  - Test VCR cassette access in parallel (replay mode)
  - Identify any race conditions or shared state issues
  - Document any tests requiring serial execution
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 14.2* Add serial execution markers if needed
  - Mark tests requiring serial execution with @pytest.mark.serial
  - Document why specific tests cannot run in parallel
  - Verify marked tests run correctly in serial mode
  - Update pytest.ini if serial marker needs definition
  - _Requirements: 10.5_

- [ ] 15. Integration validation
- [ ] 15.1 Run complete test suite and verify coverage
  - Execute all test categories (smoke, contract, pagination, negative, resilience, vcr)
  - Verify all 10 requirements have passing tests
  - Check HTML report for comprehensive coverage
  - Validate no skipped tests remain (except intentionally deferred)
  - Measure total test execution time
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.10, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 7.1, 7.2, 7.3, 7.4, 7.5, 8.1, 8.2, 8.3, 8.4, 8.5, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 15.2 Verify VCR cassettes are created and functional
  - Check tests/cassettes/ directory for new cassette files
  - Verify cassettes for all 6 resource types
  - Test replay mode works (run tests without network access)
  - Validate cassette file sizes are reasonable
  - Document cassette refresh process if needed
  - _Requirements: 6.1, 6.2, 6.7, 6.8_

- [ ] 15.3 Validate schema definitions against live API
  - Run contract tests against live API (record mode)
  - Verify all resource schemas match actual API responses
  - Check for any schema validation failures
  - Update schemas if API structure has changed
  - Document any schema version assumptions
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ] 15.4 Test parallel execution performance
  - Run test suite with pytest -n4 to measure speedup
  - Compare execution time vs serial execution
  - Verify 4x speedup is achieved (or document bottlenecks)
  - Ensure all tests pass in parallel mode
  - Document any parallel execution issues
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

## Requirements Coverage Matrix

| Requirement | Tasks |
|-------------|-------|
| 1.1 | 1.1, 3.1 |
| 1.2 | 3.1 |
| 1.3 | 3.1 |
| 1.4 | 3.2 |
| 1.5 | 3.1 |
| 2.1 | 4.1, 15.3 |
| 2.2 | 4.1 |
| 2.3 | 4.1, 4.2 |
| 2.4 | 2.1, 2.2, 2.3, 2.4, 2.5, 15.3 |
| 2.5 | 2.6, 7.1, 7.2 |
| 2.6 | 7.1 |
| 2.7 | 7.1 |
| 3.1 | 9.7, 13.1 |
| 3.2 | 5.1, 9.7 |
| 3.3 | 9.7, 13.2 |
| 3.4 | 9.7, 13.3 |
| 3.5 | 9.7 |
| 3.6 | 2.6 |
| 3.7 | 9.2, 13.4 |
| 3.8 | 9.2, 13.5 |
| 3.9 | 5.2 |
| 3.10 | 13.3 |
| 4.1 | 15.1 |
| 4.2 | 15.1 |
| 4.3 | 15.1 |
| 4.4 | 6.1 |
| 4.5 | 6.1 |
| 4.6 | 15.1 |
| 4.7 | 6.2 |
| 4.8 | 15.1 |
| 4.9 | 6.1 |
| 4.10 | 15.1 |
| 5.1 | 9.1, 9.3, 9.6, 11.1, 11.4 |
| 5.2 | 9.1, 9.3, 9.4, 11.1, 11.2 |
| 5.3 | 9.1, 9.3, 9.4, 11.1, 11.2 |
| 5.4 | 9.1, 9.3, 11.1, 11.4 |
| 5.5 | 9.1, 9.3, 9.5, 11.1, 11.3 |
| 5.6 | 9.1, 9.2, 9.3, 9.5, 11.1, 11.3 |
| 5.7 | 9.1, 11.1, 11.5 |
| 6.1 | 12.1, 12.2, 15.2 |
| 6.2 | 12.1, 12.2, 15.2 |
| 6.3 | 12.1, 12.3 |
| 6.4 | 12.1, 12.3 |
| 6.5 | 12.1, 12.4 |
| 6.6 | 12.1, 12.4 |
| 6.7 | 12.1, 12.2, 15.2 |
| 6.8 | 12.1, 12.2, 15.2 |
| 7.1 | 15.1 |
| 7.2 | 15.1 |
| 7.3 | 15.1 |
| 7.4 | 15.1 |
| 7.5 | 15.1 |
| 8.1 | 8.3 |
| 8.2 | 10.1 |
| 8.3 | 8.1, 8.2 |
| 8.4 | 15.1 |
| 8.5 | 10.1 |
| 9.1 | 15.1 |
| 9.2 | 7.2 |
| 9.3 | 7.2 |
| 9.4 | 15.1 |
| 9.5 | 15.1 |
| 9.6 | 15.1 |
| 9.7 | 15.1 |
| 10.1 | 14.1, 15.4 |
| 10.2 | 14.1, 15.4 |
| 10.3 | 14.1, 15.4 |
| 10.4 | 14.1, 15.4 |
| 10.5 | 14.2 |

## Execution Guidance

### Phase 1 (Tasks 1-6)
- Can be executed in parallel where marked with (P)
- Low risk, extends existing patterns
- Provides immediate value with expanded test coverage
- Estimated time: 2-3 days

### Phase 2 (Tasks 7-10)
- Infrastructure setup for Phase 3
- Tasks within same major task can be parallelized
- Creates foundation for advanced testing
- Estimated time: 3-4 days

### Phase 3 (Tasks 11-15)
- Advanced testing with mocking
- Some tasks depend on Phase 2 completion
- Highest value for resilience validation
- Integration tasks validate complete system
- Estimated time: 3-4 days

### Parallel Execution Notes
- Tasks marked (P) can be executed concurrently
- Ensure no file conflicts when running parallel tasks
- Session-scoped fixtures are safe for parallel execution
- VCR cassettes in replay mode are safe for parallel reads
- Mock fixtures use per-test context (responses library)

### Optional Tasks
- Tasks marked with `*` are optional and can be deferred post-MVP
- These tasks primarily validate non-functional requirements or edge cases
- Core functionality is testable without these tasks
- Recommended to complete for comprehensive coverage
