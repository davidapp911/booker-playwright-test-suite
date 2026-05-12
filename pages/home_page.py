from pages.base_page import BasePage


class HomePage(BasePage):
    ROOMS = "#rooms"

    def room_cards(self):
        return self.page.locator(self.ROOMS)
