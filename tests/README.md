# Testing

Tests are organized in `unit/` and `integration/` folders.

## Running Tests

```bash
# All tests
pytest -v
make test          # Alternative (requires make)

# Unit tests only
pytest tests/unit -v -m unit
make test-unit     # Alternative

# Integration tests only
pytest tests/integration -v -m integration
make test-integration     # Alternative

# With coverage
pytest --cov=. --cov-report=html --cov-report=term-missing
make test-coverage     # Alternative
```

**Note:** `make` commands work in WSL/Linux. Use `pytest` commands directly in Git Bash/PowerShell.

## Coverage

- **Unit tests**: 32 tests covering event dispatchers
- **Integration tests**: 20 tests covering API endpoints
- **Total**: 52 tests

## Fixtures

Available in `conftest.py`:

- `sample_user` - User data dict
- `sample_user_with_id` - Complete user object
- `mock_publisher` - Mocked Publisher
- `reset_users_state` - Clean users state
- `reset_statistics_state` - Clean statistics state
- `test_client` - FastAPI test client
