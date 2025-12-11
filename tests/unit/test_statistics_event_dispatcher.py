

import pytest
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from freezegun import freeze_time
from apis.statistics.event_dispatcher import (
    total_users_rpc,
    total_updates_rpc,
    registered_last_24_rpc,
    user_registered_event,
    user_updated_event,
    TOTAL_USERS,
    TOTAL_UPDATES,
    REGISTERED_USERS_TIMELINE
)


@pytest.mark.unit
class TestTotalUsersRPC:
    
    def test_total_users_initial_zero(self, reset_statistics_state):
        result = total_users_rpc({})
        
        assert result["total_users"] == 0
    
    def test_total_users_after_registration(self, reset_statistics_state):
        user_registered_event({})
        user_registered_event({})
        
        result = total_users_rpc({})
        
        assert result["total_users"] == 2


@pytest.mark.unit
class TestTotalUpdatesRPC:
    
    def test_total_updates_initial_zero(self, reset_statistics_state):
        result = total_updates_rpc({})
        
        assert result["total_updates"] == 0
    
    def test_total_updates_after_update_events(self, reset_statistics_state):
        user_updated_event({})
        user_updated_event({})
        user_updated_event({})
        
        result = total_updates_rpc({})
        
        assert result["total_updates"] == 3


@pytest.mark.unit
class TestRegisteredLast24RPC:
    
    @freeze_time("2024-12-10 12:00:00")
    def test_registered_last_24h_empty(self, reset_statistics_state):
        result = registered_last_24_rpc({})
        
        assert result["registered_last_24h"] == 0
    
    @freeze_time("2024-12-10 12:00:00")
    def test_registered_last_24h_within_window(self, reset_statistics_state):
        user_registered_event({})
        user_registered_event({})
        
        result = registered_last_24_rpc({})
        
        assert result["registered_last_24h"] == 2
    
    def test_registered_last_24h_excludes_old_registrations(self, reset_statistics_state):
        from apis.statistics.event_dispatcher import REGISTERED_USERS_TIMELINE
        
        argentina_tz = ZoneInfo("America/Argentina/Buenos_Aires")
        old_timestamp = datetime.now(argentina_tz) - timedelta(hours=26)
        REGISTERED_USERS_TIMELINE.append(old_timestamp)
        
        recent_timestamp = datetime.now(argentina_tz) - timedelta(hours=1)
        REGISTERED_USERS_TIMELINE.append(recent_timestamp)
        
        result = registered_last_24_rpc({})
        
        assert result["registered_last_24h"] == 1
    
    def test_registered_last_24h_boundary_case(self, reset_statistics_state):
        from apis.statistics.event_dispatcher import REGISTERED_USERS_TIMELINE
        
        argentina_tz = ZoneInfo("America/Argentina/Buenos_Aires")
        exactly_24h = datetime.now(argentina_tz) - timedelta(hours=24)
        REGISTERED_USERS_TIMELINE.append(exactly_24h)
        
        within_24h = datetime.now(argentina_tz) - timedelta(hours=23, minutes=30)
        REGISTERED_USERS_TIMELINE.append(within_24h)
        
        result = registered_last_24_rpc({})
        
        assert result["registered_last_24h"] >= 1


@pytest.mark.unit
class TestUserRegisteredEvent:
    
    def test_user_registered_increments_total(self, reset_statistics_state):
        from apis.statistics.event_dispatcher import TOTAL_USERS as initial
        
        user_registered_event({"id": 1, "name": "Test"})
        
        from apis.statistics.event_dispatcher import TOTAL_USERS as final
        assert final == initial + 1
    
    def test_user_registered_adds_to_timeline(self, reset_statistics_state):
        from apis.statistics.event_dispatcher import REGISTERED_USERS_TIMELINE
        
        initial_count = len(REGISTERED_USERS_TIMELINE)
        user_registered_event({"id": 1, "name": "Test"})
        
        assert len(REGISTERED_USERS_TIMELINE) == initial_count + 1
        assert isinstance(REGISTERED_USERS_TIMELINE[-1], datetime)
    
    def test_user_registered_multiple_events(self, reset_statistics_state):
        user_registered_event({})
        user_registered_event({})
        user_registered_event({})
        
        result = total_users_rpc({})
        assert result["total_users"] == 3


@pytest.mark.unit
class TestUserUpdatedEvent:
    
    def test_user_updated_increments_total(self, reset_statistics_state):
        from apis.statistics.event_dispatcher import TOTAL_UPDATES as initial
        
        user_updated_event({"id": 1, "name": "Updated"})
        
        from apis.statistics.event_dispatcher import TOTAL_UPDATES as final
        assert final == initial + 1
    
    def test_user_updated_multiple_events(self, reset_statistics_state):
        user_updated_event({})
        user_updated_event({})
        
        result = total_updates_rpc({})
        assert result["total_updates"] == 2
    
    def test_user_updated_does_not_affect_total_users(self, reset_statistics_state):
        user_updated_event({})
        
        result = total_users_rpc({})
        assert result["total_users"] == 0
