"""Tests for Flask application."""
import pytest
from src.app import app


@pytest.fixture
def client():
    """Create test client."""
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Health endpoint tests."""

    def test_health_returns_200(self, client):
        """Test health endpoint returns 200."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_returns_status(self, client):
        """Test health endpoint returns status."""
        response = client.get('/health')
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data


class TestReadyEndpoint:
    """Ready endpoint tests."""

    def test_ready_returns_200(self, client):
        """Test ready endpoint returns 200."""
        response = client.get('/ready')
        assert response.status_code == 200

    def test_ready_returns_true(self, client):
        """Test ready endpoint returns true."""
        response = client.get('/ready')
        data = response.get_json()
        assert data['ready'] is True


class TestAPIStatus:
    """API status endpoint tests."""

    def test_api_status_returns_200(self, client):
        """Test API status endpoint returns 200."""
        response = client.get('/api/status')
        assert response.status_code == 200

    def test_api_status_returns_message(self, client):
        """Test API status endpoint returns message."""
        response = client.get('/api/status')
        data = response.get_json()
        assert 'message' in data
        assert 'environment' in data
