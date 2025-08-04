import pytest
from app import app as flask_app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    with flask_app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page to ensure it returns the correct message."""
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == "Hello! This is a simple Flask app for the DevSecOps demo."