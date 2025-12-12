# Testing

Tests are organized in `unit/` and `integration/` folders.

## Running Tests

### All tests

```bash
pytest -v
make test          # Alternative (requires make)
```

### Unit tests only

```bash
pytest tests/unit -v -m unit
make test-unit     # Alternative
```

### Integration tests only

```bash
pytest tests/integration -v -m integration
make test-integration     # Alternative
```

### With coverage

```bash
pytest --cov=. --cov-report=html --cov-report=term-missing
make test-coverage     # Alternative
```

> **Note**: `make` commands work in WSL/Linux. Use `pytest` commands directly in Git Bash/PowerShell.

## Coverage

- **Unit tests**: 35 tests covering event dispatchers, handlers and repositories.
- **Integration tests**: 21 tests covering API endpoints and RPC flows.
- **Total**: 56 tests

## Fixtures

Available in `conftest.py` and test modules:

- `sample_user`: User data dict for testing.
- `sample_user_with_id`: Complete user object with ID and timestamps.
- `mock_publisher`: Mocked Publisher to prevent AWS network calls.
- `reset_users_state`: Clears the in-memory `UserRepository` singleton.
- `reset_statistics_state`: Clears the in-memory `StatisticsRepository` singleton.
- `test_client`: FastAPI TestClient for endpoints.
- `handlers`: Instance of `EventHandlers` with injected repository (Unit tests only).
