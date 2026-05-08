from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    ROOMS = "#rooms"

    def room_cards_are_visible(self):
        expect(self.page.locator(self.ROOMS)).not_to_have_count(0)
