import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_ready_endpoint(client):
    """Test ready probe endpoint"""
    response = client.get('/ready')
    assert response.status_code == 200
    assert response.json['ready'] is True

def test_api_status_endpoint(client):
    """Test API status endpoint"""
    response = client.get('/api/status')
    assert response.status_code == 200
    assert response.json['message'] == 'API is working'

def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert 'error' in response.json
