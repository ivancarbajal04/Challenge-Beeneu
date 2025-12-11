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
    from apis.users import event_dispatcher
    original_users = event_dispatcher.USERS.copy()
    original_count = event_dispatcher.USER_UPDATES_COUNT
    event_dispatcher.USERS.clear()
    event_dispatcher.USER_UPDATES_COUNT = 0
    yield
    event_dispatcher.USERS.clear()
    event_dispatcher.USERS.extend(original_users)
    event_dispatcher.USER_UPDATES_COUNT = original_count


@pytest.fixture
def reset_statistics_state():
    from apis.statistics import event_dispatcher
    original_total_users = event_dispatcher.TOTAL_USERS
    original_total_updates = event_dispatcher.TOTAL_UPDATES
    original_timeline = event_dispatcher.REGISTERED_USERS_TIMELINE.copy()
    event_dispatcher.TOTAL_USERS = 0
    event_dispatcher.TOTAL_UPDATES = 0
    event_dispatcher.REGISTERED_USERS_TIMELINE.clear()
    yield
    event_dispatcher.TOTAL_USERS = original_total_users
    event_dispatcher.TOTAL_UPDATES = original_total_updates
    event_dispatcher.REGISTERED_USERS_TIMELINE.clear()
    event_dispatcher.REGISTERED_USERS_TIMELINE.extend(original_timeline)


@pytest.fixture
def test_client():
    from main import app
    return TestClient(app)
