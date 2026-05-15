import os

import pytest
from dotenv import load_dotenv

from api.client import BookerClient
from helpers import fake_booking, fake_room


@pytest.fixture(scope="session")
def base_url():
    load_dotenv()
    return os.getenv("BASE_URL")


# --------> authentication
@pytest.fixture(scope="session")
def credentials():
    load_dotenv()
    return {"username": os.getenv("USERNAME"), "password": os.getenv("PASSWORD")}


@pytest.fixture(scope="session")
def client(base_url):
    return BookerClient(base_url)


@pytest.fixture(scope="session")
def auth_client(client, credentials):
    response = client.post("/api/auth/login", json=credentials)
    token_is_valid = client.post("/api/auth/validate", json=response.json()).json()["valid"]

    if token_is_valid:
        client.set_cookie("token", response.json()["token"])
        yield client
    else:
        raise RuntimeError("Auth setup failed: could not obtain a valid token")

    client.post("/api/auth/logout", json=response.json())


# --------> booking
@pytest.fixture()
def created_booking(auth_client):
    booking = fake_booking()
    booking_id = auth_client.post("/api/booking", json=booking).json()["bookingid"]

    yield booking_id

    if booking_id:
        auth_client.delete(f"/api/booking/{booking_id}")


@pytest.fixture()
def delete_booking_after(auth_client):
    booking_id = None

    def _set_bookin_id(id):
        nonlocal booking_id
        booking_id = id

    yield _set_bookin_id

    if booking_id:
        auth_client.delete(f"/api/booking/{booking_id}")


# --------> rooms
@pytest.fixture()
def create_room(auth_client):
    data = fake_room()
    auth_client.post("/api/room", json=data)

    rooms = auth_client.get("/api/room").json()["rooms"]
    room_id = next(
        (r["roomid"] for r in rooms if str(r["roomName"]) == str(data["roomName"])),
        None,
    )

    yield {"id": room_id, "name": data["roomName"]}

    if room_id:
        auth_client.delete(f"/api/room/{room_id}")


@pytest.fixture()
def delete_room_after(auth_client):
    room_name = None

    def _set_room(name):
        nonlocal room_name
        room_name = name

    yield _set_room

    rooms = auth_client.get("/api/room").json()["rooms"]
    room_id = next((r["roomid"] for r in rooms if str(r["roomName"]) == str(room_name)), None)
    if room_id:
        auth_client.delete(f"/api/room/{room_id}")
