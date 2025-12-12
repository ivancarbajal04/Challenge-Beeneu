from unittest.mock import MagicMock
import pytest
from apis.users.event_dispatcher import EventHandlers
from apis.users.repository import UserNotFoundError, UserValidationError

class TestUsersEventHandlers:
    @pytest.fixture
    def mock_repo(self):
        return MagicMock()

    @pytest.fixture
    def handlers(self, mock_repo):
        return EventHandlers(repository=mock_repo)

    def test_register_user_rpc(self, handlers, mock_repo):
        payload = {
            "name": "Ivan",
            "surname": "Carbajal",
            "dni": "123",
            "address": "Street 123"
        }
        mock_repo.create.return_value = {**payload, "id": 1}
        
        result = handlers.register_user_rpc(payload)
        
        mock_repo.create.assert_called_once()
        assert result["id"] == 1
        assert result["name"] == "Ivan"

    def test_register_user_rpc_validation_error(self, handlers):
        payload = {"name": "Ivan"} # Missing required fields
        
        # The handler now catches exception and returns error dict
        result = handlers.register_user_rpc(payload)
        
        assert "error" in result
        assert "Field required" in result["error"] or "missing" in result["error"] or "validation" in result["error"].lower()

    def test_update_user_rpc_success(self, handlers, mock_repo):
        payload = {"id": 1, "name": "Ivan Updated"}
        mock_repo.update.return_value = {"id": 1, "name": "Ivan Updated"}
        
        result = handlers.update_user_rpc(payload)
        
        mock_repo.update.assert_called_once()
        assert result["name"] == "Ivan Updated"

    def test_update_user_rpc_not_found(self, handlers, mock_repo):
        payload = {"id": 999, "name": "Ivan"}
        
        mock_repo.update.side_effect = UserNotFoundError("User not found")
        
        result = handlers.update_user_rpc(payload)
        
        assert "error" in result
        assert "User not found" in result["error"]
