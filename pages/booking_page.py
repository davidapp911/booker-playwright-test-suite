from playwright.sync_api import expect

from pages.base_page import BasePage


class BookingPage(BasePage):
    def load_room_booking(self, base_url, room_id: int, check_in: str, check_out: str):
        url = f"{base_url}reservation/{room_id}?checkin={check_in}&checkout={check_out}"
        self.navigate(url)

    def click_reserve_now(self):
        self.page.get_by_role("button", name="Reserve Now").click()

    def fill_reservation_form(self, firstname: str, lastname: str, email: str, phone: str):
        self.page.get_by_role("textbox", name="Firstname").fill(firstname)
        self.page.get_by_role("textbox", name="Lastname").fill(lastname)
        self.page.get_by_role("textbox", name="Email").fill(email)
        self.page.get_by_role("textbox", name="Phone").fill(phone)

    def confirmation_is_visible(self):
        expect(self.page.get_by_role("heading", name="Booking Confirmed")).to_be_visible()

    def confirmation_is_not_visible(self):
        expect(self.page.get_by_role("heading", name="Booking Confirmed")).not_to_be_visible()

    def alert_is_visible(self):
        expect(self.page.get_by_role("alert").filter(has_text="Lastname should not be")).to_be_visible()

    def load_error_is_visible(self):
        expect(self.page.get_by_role("heading", name="This page couldn’t load")).to_be_visible()
