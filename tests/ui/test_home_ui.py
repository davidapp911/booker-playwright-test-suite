import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage


@pytest.mark.home
def test_rooms_are_visible(page: Page, base_url):
    page_obj = HomePage(page)
    page_obj.navigate(base_url)
    expect(page_obj.room_cards()).not_to_have_count(0)


@pytest.mark.home
def test_availability_calendar_renders(page: Page, base_url):
    page_obj = HomePage(page)
    page_obj.navigate(base_url)
    expect(page_obj.availability_calendar()).to_be_visible()
