import pytest

from api.models import BookingListResponse, BookingResponse, BookingUpdateResponse
from helpers import fake_booking, fake_booking_dates, fake_id_num


@pytest.mark.booking_api
def test_valid_booking(auth_client, delete_booking_by_id, delete_message):
    booking = fake_booking()

    response = auth_client.post("/api/booking", json=booking)
    delete_booking_by_id(response.json()["bookingid"])
    delete_message(f"{booking['firstname']} {booking['lastname']}")

    assert response.status_code == 201
    BookingResponse.model_validate(response.json())


@pytest.mark.booking_api
def test_get_booking_by_id(auth_client, created_booking):
    response = auth_client.get(f"/api/booking/{created_booking['bookingid']}")
    assert response.status_code == 200
    BookingResponse.model_validate(response.json())


@pytest.mark.booking_api
def test_list_bookings_by_roomid(auth_client):
    response = auth_client.get("/api/booking?roomid=1")

    assert response.status_code == 200
    BookingListResponse.model_validate(response.json())


@pytest.mark.booking_api
def test_update_booking(auth_client, created_booking):
    response = auth_client.put(f"/api/booking/{created_booking['bookingid']}", json=fake_booking())

    assert response.status_code == 200
    BookingUpdateResponse.model_validate(response.json())


@pytest.mark.booking_api
def test_delete_booking(auth_client, created_booking):
    response = auth_client.delete(f"/api/booking/{created_booking['bookingid']}")

    assert response.status_code == 202


@pytest.mark.booking_api
def test_delete_booking_no_auth(client, created_booking):
    response = client.delete(f"/api/booking/{created_booking['bookingid']}")

    assert response.status_code == 403


@pytest.mark.booking_api
def test_update_booking_no_auth(client, created_booking):
    response = client.put(f"/api/booking/{created_booking['bookingid']}", json=fake_booking())

    assert response.status_code == 403


@pytest.mark.booking_api
def test_get_nonexistent_booking(auth_client):
    response = auth_client.get(f"/api/booking/{fake_id_num()}")
    assert response.status_code == 404


@pytest.mark.booking_api
def test_invalid_date_range_booking(auth_client):
    invalid_booking = fake_booking()
    invalid_booking["bookingdates"] = fake_booking_dates(1, -5)

    response = auth_client.post("/api/booking", json=invalid_booking)

    assert response.status_code == 409


@pytest.mark.booking_api
def test_overlapping_booking(auth_client, created_room, delete_booking_by_id, delete_message):
    initial_booking = fake_booking()
    overlapping_booking = fake_booking()
    initial_booking["roomid"] = created_room["id"]
    overlapping_booking["roomid"] = created_room["id"]
    initial_booking["bookingdates"] = fake_booking_dates(1, 3)
    overlapping_booking["bookingdates"] = fake_booking_dates(2, 4)

    response = auth_client.post("/api/booking", json=initial_booking)

    delete_booking_by_id(response.json()["bookingid"])
    delete_message(f"{initial_booking['firstname']} {initial_booking['lastname']}")
    assert response.status_code == 201
    BookingResponse.model_validate(response.json())

    response = auth_client.post("/api/booking", json=overlapping_booking)
    assert response.status_code == 409
