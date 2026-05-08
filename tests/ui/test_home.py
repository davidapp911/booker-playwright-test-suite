import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage


@pytest.mark.home
def test_rooms_are_visible(page: Page, base_url):

    page_obj = HomePage(page)
    page_obj.navigate(base_url)
    page_obj.room_cards_are_visible()
