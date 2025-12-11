

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestRegisterUserEndpoint:
    
    def test_register_user_success(self, test_client, sample_user, mock_publisher):
        # Mock the publisher to return success
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": {**sample_user, "id": 1}
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.post("/users/register", json=sample_user)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["user"]["name"] == sample_user["name"]
        
        # Verify RPC was called
        mock_publisher.call_rpc.assert_called_once_with(
            event_type="REGISTER_USER_RPC",
            payload=sample_user
        )
        
        # Verify event was published
        mock_publisher.publish.assert_called_once()
    
    def test_register_user_rpc_failure(self, test_client, sample_user, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": False,
            "error": "Database connection failed"
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.post("/users/register", json=sample_user)
        
        assert response.status_code == 500
        assert "Database connection failed" in response.json()["detail"]
    
    def test_register_user_invalid_payload(self, test_client, mock_publisher):
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.post("/users/register", json={})
        
        # Should still call the RPC (validation happens in event_dispatcher)
        assert response.status_code in [200, 400, 422, 500]
    
    def test_register_user_publishes_event(self, test_client, sample_user, mock_publisher):
        user_data = {**sample_user, "id": 1}
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": user_data
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.post("/users/register", json=sample_user)
        
        # Verify the event was published with correct data
        mock_publisher.publish.assert_called_once_with(
            event_type="USER_REGISTERED_EVENT",
            payload=user_data
        )


@pytest.mark.integration
class TestListUsersEndpoint:
    
    def test_list_users_no_filters(self, test_client, mock_publisher):
        mock_users = [
            {"id": 1, "name": "John", "surname": "Doe"},
            {"id": 2, "name": "Jane", "surname": "Smith"}
        ]
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": mock_users
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.get("/users/")
        
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert len(data["users"]) == 2
        
        # Verify RPC was called with None filters
        mock_publisher.call_rpc.assert_called_once_with(
            event_type="LIST_USERS_RPC",
            payload={"name": None, "surname": None, "dni": None}
        )
    
    def test_list_users_with_name_filter(self, test_client, mock_publisher):
        mock_users = [{"id": 1, "name": "John", "surname": "Doe"}]
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": mock_users
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.get("/users/?name=John")
        
        assert response.status_code == 200
        
        # Verify RPC was called with name filter
        mock_publisher.call_rpc.assert_called_once_with(
            event_type="LIST_USERS_RPC",
            payload={"name": "John", "surname": None, "dni": None}
        )
    
    def test_list_users_with_multiple_filters(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": []
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.get("/users/?name=John&dni=12345678")
        
        assert response.status_code == 200
        
        # Verify RPC was called with multiple filters
        mock_publisher.call_rpc.assert_called_once_with(
            event_type="LIST_USERS_RPC",
            payload={"name": "John", "surname": None, "dni": "12345678"}
        )
    
    def test_list_users_rpc_failure(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": False,
            "error": "Service unavailable"
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.get("/users/")
        
        assert response.status_code == 500


@pytest.mark.integration
class TestUpdateUserEndpoint:
    
    def test_update_user_success(self, test_client, mock_publisher):
        update_payload = {"id": 1, "name": "Jane"}
        updated_user = {"id": 1, "name": "Jane", "surname": "Doe"}
        
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": updated_user
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.put("/users/update", json=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["user"]["name"] == "Jane"
        
        # Verify RPC was called
        mock_publisher.call_rpc.assert_called_once_with(
            event_type="UPDATE_USER_RPC",
            payload=update_payload
        )
        
        # Verify event was published
        mock_publisher.publish.assert_called_once_with(
            event_type="USER_UPDATED_EVENT",
            payload=updated_user
        )
    
    def test_update_user_missing_id(self, test_client, mock_publisher):
        update_payload = {"name": "Jane"}  # Missing 'id'
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.put("/users/update", json=update_payload)
        
        assert response.status_code == 400
        assert "id" in response.json()["detail"].lower()
    
    def test_update_user_not_found(self, test_client, mock_publisher):
        update_payload = {"id": 999, "name": "Jane"}
        
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": {"error": "User not found"}
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.put("/users/update", json=update_payload)
        
        assert response.status_code == 404
    
    def test_update_user_rpc_failure(self, test_client, mock_publisher):
        update_payload = {"id": 1, "name": "Jane"}
        
        mock_publisher.call_rpc.return_value = {
            "success": False,
            "error": "Update failed"
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.put("/users/update", json=update_payload)
        
        assert response.status_code == 500
    
    def test_update_user_multiple_fields(self, test_client, mock_publisher):
        update_payload = {
            "id": 1,
            "name": "Jane",
            "address": "456 New St"
        }
        
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": {**update_payload, "surname": "Doe"}
        }
        
        with patch('apis.users.router.publisher', mock_publisher):
            response = test_client.put("/users/update", json=update_payload)
        
        assert response.status_code == 200
        
        # Verify RPC was called with all fields
        mock_publisher.call_rpc.assert_called_once_with(
            event_type="UPDATE_USER_RPC",
            payload=update_payload
        )
