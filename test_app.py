import app as app_module


def test_home_page_loads():
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as client:
        response = client.get("/")

    assert response.status_code == 200


def test_admin_sign_in_requires_correct_password(monkeypatch):
    monkeypatch.setattr(app_module, "ADMIN_PASSWORD", "test-admin-password")

    incorrect_attempt = {
        "full_name": "admin",
        "school_year": "12",
        "email": "admin",
        "admin_password": "incorrect-password",
    }
    correct_attempt = {**incorrect_attempt, "admin_password": "test-admin-password"}

    assert not app_module.is_admin_sign_in_attempt(incorrect_attempt)
    assert app_module.is_admin_sign_in_attempt(correct_attempt)
