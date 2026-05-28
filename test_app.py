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


def test_home_alias_route_loads(client):
    """Test that /home route is available."""
    response = client.get("/home")
    assert response.status_code == 200


def test_music_page_loads(client):
    """Test that the music page returns status 200."""
    response = client.get("/music")
    assert response.status_code == 200


def test_music_page_has_content(client):
    """Test that the music page contains expected content."""
    response = client.get("/music")
    assert b"Sheet music and tracks" in response.data


def test_home_nav_link_is_active_on_home(client):
    """Test that Home nav item is marked active on the home route."""
    response = client.get("/")
    assert b'nav-link active' in response.data


def test_music_nav_link_is_active_on_music(client):
    """Test that Music nav item is marked active on the music route."""
    response = client.get("/music")
    assert b'href="/music">Music</a>' in response.data
    assert b'nav-link active' in response.data


def test_unknown_route_returns_404(client):
    """Test that an unknown route returns 404."""
    response = client.get("/does-not-exist")
    assert response.status_code == 404
