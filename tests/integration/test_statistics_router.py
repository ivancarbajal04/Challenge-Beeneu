

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


@pytest.mark.integration
class TestTotalUsersEndpoint:
    
    def test_get_total_users_success(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": {"total_users": 42}
        }
        
        with patch('apis.statistics.router.publisher', mock_publisher):
            response = test_client.get("/statistics/total-users")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_users"] == 42
        
        mock_publisher.call_rpc.assert_called_once_with(
            event_type="TOTAL_USERS_RPC",
            payload={}
        )
    
    def test_get_total_users_zero(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": {"total_users": 0}
        }
        
        with patch('apis.statistics.router.publisher', mock_publisher):
            response = test_client.get("/statistics/total-users")
        
        assert response.status_code == 200
        assert response.json()["total_users"] == 0
    
    def test_get_total_users_rpc_failure(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": False,
            "error": "Statistics service unavailable"
        }
        
        with patch('apis.statistics.router.publisher', mock_publisher):
            response = test_client.get("/statistics/total-users")
        
        assert response.status_code == 500
        assert "Statistics service unavailable" in response.json()["detail"]


@pytest.mark.integration
class TestTotalUpdatesEndpoint:
    
    def test_get_total_updates_success(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": {"total_updates": 15}
        }
        
        with patch('apis.statistics.router.publisher', mock_publisher):
            response = test_client.get("/statistics/total-updates")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_updates"] == 15
        
        mock_publisher.call_rpc.assert_called_once_with(
            event_type="TOTAL_UPDATES_RPC",
            payload={}
        )
    
    def test_get_total_updates_zero(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": {"total_updates": 0}
        }
        
        with patch('apis.statistics.router.publisher', mock_publisher):
            response = test_client.get("/statistics/total-updates")
        
        assert response.status_code == 200
        assert response.json()["total_updates"] == 0
    
    def test_get_total_updates_rpc_failure(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": False,
            "error": "Service error"
        }
        
        with patch('apis.statistics.router.publisher', mock_publisher):
            response = test_client.get("/statistics/total-updates")
        
        assert response.status_code == 500


@pytest.mark.integration
class TestRegisteredLast24hEndpoint:
    
    def test_get_registered_last_24h_success(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": {"registered_last_24h": 7}
        }
        
        with patch('apis.statistics.router.publisher', mock_publisher):
            response = test_client.get("/statistics/registered-last-24h")
        
        assert response.status_code == 200
        data = response.json()
        assert data["registered_last_24h"] == 7
        
        mock_publisher.call_rpc.assert_called_once_with(
            event_type="REGISTERED_LAST_24_RPC",
            payload={}
        )
    
    def test_get_registered_last_24h_zero(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": {"registered_last_24h": 0}
        }
        
        with patch('apis.statistics.router.publisher', mock_publisher):
            response = test_client.get("/statistics/registered-last-24h")
        
        assert response.status_code == 200
        assert response.json()["registered_last_24h"] == 0
    
    def test_get_registered_last_24h_rpc_failure(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": False,
            "error": "Timeline data unavailable"
        }
        
        with patch('apis.statistics.router.publisher', mock_publisher):
            response = test_client.get("/statistics/registered-last-24h")
        
        assert response.status_code == 500
        assert "Timeline data unavailable" in response.json()["detail"]


@pytest.mark.integration
class TestStatisticsEndpointsIntegration:
    
    def test_all_statistics_endpoints_available(self, test_client, mock_publisher):
        mock_publisher.call_rpc.return_value = {
            "success": True,
            "data": {"value": 0}
        }
        
        endpoints = [
            "/statistics/total-users",
            "/statistics/total-updates",
            "/statistics/registered-last-24h"
        ]
        
        with patch('apis.statistics.router.publisher', mock_publisher):
            for endpoint in endpoints:
                response = test_client.get(endpoint)
                assert response.status_code == 200, f"Endpoint {endpoint} failed"
