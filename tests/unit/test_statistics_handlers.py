from unittest.mock import MagicMock
import pytest
from apis.statistics.event_dispatcher import EventHandlers

class TestStatisticsEventHandlers:
    @pytest.fixture
    def mock_repo(self):
        return MagicMock()

    @pytest.fixture
    def handlers(self, mock_repo):
        return EventHandlers(repository=mock_repo)

    def test_total_users_rpc(self, handlers, mock_repo):
        mock_repo.get_total_users.return_value = 10
        result = handlers.total_users_rpc({})
        assert result["total_users"] == 10

    def test_user_registered_event(self, handlers, mock_repo):
        handlers.user_registered_event({})
        mock_repo.increment_total_users.assert_called_once()
