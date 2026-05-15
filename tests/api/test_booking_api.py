import pytest

from api.models import BookingListResponse, BookingResponse
from helpers import fake_booking


@pytest.mark.booking_api
def test_valid_booking(auth_client, delete_booking_after):
    booking = fake_booking()

    response = auth_client.post("/api/booking", json=booking)
    delete_booking_after(response.json()["bookingid"])

    print(response.json())

    assert response.status_code == 201
    BookingResponse.model_validate(response.json())


@pytest.mark.booking_api
def test_get_booking_by_id(auth_client, created_booking):
    response = auth_client.get(f"/api/booking/{created_booking}")

    assert response.status_code == 200
    BookingResponse.model_validate(response.json())


@pytest.mark.booking_api
def test_list_bookings_by_roomid(auth_client):
    response = auth_client.get("/api/booking?roomid=1")

    assert response.status_code == 200
    BookingListResponse.model_validate(response.json())
