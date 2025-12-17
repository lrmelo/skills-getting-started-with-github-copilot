from fastapi.testclient import TestClient
import copy
import src.app as app_module

client = TestClient(app_module.app)


def _ensure_absent(activity, email):
    parts = app_module.activities[activity]["participants"]
    app_module.activities[activity]["participants"] = [p for p in parts if p != email]


def _ensure_present(activity, email):
    parts = app_module.activities[activity]["participants"]
    if email not in parts:
        parts.append(email)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_duplicate():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure clean start
    _ensure_absent(activity, email)

    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400


def test_remove_participant():
    activity = "Chess Club"
    email = "removeme@example.com"

    # Ensure the participant exists, then remove
    _ensure_present(activity, email)
    assert email in app_module.activities[activity]["participants"]

    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]
