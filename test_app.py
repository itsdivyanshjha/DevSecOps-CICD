import pytest
from app import app as flask_app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    with flask_app.test_client() as client:
        yield client

def test_home_page_status(client):
    """Test that the home page returns a successful status code."""
    response = client.get('/')
    assert response.status_code == 200

def test_home_page_content(client):
    """Test that the home page contains the expected DevSecOps content."""
    response = client.get('/')
    html_content = response.get_data(as_text=True)
    
    # Check for key elements in the new HTML content
    assert "DevSecOps Pipeline Showcase" in html_content
    assert "Pipeline Stages" in html_content
    assert "SonarQube SAST Analysis" in html_content
    assert "OWASP Dependency Check" in html_content
    assert "Trivy Container Scan" in html_content
    assert "Docker Unit Tests" in html_content
    assert "Jenkins Container Deployment" in html_content
    assert "Experiment Overview" in html_content
    assert "Technology Stack" in html_content

def test_home_page_structure(client):
    """Test that the HTML structure is properly formatted."""
    response = client.get('/')
    html_content = response.get_data(as_text=True)
    
    # Check for proper HTML structure
    assert "<!DOCTYPE html>" in html_content
    assert "<html" in html_content
    assert "<head>" in html_content
    assert "<body>" in html_content
    assert "</html>" in html_content

def test_css_styling(client):
    """Test that CSS styling is included in the response."""
    response = client.get('/')
    html_content = response.get_data(as_text=True)
    
    # Check for CSS styles
    assert "background: linear-gradient" in html_content
    assert "border-radius" in html_content
    assert "box-shadow" in html_content

def test_pipeline_steps_count(client):
    """Test that all 6 pipeline steps are present."""
    response = client.get('/')
    html_content = response.get_data(as_text=True)
    
    # Count the step numbers (1-6)
    for i in range(1, 7):
        assert f'<div class="step-number">{i}</div>' in html_content

def test_technology_stack(client):
    """Test that the technology stack section includes expected tools."""
    response = client.get('/')
    html_content = response.get_data(as_text=True)
    
    # Check for technology tags
    expected_tools = ["Jenkins", "SonarQube", "OWASP", "Trivy", "Docker", "Python", "Flask"]
    for tool in expected_tools:
        assert f'<span class="tech-tag">{tool}</span>' in html_content