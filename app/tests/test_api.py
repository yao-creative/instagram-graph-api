import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.schemas.instagram import Period, MetricType, Metric


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint returns the expected response."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "version" in response.json()


def test_health_check(client):
    """Test the health check endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@patch("app.services.instagram.InstagramGraphService")
def test_get_instagram_insights(mock_service, client):
    """Test the Instagram insights endpoint with mocked service."""
    # Configure mock
    mock_instance = mock_service.return_value
    mock_instance.get_insights.return_value = {
        "status": "success",
        "message": "Successfully retrieved Instagram insights",
        "data": {
            "data": [
                {
                    "name": "reach",
                    "period": "day",
                    "title": "Reach",
                    "description": "Number of unique accounts that saw your content",
                    "id": "12345_reach/day",
                    "total_value": {"value": 1000}
                }
            ]
        }
    }
    
    # Make request
    response = client.get(
        "/api/v1/instagram/insights",
        params={
            "instagram_account_id": "12345",
            "metrics": [Metric.REACH],
            "period": Period.DAY,
            "metric_type": MetricType.TOTAL_VALUE
        }
    )
    
    # Check response
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify mock was called with expected parameters
    mock_instance.get_insights.assert_called_once()


@patch("app.services.instagram.InstagramGraphService")
def test_get_sample_requests(mock_service, client):
    """Test the sample requests endpoint with mocked service."""
    # Configure mock
    mock_instance = mock_service.return_value
    mock_instance.generate_sample_requests.return_value = {
        "example1": {
            "url": "/api/v1/insights?instagram_account_id=12345&metrics=reach",
            "description": "Example request"
        }
    }
    
    # Make request
    response = client.get("/api/v1/instagram/sample-requests")
    
    # Check response
    assert response.status_code == 200
    assert "samples" in response.json()
    assert "example1" in response.json()["samples"] 