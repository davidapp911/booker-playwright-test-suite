import pytest
from playwright.sync_api import Page

from helpers import dategen_today, person_generator
from pages.booking_page import BookingPage


@pytest.mark.booking
def test_create_reservation(page: Page, base_url):
    page_obj = BookingPage(page)

    page_obj.load_room_booking(base_url, 1, dategen_today(), dategen_today(2))
    page_obj.click_reserve_now()
    page_obj.fill_reservation_form(**person_generator())
    page_obj.click_reserve_now()
    page_obj.confirmation_is_visible()


@pytest.mark.booking
def test_submit_empty_form(page: Page, base_url):
    page_obj = BookingPage(page)

    page_obj.load_room_booking(base_url, 1, dategen_today(), dategen_today(2))
    page_obj.click_reserve_now()
    page_obj.click_reserve_now()
    page_obj.alert_is_visible()


@pytest.mark.booking
def test_checkout_before_checkin_reservation(page: Page, base_url):
    # site crashes instead of showing a validation error - bug
    page_obj = BookingPage(page)
    page_obj.load_room_booking(base_url, 1, dategen_today(), dategen_today(-2))
    page_obj.click_reserve_now()
    page_obj.fill_reservation_form(**person_generator())
    page_obj.click_reserve_now()
    page_obj.load_error_is_visible()


@pytest.mark.xfail(reason="site accepts past check-in dates - bug")
def test_past_date_checkin_reservation(page: Page, base_url):
    page_obj = BookingPage(page)
    page_obj.load_room_booking(base_url, 1, dategen_today(-2), dategen_today(1))
    page_obj.click_reserve_now()
    page_obj.fill_reservation_form(**person_generator())
    page_obj.click_reserve_now()
    page_obj.confirmation_is_not_visible()
