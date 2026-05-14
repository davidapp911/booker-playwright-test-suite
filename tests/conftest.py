import os

import pytest
from dotenv import load_dotenv

from api.client import BookerClient


@pytest.fixture(scope="session")
def base_url():
    load_dotenv()
    return os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def credentials():
    load_dotenv()
    return {"username": os.getenv("USERNAME"), "password": os.getenv("PASSWORD")}


@pytest.fixture(scope="session")
def auth_client(base_url, credentials):
    client = BookerClient(base_url)
    response = client.post("/api/auth/login", json=credentials)
    token_is_valid = client.post("/api/auth/validate", json=response.json()).json()["valid"]

    if token_is_valid:
        client.set_cookie("token", response.json()["token"])
        yield client
    else:
        raise RuntimeError("Auth setup failed: could not obtain a valid token")

    client.post("/api/auth/logout", json=response.json())
