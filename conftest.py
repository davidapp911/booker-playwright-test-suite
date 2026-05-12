import os

import httpx
import pytest
from dotenv import load_dotenv

from helpers import fake_room


@pytest.fixture(scope="session")
def base_url():
    load_dotenv()
    return os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def username():
    load_dotenv()
    return os.getenv("USERNAME")


@pytest.fixture(scope="session")
def password():
    load_dotenv()
    return os.getenv("PASSWORD")


@pytest.fixture(scope="session")
def auth_token(base_url, username, password):

    response = httpx.post(
        f"{base_url}api/auth/login", json={"username": username, "password": password}
    )
    return response.json()["token"]


@pytest.fixture()
def delete_room_after(base_url, auth_token):
    room_name = None

    def _set_room(name):
        nonlocal room_name
        room_name = name

    yield _set_room

    rooms = httpx.get(f"{base_url}api/room").json()["rooms"]
    room_id = next(
        (r["roomid"] for r in rooms if str(r["roomName"]) == str(room_name)), None
    )
    if room_id:
        httpx.delete(f"{base_url}api/room/{room_id}", cookies={"token": auth_token})


@pytest.fixture()
def create_room(base_url, auth_token):
    data = fake_room()
    httpx.post(f"{base_url}api/room", json=data, cookies={"token": auth_token})

    yield data["roomName"]

    rooms = httpx.get(f"{base_url}api/room").json()["rooms"]
    room_id = next(
        (r["roomid"] for r in rooms if str(r["roomName"]) == str(data["roomName"])),
        None,
    )
    if room_id:
        httpx.delete(f"{base_url}api/room/{room_id}", cookies={"token": auth_token})
