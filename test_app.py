from io import BytesIO
import json

import pytest

import app as app_module


@pytest.fixture
def app_env(tmp_path, monkeypatch):
    sign_ups_file = tmp_path / "data" / "sign_ups.csv"
    performances_file = tmp_path / "data" / "upcoming_performances.json"
    images_dir = tmp_path / "images"
    images_dir.mkdir()

    (images_dir / "choir_camp.jpg").write_bytes(b"fake image bytes")
    (images_dir / "ignore.txt").write_text("not an image", encoding="utf-8")

    monkeypatch.setattr(app_module, "SIGN_UPS_FILE", sign_ups_file)
    monkeypatch.setattr(app_module, "PERFORMANCES_FILE", performances_file)
    monkeypatch.setattr(app_module, "IMAGES_DIR", images_dir)

    app_module.app.config.update(TESTING=True)

    return {
        "app": app_module.app,
        "sign_ups_file": sign_ups_file,
        "performances_file": performances_file,
        "images_dir": images_dir,
    }


@pytest.fixture
def client(app_env):
    with app_env["app"].test_client() as client:
        yield client


@pytest.fixture
def admin_client(client):
    response = client.post(
        "/sign-up",
        data={
            "full_name": "admin",
            "school_year": "12",
            "email": "admin",
        },
    )
    assert response.status_code == 302
    assert "/admin" in response.headers["Location"]
    return client


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_contains_main_content_and_footer_links(client):
    response = client.get("/")
    assert b"Tempe High School Choir" in response.data
    assert b"Upcoming Performances:" in response.data
    assert b"LICENSE" in response.data
    assert b"GitHub" in response.data
    assert b"Attribution" in response.data


def test_home_alias_route_loads(client):
    response = client.get("/home")
    assert response.status_code == 200


def test_home_mono_route_loads_and_enables_mono_mode(client):
    response = client.get("/home/mono")
    assert response.status_code == 200
    assert b"mono-mode" in response.data
    assert b'href="/music"' in response.data

    later_response = client.get("/music")
    assert b"mono-mode" in later_response.data


def test_music_page_loads_and_lists_sheet_music(client):
    response = client.get("/music")
    assert response.status_code == 200
    assert b"Sheet music and tracks." in response.data
    assert b"Wicked Medley" in response.data
    assert b"Open PDF" in response.data
    assert b"Search music" in response.data


def test_music_mono_route_loads(client):
    response = client.get("/music/mono")
    assert response.status_code == 200
    assert b"mono-mode" in response.data


def test_photos_page_lists_images_from_gallery_directory(client):
    response = client.get("/photos")
    assert response.status_code == 200
    assert b"Choir Camp" in response.data
    assert b"ignore.txt" not in response.data


def test_sign_up_page_loads(client):
    response = client.get("/sign-up")
    assert response.status_code == 200
    assert b"Register for choir with your name and email." in response.data
    assert b"Use your school email so choir sign-ups stay organised" in response.data
    assert b"mono-mode" not in response.data


def test_sign_up_mono_success_redirect_stays_in_mono_mode(client):
    response = client.post(
        "/sign-up/mono",
        data={
            "full_name": "Remy Ellis",
            "school_year": "10",
            "email": "remy.ellis@education.nsw.gov.au",
        },
    )

    assert response.status_code == 302
    assert "/sign-up/mono?success=1" in response.headers["Location"]


def test_sign_up_rejects_non_nsw_education_email(client, app_env):
    response = client.post(
        "/sign-up",
        data={
            "full_name": "Remy Ellis",
            "school_year": "10",
            "email": "remy@example.com",
        },
    )

    assert response.status_code == 200
    assert b"Email must end in @education.nsw.gov.au." in response.data
    assert not app_env["sign_ups_file"].exists()


def test_sign_up_accepts_valid_email_and_saves_csv(client, app_env):
    response = client.post(
        "/sign-up",
        data={
            "full_name": "Remy Ellis",
            "school_year": "10",
            "email": "remy.ellis@education.nsw.gov.au",
        },
    )

    assert response.status_code == 302
    assert "success=1" in response.headers["Location"]
    csv_text = app_env["sign_ups_file"].read_text(encoding="utf-8")
    assert "Remy Ellis" in csv_text
    assert "10" in csv_text
    assert "remy.ellis@education.nsw.gov.au" in csv_text


def test_sign_up_shows_error_when_save_fails(client, monkeypatch):
    def fail_to_save(_sign_up_data):
        raise OSError("disk full")

    monkeypatch.setattr(app_module, "save_sign_up", fail_to_save)

    response = client.post(
        "/sign-up",
        data={
            "full_name": "Remy Ellis",
            "school_year": "10",
            "email": "remy.ellis@education.nsw.gov.au",
        },
    )

    assert response.status_code == 200
    assert b"could not be saved right now" in response.data


def test_admin_route_requires_sign_in(client):
    response = client.get("/admin")
    assert response.status_code == 302
    assert "/sign-up" in response.headers["Location"]


def test_admin_sign_in_sets_session_and_shows_dashboard(client):
    response = client.post(
        "/sign-up",
        data={
            "full_name": "admin",
            "school_year": "12",
            "email": "admin",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Admin Dashboard" in response.data
    with client.session_transaction() as session:
        assert session["is_admin"] is True


def test_admin_sign_in_from_mono_redirects_to_mono_dashboard(client):
    response = client.post(
        "/sign-up/mono",
        data={
            "full_name": "admin",
            "school_year": "12",
            "email": "admin",
        },
    )

    assert response.status_code == 302
    assert "/admin/mono" in response.headers["Location"]


def test_admin_dashboard_displays_saved_sign_ups(admin_client):
    app_module.save_sign_up(
        {
            "full_name": "Student Example",
            "school_year": "9",
            "email": "student.example@education.nsw.gov.au",
        }
    )

    response = admin_client.get("/admin")
    assert response.status_code == 200
    assert b"Student Example" in response.data
    assert b"Download Sign-Ups CSV" in response.data
    assert b"Search Sign-Ups" in response.data


def test_faq_page_loads_search_box_and_existing_questions(client):
    response = client.get("/faqs")
    assert response.status_code == 200
    assert b"Search FAQs" in response.data
    assert b"When and where are choir rehearsals?" in response.data


def test_snack_roster_page_loads(client):
    response = client.get("/snack-roster")
    assert response.status_code == 200
    assert b"Snack Roster" in response.data
    assert b"How This Page Can Be Used" in response.data


def test_admin_can_update_performances_and_home_reflects_changes(admin_client, app_env):
    response = admin_client.post(
        "/admin",
        data={
            "action": "performances",
            "performance_title": [
                "Concert Night",
                "",
                "",
                "",
                "",
            ],
            "performance_where": [
                "School Hall",
                "",
                "",
                "",
                "",
            ],
            "performance_time": [
                "6:00 PM",
                "",
                "",
                "",
                "",
            ],
            "performance_date": [
                "Friday 20 June 2026",
                "",
                "",
                "",
                "",
            ],
            "performance_notes": [
                "Arrive early",
                "",
                "",
                "",
                "",
            ],
        },
    )

    assert response.status_code == 302
    saved_performances = json.loads(app_env["performances_file"].read_text(encoding="utf-8"))
    assert saved_performances[0]["title"] == "Concert Night"

    home_response = admin_client.get("/home")
    assert b"Concert Night" in home_response.data
    assert b"School Hall" in home_response.data


def test_admin_can_upload_valid_photos_only(admin_client, app_env):
    response = admin_client.post(
        "/admin",
        data={
            "action": "photos",
            "photo_uploads": [
                (BytesIO(b"fake image bytes"), "new_photo.jpg"),
                (BytesIO(b"plain text"), "not_photo.txt"),
            ],
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 302
    uploaded_files = sorted(path.name for path in app_env["images_dir"].iterdir())
    assert any(name.startswith("new_photo") for name in uploaded_files)
    assert "not_photo.txt" not in uploaded_files


def test_download_sign_ups_requires_admin(client):
    response = client.get("/admin/sign-ups/download")
    assert response.status_code == 302
    assert "/sign-up" in response.headers["Location"]


def test_admin_can_download_sign_ups_csv(admin_client):
    app_module.save_sign_up(
        {
            "full_name": "Student Example",
            "school_year": "9",
            "email": "student.example@education.nsw.gov.au",
        }
    )

    response = admin_client.get("/admin/sign-ups/download")
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert b"Student Example" in response.data
    response.close()


def test_license_and_attribution_routes_load(client):
    license_response = client.get("/license")
    attribution_response = client.get("/attribution")

    assert license_response.status_code == 200
    assert b"GNU GENERAL PUBLIC LICENSE" in license_response.data
    assert attribution_response.status_code == 200


def test_unknown_route_returns_404(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404


def test_accessibility_preferences_can_be_saved_and_persist_across_pages(client):
    response = client.post(
        "/accessibility",
        data={
            "next_url": "/home",
            "dyslexic_font": "on",
            "dark_mode": "on",
            "large_text": "on",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/home")

    home_response = client.get("/home")
    assert b"mono-mode" in home_response.data
    assert b"dark-mode" in home_response.data
    assert b"large-text" in home_response.data

    faq_response = client.get("/faqs")
    assert b"dark-mode" in faq_response.data
    assert b"OpenDyslexic font" in faq_response.data


def test_accessibility_reset_strips_mono_path_and_clears_preferences(client):
    client.get("/home/mono")

    response = client.post(
        "/accessibility/mono",
        data={
            "next_url": "/home/mono",
            "reset": "1",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/home")

    home_response = client.get("/home")
    assert b"mono-mode" not in home_response.data
