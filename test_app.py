import app as app_module


def test_sign_up_redirect_stays_in_standard_mode(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "SIGN_UPS_FILE", tmp_path / "sign_ups.csv")
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as client:
        response = client.post(
            "/sign-up",
            data={
                "full_name": "Test User",
                "school_year": "10",
                "email": "test.user@education.nsw.gov.au",
            },
        )
        redirected_response = client.get(response.headers["Location"])

    assert response.headers["Location"] == "/sign-up?success=1"
    assert b"mono-mode" not in redirected_response.data


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
