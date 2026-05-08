from playwright.sync_api import expect

from pages.base_page import BasePage


class BookingPage(BasePage):
    def load_room_booking(self, base_url, room_id: int, check_in: str, check_out: str):
        url = f"{base_url}reservation/{room_id}?checkin={check_in}&checkout={check_out}"
        self.navigate(url)

    def click_reserve_now(self):
        self.page.get_by_role("button", name="Reserve Now").click()

    def fill_reservation_form(self, first_name: str, last_name: str, email: str, phone: str):
        self.page.get_by_role("textbox", name="Firstname").fill(first_name)
        self.page.get_by_role("textbox", name="Lastname").fill(last_name)
        self.page.get_by_role("textbox", name="Email").fill(email)
        self.page.get_by_role("textbox", name="Phone").fill(phone)

    def confirmation_is_visible(self):
        expect(self.page.get_by_role("heading", name="Booking Confirmed")).to_be_visible()
