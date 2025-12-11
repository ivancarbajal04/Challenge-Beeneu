# Testing

Los tests están organizados en las carpetas `unit/` e `integration/`.

## Ejecutar Tests

```bash
# Todos los tests
pytest -v
make test          # Alternativa (requiere make)

# Solo tests unitarios
pytest tests/unit -v -m unit
make test-unit     # Alternativa

# Solo tests de integración
pytest tests/integration -v -m integration
make test-integration     # Alternativa

# Con coverage
pytest --cov=. --cov-report=html --cov-report=term-missing
make test-coverage     # Alternativa
```

**Nota:** Los comandos `make` funcionan en WSL/Linux. Usar comandos `pytest` directamente en Git Bash/PowerShell.

## Coverage

- **Tests unitarios**: 32 tests cubriendo event dispatchers
- **Tests de integración**: 20 tests cubriendo endpoints del API
- **Total**: 52 tests

## Fixtures

Disponibles en `conftest.py`:

- `sample_user` - Diccionario con datos de usuario
- `sample_user_with_id` - Objeto usuario completo
- `mock_publisher` - Publisher mockeado
- `reset_users_state` - Limpia estado de users
- `reset_statistics_state` - Limpia estado de statistics
- `test_client` - Cliente de test de FastAPI
