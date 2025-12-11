

import pytest
from datetime import datetime
from apis.users.event_dispatcher import (
    register_user_rpc,
    list_users_rpc,
    update_user_rpc,
    send_email,
    USERS,
    USER_UPDATES_COUNT
)


@pytest.mark.unit
class TestRegisterUserRPC:
    
    def test_register_user_creates_new_user(self, reset_users_state, sample_user):
        result = register_user_rpc(sample_user)
        
        assert result["id"] == 1
        assert result["name"] == sample_user["name"]
        assert result["surname"] == sample_user["surname"]
        assert result["dni"] == sample_user["dni"]
        assert result["address"] == sample_user["address"]
        assert "created_at" in result
        assert "updated_at" in result
    
    def test_register_user_adds_to_users_list(self, reset_users_state, sample_user):
        initial_count = len(USERS)
        register_user_rpc(sample_user)
        
        assert len(USERS) == initial_count + 1
        assert USERS[0]["name"] == sample_user["name"]
    
    def test_register_user_increments_id(self, reset_users_state, sample_user):
        user1 = register_user_rpc(sample_user)
        user2 = register_user_rpc(sample_user)
        
        assert user1["id"] == 1
        assert user2["id"] == 2
    
    def test_register_user_sets_timestamps(self, reset_users_state, sample_user):
        result = register_user_rpc(sample_user)
        
        # Verify timestamps are ISO format strings
        datetime.fromisoformat(result["created_at"])
        datetime.fromisoformat(result["updated_at"])


@pytest.mark.unit
class TestListUsersRPC:
    
    def test_list_users_no_filters_returns_all(self, reset_users_state):
        # Register multiple users
        register_user_rpc({"name": "John", "surname": "Doe", "dni": "111", "address": "St 1"})
        register_user_rpc({"name": "Jane", "surname": "Smith", "dni": "222", "address": "St 2"})
        
        result = list_users_rpc({})
        
        assert len(result) == 2
    
    def test_list_users_filter_by_name(self, reset_users_state):
        register_user_rpc({"name": "John", "surname": "Doe", "dni": "111", "address": "St 1"})
        register_user_rpc({"name": "Jane", "surname": "Smith", "dni": "222", "address": "St 2"})
        
        result = list_users_rpc({"name": "John", "surname": None, "dni": None})
        
        assert len(result) == 1
        assert result[0]["name"] == "John"
    
    def test_list_users_filter_by_dni(self, reset_users_state):
        register_user_rpc({"name": "John", "surname": "Doe", "dni": "111", "address": "St 1"})
        register_user_rpc({"name": "Jane", "surname": "Smith", "dni": "222", "address": "St 2"})
        
        result = list_users_rpc({"name": None, "surname": None, "dni": "222"})
        
        assert len(result) == 1
        assert result[0]["dni"] == "222"
    
    def test_list_users_multiple_filters(self, reset_users_state):
        register_user_rpc({"name": "John", "surname": "Doe", "dni": "111", "address": "St 1"})
        register_user_rpc({"name": "John", "surname": "Smith", "dni": "222", "address": "St 2"})
        
        result = list_users_rpc({"name": "John", "surname": "Doe", "dni": None})
        
        assert len(result) == 1
        assert result[0]["surname"] == "Doe"
    
    def test_list_users_no_matches(self, reset_users_state):
        register_user_rpc({"name": "John", "surname": "Doe", "dni": "111", "address": "St 1"})
        
        result = list_users_rpc({"name": "NonExistent", "surname": None, "dni": None})
        
        assert len(result) == 0


@pytest.mark.unit
class TestUpdateUserRPC:
    
    def test_update_user_success(self, reset_users_state):
        user = register_user_rpc({"name": "John", "surname": "Doe", "dni": "111", "address": "St 1"})
        
        result = update_user_rpc({"id": user["id"], "name": "Jane"})
        
        assert result["name"] == "Jane"
        assert result["surname"] == "Doe"  # Unchanged
        assert result["id"] == user["id"]
    
    def test_update_user_multiple_fields(self, reset_users_state):
        user = register_user_rpc({"name": "John", "surname": "Doe", "dni": "111", "address": "St 1"})
        
        result = update_user_rpc({
            "id": user["id"],
            "name": "Jane",
            "address": "New Street 123"
        })
        
        assert result["name"] == "Jane"
        assert result["address"] == "New Street 123"
        assert result["surname"] == "Doe"  # Unchanged
    
    def test_update_user_not_found(self, reset_users_state):
        result = update_user_rpc({"id": 999, "name": "Jane"})
        
        assert "error" in result
        assert result["error"] == "User not found"
    
    def test_update_user_updates_timestamp(self, reset_users_state):
        user = register_user_rpc({"name": "John", "surname": "Doe", "dni": "111", "address": "St 1"})
        original_updated_at = user["updated_at"]
        
        import time
        time.sleep(0.01)  # Small delay to ensure timestamp difference
        
        result = update_user_rpc({"id": user["id"], "name": "Jane"})
        
        assert result["updated_at"] != original_updated_at
    
    def test_update_user_increments_counter(self, reset_users_state):
        from apis.users.event_dispatcher import USER_UPDATES_COUNT as initial_count
        
        user = register_user_rpc({"name": "John", "surname": "Doe", "dni": "111", "address": "St 1"})
        update_user_rpc({"id": user["id"], "name": "Jane"})
        
        from apis.users.event_dispatcher import USER_UPDATES_COUNT as final_count
        assert final_count == initial_count + 1


@pytest.mark.unit
class TestSendEmail:
    
    def test_send_email_executes_without_error(self, reset_users_state, sample_user_with_id):
        # Since loguru doesn't integrate with pytest's caplog,
        # we just verify the function executes successfully
        try:
            send_email(sample_user_with_id)
            # If we get here, the function executed successfully
            assert True
        except Exception as e:
            pytest.fail(f"send_email raised an exception: {e}")
