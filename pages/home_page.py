from playwright.sync_api import Locator

from pages.base_page import BasePage


class HomePage(BasePage):
    ROOMS = "#rooms"

    def room_cards(self) -> Locator:
        return self.page.locator(self.ROOMS)
