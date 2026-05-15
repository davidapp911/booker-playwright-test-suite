import pytest

from api.client import BookerClient
from helpers import fake_booking


@pytest.fixture(scope="session")
def client(base_url):
    return BookerClient(base_url)


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
