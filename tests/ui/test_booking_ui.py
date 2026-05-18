import pytest
from playwright.sync_api import Page, expect

from helpers import apply_field_rules, fake_booking, fake_booking_dates, relative_date
from pages.booking_page import BookingPage


@pytest.mark.booking
def test_create_reservation(page: Page, base_url, created_room, delete_booking_by_room_id, delete_message):
    booking_data = apply_field_rules(fake_booking(), exclude=["roomid", "depositpaid", "bookingdates"])
    delete_booking_by_room_id(created_room["id"])
    delete_message(f"{booking_data['firstname']} {booking_data['lastname']}")
    page_obj = BookingPage(page)
    page_obj.load_room_booking(base_url, created_room["id"], **fake_booking_dates())
    page_obj.click_reserve_now()
    page_obj.fill_reservation_form(**booking_data)
    page_obj.click_reserve_now()
    expect(page_obj.confirmation()).to_be_visible()


@pytest.mark.booking
def test_submit_empty_form(page: Page, base_url):
    page_obj = BookingPage(page)

    page_obj.load_room_booking(base_url, 1, **fake_booking_dates())
    page_obj.click_reserve_now()
    page_obj.click_reserve_now()
    expect(page_obj.empty_field_alert()).to_be_visible()


@pytest.mark.booking
def test_checkout_before_checkin_reservation(page: Page, base_url):
    # site crashes instead of showing a validation error - bug
    booking_data = apply_field_rules(fake_booking(), exclude=["roomid", "depositpaid", "bookingdates"])

    page_obj = BookingPage(page)
    page_obj.load_room_booking(base_url, 1, relative_date(), relative_date(-2))
    page_obj.click_reserve_now()
    page_obj.fill_reservation_form(**booking_data)
    page_obj.click_reserve_now()
    expect(page_obj.load_error()).to_be_visible()


@pytest.mark.xfail(reason="site accepts past check-in dates - bug")
def test_past_date_checkin_reservation(page: Page, base_url):
    booking_data = apply_field_rules(fake_booking(), exclude=["roomid", "depositpaid", "bookingdates"])
    page_obj = BookingPage(page)
    page_obj.load_room_booking(base_url, 1, relative_date(-2), relative_date(1))
    page_obj.click_reserve_now()
    page_obj.fill_reservation_form(**booking_data)
    page_obj.click_reserve_now()
    expect(page_obj.confirmation()).not_to_be_visible()


@pytest.mark.booking
def test_booking_not_reaching_server(page: Page, base_url):

    page.route(
        "**/api/booking",
        lambda route: (
            route.fulfill(status=500, content_type="application/json", body="{}")
            if route.request.method == "POST"
            else route.continue_()
        ),
    )

    booking_data = apply_field_rules(fake_booking(), exclude=["roomid", "depositpaid", "bookingdates"])
    page_obj = BookingPage(page)
    page_obj.load_room_booking(base_url, 1, **fake_booking_dates())
    page_obj.click_reserve_now()
    page_obj.fill_reservation_form(**booking_data)
    page_obj.click_reserve_now()
    expect(page_obj.load_error()).to_be_visible()
