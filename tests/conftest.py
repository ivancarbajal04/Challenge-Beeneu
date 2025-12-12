import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import datetime
from zoneinfo import ZoneInfo
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_user():
    return {
        "name": "John",
        "surname": "Doe",
        "dni": "12345678",
        "address": "123 Main St"
    }


@pytest.fixture
def sample_user_with_id():
    argentina_tz = ZoneInfo("America/Argentina/Buenos_Aires")
    return {
        "id": 1,
        "name": "John",
        "surname": "Doe",
        "dni": "12345678",
        "address": "123 Main St",
        "created_at": datetime.now(argentina_tz).isoformat(),
        "updated_at": datetime.now(argentina_tz).isoformat()
    }


@pytest.fixture
def mock_publisher():
    mock = MagicMock()
    mock.call_rpc.return_value = {
        "success": True,
        "data": {"id": 1, "name": "Test User"},
        "status": "OK"
    }
    mock.publish.return_value = {
        "success": True,
        "correlation_id": "test-correlation-id"
    }
    return mock


@pytest.fixture
def reset_users_state():
    from apis.users.repository import UserRepository
    repo = UserRepository()
    original_users = repo.users.copy()
    original_count = repo._updates_count
    
    repo.users.clear()
    repo._updates_count = 0
    
    yield
    
    repo.users.clear()
    repo.users.extend(original_users)
    repo._updates_count = original_count


@pytest.fixture
def reset_statistics_state():
    from apis.statistics.repository import StatisticsRepository
    repo = StatisticsRepository()
    
    original_total_users = repo._total_users
    original_total_updates = repo._total_updates
    original_timeline = repo._user_registration_timeline.copy()
    
    repo._total_users = 0
    repo._total_updates = 0
    repo._user_registration_timeline.clear()
    
    yield
    
    repo._total_users = original_total_users
    repo._total_updates = original_total_updates
    repo._user_registration_timeline.clear()
    repo._user_registration_timeline.extend(original_timeline)


@pytest.fixture
def test_client():
    from main import app
    return TestClient(app)
