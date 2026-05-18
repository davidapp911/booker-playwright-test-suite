import pytest

from api.models import BookingListResponse, BookingResponse, BookingUpdateResponse
from helpers import fake_booking


@pytest.mark.booking_api
def test_valid_booking(auth_client, delete_booking_by_id, delete_message):
    booking = fake_booking()

    response = auth_client.post("/api/booking", json=booking)
    delete_booking_by_id(response.json()["bookingid"])
    delete_message(f"{booking['firstname']} {booking['lastname']}")

    print(f"{booking['firstname']} {booking['lastname']}")

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


@pytest.mark.booking_api
def test_update_booking(auth_client, created_room, created_booking):
    updated_booking = fake_booking()
    updated_booking["roomid"] = created_room["id"]

    response = auth_client.put(f"/api/booking/{created_booking}", json=updated_booking)

    assert response.status_code == 200
    BookingUpdateResponse.model_validate(response.json())
