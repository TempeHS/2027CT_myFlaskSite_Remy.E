import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for our Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    """Test that the home page returns status 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_has_title(client):
    """Test that the home page contains our site title."""
    response = client.get("/")
    assert b"My Flask Site" in response.data
