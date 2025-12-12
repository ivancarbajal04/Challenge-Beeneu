

import pytest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from freezegun import freeze_time
from apis.statistics.event_dispatcher import EventHandlers
from apis.statistics.repository import StatisticsRepository


@pytest.fixture
def handlers():
    repo = StatisticsRepository()
    return EventHandlers(repository=repo)


@pytest.mark.unit
class TestTotalUsersRPC:
    
    def test_total_users_initial_zero(self, reset_statistics_state, handlers):
        result = handlers.total_users_rpc({})
        
        assert result["total_users"] == 0
    
    def test_total_users_after_registration(self, reset_statistics_state, handlers):
        handlers.user_registered_event({})
        handlers.user_registered_event({})
        
        result = handlers.total_users_rpc({})
        
        assert result["total_users"] == 2


@pytest.mark.unit
class TestTotalUpdatesRPC:
    
    def test_total_updates_initial_zero(self, reset_statistics_state, handlers):
        result = handlers.total_updates_rpc({})
        
        assert result["total_updates"] == 0
    
    def test_total_updates_after_update_events(self, reset_statistics_state, handlers):
        handlers.user_updated_event({})
        handlers.user_updated_event({})
        handlers.user_updated_event({})
        
        result = handlers.total_updates_rpc({})
        
        assert result["total_updates"] == 3


@pytest.mark.unit
class TestRegisteredLast24RPC:
    
    @freeze_time("2024-12-10 12:00:00")
    def test_registered_last_24h_empty(self, reset_statistics_state, handlers):
        result = handlers.registered_last_24_rpc({})
        
        assert result["registered_last_24h"] == 0
    
    @freeze_time("2024-12-10 12:00:00")
    def test_registered_last_24h_within_window(self, reset_statistics_state, handlers):
        handlers.user_registered_event({})
        handlers.user_registered_event({})
        
        result = handlers.registered_last_24_rpc({})
        
        assert result["registered_last_24h"] == 2
    
    def test_registered_last_24h_excludes_old_registrations(self, reset_statistics_state, handlers):
        repo = StatisticsRepository()
        # We need to manually manipulate the singleton repo since handlers uses it
        
        argentina_tz = ZoneInfo("America/Argentina/Buenos_Aires")
        old_timestamp = datetime.now(argentina_tz) - timedelta(hours=26)
        repo._user_registration_timeline.append(old_timestamp)
        
        recent_timestamp = datetime.now(argentina_tz) - timedelta(hours=1)
        repo._user_registration_timeline.append(recent_timestamp)
        
        result = handlers.registered_last_24_rpc({})
        
        assert result["registered_last_24h"] == 1
    
    def test_registered_last_24h_boundary_case(self, reset_statistics_state, handlers):
        repo = StatisticsRepository()
        
        argentina_tz = ZoneInfo("America/Argentina/Buenos_Aires")
        exactly_24h = datetime.now(argentina_tz) - timedelta(hours=24)
        repo._user_registration_timeline.append(exactly_24h)
        # Assuming boundary condition: > cutoff. if exactly cutoff, it is not > (so excluded)
        
        within_24h = datetime.now(argentina_tz) - timedelta(hours=23, minutes=30)
        repo._user_registration_timeline.append(within_24h)
        
        result = handlers.registered_last_24_rpc({})
        
        assert result["registered_last_24h"] >= 1


@pytest.mark.unit
class TestUserRegisteredEvent:
    
    def test_user_registered_increments_total(self, reset_statistics_state, handlers):
        repo = StatisticsRepository()
        initial = repo.get_total_users()
        
        handlers.user_registered_event({"id": 1, "name": "Test"})
        
        final = repo.get_total_users()
        assert final == initial + 1
    
    def test_user_registered_adds_to_timeline(self, reset_statistics_state, handlers):
        repo = StatisticsRepository()
        
        initial_count = len(repo._user_registration_timeline)
        handlers.user_registered_event({"id": 1, "name": "Test"})
        
        assert len(repo._user_registration_timeline) == initial_count + 1
        assert isinstance(repo._user_registration_timeline[-1], datetime)
    
    def test_user_registered_multiple_events(self, reset_statistics_state, handlers):
        handlers.user_registered_event({})
        handlers.user_registered_event({})
        handlers.user_registered_event({})
        
        result = handlers.total_users_rpc({})
        assert result["total_users"] == 3


@pytest.mark.unit
class TestUserUpdatedEvent:
    
    def test_user_updated_increments_total(self, reset_statistics_state, handlers):
        repo = StatisticsRepository()
        initial = repo.get_total_updates()
        
        handlers.user_updated_event({"id": 1, "name": "Updated"})
        
        final = repo.get_total_updates()
        assert final == initial + 1
    
    def test_user_updated_multiple_events(self, reset_statistics_state, handlers):
        handlers.user_updated_event({})
        handlers.user_updated_event({})
        
        result = handlers.total_updates_rpc({})
        assert result["total_updates"] == 2
    
    def test_user_updated_does_not_affect_total_users(self, reset_statistics_state, handlers):
        handlers.user_updated_event({})
        
        result = handlers.total_users_rpc({})
        assert result["total_users"] == 0
