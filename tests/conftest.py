import os
from collections.abc import Callable, Generator
from typing import Any

import pytest
from dotenv import load_dotenv

from api.client import BookerClient
from helpers import fake_booking, fake_room

load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    url = os.getenv("BASE_URL")
    if not url:
        raise RuntimeError("BASE_URL not set in environment")
    return url


# --------> authentication
@pytest.fixture(scope="session")
def credentials() -> dict[str, str]:
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    if not username or not password:
        raise RuntimeError("ADMIN_USERNAME or ADMIN_PASSWORD not set in environment")
    return {"username": username, "password": password}


@pytest.fixture(scope="session")
def client(base_url) -> BookerClient:
    return BookerClient(base_url)


@pytest.fixture(scope="session")
def auth_client(client, credentials) -> Generator[BookerClient, None, None]:
    response = client.post("/api/auth/login", json=credentials)
    token_is_valid = client.post("/api/auth/validate", json=response.json()).json()["valid"]

    if token_is_valid:
        client.set_cookie("token", response.json()["token"])
    else:
        raise RuntimeError("Auth setup failed: could not obtain a valid token")

    yield client

    client.post("/api/auth/logout", json=response.json())


# --------> booking
@pytest.fixture()
def created_booking(auth_client, delete_message) -> Generator[int, None, None]:
    booking = fake_booking()
    delete_message(f"{booking['firstname']} {booking['lastname']}")
    booking_id = auth_client.post("/api/booking", json=booking).json()["bookingid"]

    yield booking_id

    if booking_id:
        auth_client.delete(f"/api/booking/{booking_id}")


@pytest.fixture()
def delete_booking_by_id(auth_client) -> Generator[Callable[[int], None], None, None]:
    booking_id = None

    def _set_booking_id(id):
        nonlocal booking_id
        booking_id = id

    yield _set_booking_id

    if booking_id:
        auth_client.delete(f"/api/booking/{booking_id}")


@pytest.fixture()
def delete_booking_by_room_id(auth_client) -> Generator[Callable[[int], None], None, None]:
    room_id = None

    def _set_room_id(id):
        nonlocal room_id
        room_id = id

    yield _set_room_id

    if room_id:
        response = auth_client.get(f"/api/booking?roomid={room_id}")
        bookings = response.json()["bookings"]
        for entry in bookings:
            auth_client.delete(f"/api/booking/{entry['bookingid']}")


# --------> rooms
@pytest.fixture()
def created_room(auth_client) -> Generator[dict[str, Any], None, None]:
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
def delete_room(auth_client) -> Generator[Callable[[str], None], None, None]:
    room_name = None

    def _set_room(name):
        nonlocal room_name
        room_name = name

    yield _set_room

    if room_name:
        rooms = auth_client.get("/api/room").json()["rooms"]
        room_id = next((r["roomid"] for r in rooms if str(r["roomName"]) == str(room_name)), None)
        if room_id:
            auth_client.delete(f"/api/room/{room_id}")


# -----------> messages
@pytest.fixture()
def delete_message(auth_client) -> Generator[Callable[[str], None], None, None]:
    message_name = None

    def _set_name(name):
        nonlocal message_name
        message_name = name

    yield _set_name

    message_id = next(
        (m["id"] for m in auth_client.get("/api/message").json()["messages"] if m["name"] == message_name), None
    )

    if message_id:
        auth_client.delete(f"/api/message/{message_id}")
