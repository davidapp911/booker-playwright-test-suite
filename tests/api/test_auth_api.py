import pytest


@pytest.mark.auth
def test_valid_login_returns_token(client, credentials):
    response = client.post("/api/auth/login", json=credentials)
    assert response.status_code == 200
    assert response.json()["token"]


@pytest.mark.auth
def test_invalid_password(client, credentials):
    wrong_credentials = {
        "username": credentials["username"],
        "password": "ThIsIsAwRoNgPaSsWoRd",
    }
    response = client.post("/api/auth/login", json=wrong_credentials)
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid credentials"


@pytest.mark.auth
def test_missing_credentials(client):
    response = client.post("/api/auth/login", json={})
    assert response.status_code != 200
