import re

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage


@pytest.mark.home
def test_assert_title(page: Page, base_url):

    page.goto(base_url)

    expect(page).to_have_title(re.compile("Restful"))


@pytest.mark.home
def test_rooms_are_visible(page: Page, base_url):

    page_obj = HomePage(page)
    page_obj.load(base_url)
    page_obj.room_cards_are_visible()
