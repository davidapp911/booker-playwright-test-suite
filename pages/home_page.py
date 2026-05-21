from playwright.sync_api import Locator

from pages.base_page import BasePage


class HomePage(BasePage):
    ROOMS = "#rooms"
    AVAILABILITY_CALENDAR = "#booking"

    def room_cards(self) -> Locator:
        return self.page.locator(self.ROOMS)

    def availability_calendar(self) -> Locator:
        return self.page.locator(self.AVAILABILITY_CALENDAR)
