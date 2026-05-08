import pytest
from playwright.sync_api import Page

from pages.booking_page import BookingPage


@pytest.mark.booking
def test_create_reservaiton(page: Page, base_url, person_generator):
    page_obj = BookingPage(page)

    page_obj.load_room_booking(base_url, 1, "2026-05-07", "2026-05-18")
    page_obj.click_reserve_now()
    page_obj.fill_reservation_form(**person_generator)
    page_obj.click_reserve_now()
    page_obj.confirmation_is_visible()
